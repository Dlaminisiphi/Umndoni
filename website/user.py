# Import Flask modules
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

# Import database-related modules
from .database import db, User, ReportedIssue

# Import Time
import time

# Import security-related modules
from werkzeug.security import generate_password_hash, check_password_hash

# Import notification-related modules
from .notifications import send_email, send_sms

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

    return render_template("home_page.html")

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
        login_user(new_user)

        flash('Account created successfully', category='success')
    
        return redirect(url_for('user.user_dashboard'))  

    return render_template("signup_page.html")

# Route for the login page
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Log in the user
            login_user(user)

            flash('Logged in successfully', category='success')
            
            return redirect(url_for('user.user_dashboard'))
        else:
            flash('Login failed. Check your email and password.', category='error')

    return render_template("login_page.html")

# Route for the user dashboard
@user.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():

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
                user_id=current_user.id
            )

            # Add the new report to the database
            db.session.add(new_report)
            db.session.commit()
            flash('Report submitted successfully', 'success')

            # Redirect the user to the dashboard after successful submission
            return redirect(url_for('user.user_dashboard'))  

    # Render the user report page with the Google Maps API key
    return render_template("user_report_page.html", google_maps_api_key=google_maps_api_key)


# Route for the tracking page
@user.route('/track')
@login_required
def tracking():

    return render_template("tracking_page.html")

# Route for the user profile page
@user.route('/profile')
@login_required
def user_profile():

    return render_template("user_profile.html")

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))
