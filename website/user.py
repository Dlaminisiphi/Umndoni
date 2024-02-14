# Import Flask modules
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

# Import database-related modules
from .database import db, User, ReportedIssue

# Import Time
import time
from datetime import datetime

# Import security-related modules
from werkzeug.security import generate_password_hash, check_password_hash

# Import notification-related modules
from .notifications import send_email, send_sms,convert_number

# Import file upload-related modules
from .CloudStorage import upload_to_cloud_storage, allowed_file

from .google_geolocation import get_coordinates_from_address, is_within_distance

# Import os module
import os
from werkzeug.utils import secure_filename
# Create a Blueprint for the user-related routes
user = Blueprint('user', __name__)

# Route for the home page
@user.route('/')
def home():

    return render_template("home_page.html" )

@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Check if the passwords match
        if password != password2:
            flash('Passwords do not match', 'error')
            return redirect(url_for('user.signup'))

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already in use', category='error')
            return redirect(url_for('user.signup'))

        # Check if name and surname have more than 4 characters
        if len(name) < 5 or len(surname) < 5:
            flash('Name and surname must have at least 5 characters', category='error')
            return redirect(url_for('user.signup'))

        # Check if phone number is exactly 10 digits and consists of only numbers
        if not (phone_number.isdigit() and len(phone_number) == 10):
            flash('Phone number must be 10 digits and consist of only numbers',category='error')
            return redirect(url_for('user.signup'))

        #Generate hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        #formattes phone number to +27
        convert_number(phone_number)
        # Create a new user
        new_user = User(email=email, name=name, surname=surname, phone_number=phone_number, password=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        # Send email notification
        email_subject = 'Welcome to FixIt Umdoni! 🛠️'
        email_message = f'''
        Hi {name},

        Welcome to FixIt Umdoni! Thank you for signing up.

        Ready to make a difference? Report maintenance issues in a snap and help us keep Umdoni in top shape!

        Get started:
        1. Tap "Report Issue."
        2. Provide details and snap a photo.
        3. Track your reports in "My Reports."

        Have questions? Reach us at [fixitumdoni@gmail.com].

        Let's make Umdoni better together!

        Best,
        The FixIt Umdoni Team 🌟
        '''

        send_email(email, email_subject, email_message)

        # Log in the new user
        login_user(new_user, remember=True)

        flash('Account created successfully', category='success')
        
    
        return redirect(url_for('user.user_dashboard'))  

    return render_template("signup_page.html")

# Route for the login page
@user.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the login form has been submitted
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()

        # If the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Log in the user and remember the session
            login_user(user, remember=True)
            
            # Flash a success message
            flash('Logged in successfully', category='success')
            
            # Redirect the user to the user dashboard
            return redirect(url_for('user.user_dashboard'))
        else:
            # Flash an error message if login fails
            flash('Login failed. Check your email and password.', category='error')

    # Render the login page template
    return render_template("login_page.html")


# Route for the user dashboard
@user.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    # Renders the user dashboard template
    return render_template("user_dashboard.html")

# Route for the user reports page
@user.route('/reports', methods=['GET', 'POST'])
@login_required
def user_reports():
    # Fetch the Google Maps API key from the environment variable
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    # Handle form submission
    if request.method == 'POST':
        # Extract form data
        maintenance_issue = request.form.get('maintenance_issue')
        brief_description = request.form.get('brief-description')
        address = request.form.get('search_input')
        image_file = request.files.get('image-upload')

        # Check if any of the fields are empty
        if not all([maintenance_issue, brief_description, address, image_file]):
            flash('Please fill out all fields', 'error')
            return redirect(url_for('user.user_reports')) 

        # Check if the file format is allowed
        if image_file and not allowed_file(image_file.filename):
            flash('Invalid file format. Please upload a valid image (png, jpg, jpeg, gif)', 'error')
            return redirect(url_for('user.user_reports'))
        
        
        scottburgh_coordinates = (-30.28666, 30.75316) 
        user_coordinates = get_coordinates_from_address(address)

        #Check if User address is within Umdoni Municipality
        if not is_within_distance(user_coordinates, scottburgh_coordinates, 60):
            flash('This address is not in Umdoni Municipality', 'error')
            return redirect(url_for('user.user_reports'))
        # Upload the image to cloud storage
        if image_file:
            filename = secure_filename(f"{time.time()}_{image_file.filename}")
            image_url = upload_to_cloud_storage(bucket_name='fixit-bucket', filename=filename, file=image_file)


            # Create a new report using the Report model
            new_report = ReportedIssue(
                maintenance_issue=maintenance_issue,
                description=brief_description,
                picture=image_url,
                address=address,
                progress='Processing',
                maintenance_team='none',
                user_id=current_user.id
            )

            # Add the new report to the database
            db.session.add(new_report)
            db.session.commit()
            flash('Report submitted successfully', 'success')

            email=current_user.email
            phone_number=current_user.phone_number
            date_reported = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            email_subject = f"Maintenance Query Received - {maintenance_issue}"
            email_message=f'''
            Dear {current_user.name},


            Thank you for reporting a maintenance issue in Umdoni Municipality.
            Your report has been received, and we appreciate your effort in helping us maintain our community.
            Here are the details of your report:

            Report ID: {new_report.id}
            Issue: {brief_description}
            Report Adress: {new_report.id}
            Date Reported: {date_reported}

            Our dedicated team is now reviewing your report. 
            We understand the importance of addressing maintenance issues promptly and will keep you updated on the progress. 
            If you have additional details or concerns, please reply to this email. 

            Thank you for being an active participant in keeping Umdoni Municipality in good condition. 

           Have questions? Reach us at fixitumdoni@gmail.com. 

           Let's make Umdoni better together!

           Best,
           The FixIt Umdoni Team 🌟
           '''
            message_body=f'''
            Hello {current_user.name},

            Thank you for submitting a report. Your Report ID is {new_report.id}. 
            We've received your information and are actively reviewing the issue. 
            We'll keep you updated on the progress.  
            If you have questions, reply to this message.

            Fixit Umndoni 
            fixitumdoni@gmail.com
            '''
            
            send_email(email, email_subject, email_message)
            send_sms(phone_number, message_body)

            # Redirect the user to the dashboard after successful submission
            return redirect(url_for('user.user_dashboard'))  

    # Render the user report page with the Google Maps API key
    return render_template("user_report_page.html", google_maps_api_key=google_maps_api_key,user=current_user)


# Route for the tracking page
@user.route('/track')
@login_required
def tracking():
    # Query all reported issues associated with the current user
    report = ReportedIssue.query.filter_by(user_id=current_user.id).all()

    # Get the current user
    user = current_user

    # Render the tracking page with the list of reported issues and user information
    return render_template("tracking_page.html", report=report, user=user)

# Route for the user profile page
@user.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():

    if request.method == 'POST':
        # Get updated details from the form
        new_name = request.form.get('first_name')
        new_surname = request.form.get('surname')
        new_phone_number = request.form.get('phone_number')
        new_email = request.form.get('email_id')

                # Check if name and surname have more than 4 characters
        if len(new_name) < 5 or len(new_surname) < 5:
            flash('Name and surname must have at least 5 characters', category='error')
            return redirect(url_for('user.user_profile'))

        # Check if phone number is exactly 10 digits and consists of only numbers
        if not (new_phone_number.isdigit() and len(new_phone_number) == 10):
            flash('Phone number must be 10 digits and consist of only numbers',category='error')
            return redirect(url_for('user.user_profile'))

        #converts number to +27
        convert_number(new_phone_number)

        # Update user details in the database
        current_user.name = new_name
        current_user.surname = new_surname
        current_user.phone_number = new_phone_number
        current_user.email = new_email

        # Commit changes to the database
        db.session.commit()

        flash('Profile updated successfully', 'success')

    return render_template("user_profile.html",user = current_user)

# Route to log user out
@user.route('/logout')
@login_required
def logout():
    # Log out the current user using Flask-Login's logout_user function
    logout_user()

    # Redirect the user to the login page after successful logout
    return redirect(url_for('user.login'))
