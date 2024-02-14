# Import Flask modules
from flask import Blueprint, render_template,request, flash
import random
import string
from .notifications import send_email
from werkzeug.security import generate_password_hash, check_password_hash

# Import database-related modules
from .database import db, User, ReportedIssue,MaintenanceTeam

# Create the admin blueprint
admin = Blueprint('admin', __name__)

def calculate_number_of_users():
    """Calculate the number of users in the database."""
    return User.query.count()

def count_in_progress_issues():
    """Count the number of reported issues in progress."""
    return ReportedIssue.query.filter_by(progress='in progress').count()

def count_finished_issues():
    """Count the number of reported issues that are finished."""
    return ReportedIssue.query.filter_by(progress='finished').count()

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(12))
    return password

# Define a route within the admin blueprint
@admin.route('/admin')
def admin_route():
    """Render the admin page."""
    num_users = calculate_number_of_users()
    num_in_progress_issues = count_in_progress_issues()
    num_in_finished_issues = count_finished_issues()
    users = User.query.all()
    
    reported_issues = ReportedIssue.query.all()
    return render_template('admin-base.html', users=users, num_in_finished_issues=num_in_finished_issues, reported_issues=reported_issues, num_users=num_users, num_in_progress_issues=num_in_progress_issues)

@admin.route('/maintenance-team', methods=['GET', 'POST'])
def maintenance_team():
    num_users = calculate_number_of_users()
    num_in_progress_issues = count_in_progress_issues()
    num_in_finished_issues = count_finished_issues()
    maintenance_Team=MaintenanceTeam.query.all()
    
    if request.method == 'POST':
        foreman = request.form.get('foreman')
        email = request.form.get('email')
        phone_number = request.form.get('number')
        department = request.form.get('department')

        # Generate a strong password
        password = generate_password()
        
        # Hash the password before saving to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if any field is empty
        if not all([foreman, email, phone_number, department]):
            flash('Please fill out all fields', category= 'error')
        

        new_team = MaintenanceTeam(email=email, phone_number=phone_number, password=hashed_password, foreman_name=foreman, department=department)
        db.session.add(new_team)
        db.session.commit()
        flash('Team added successfully', category='success')
        
        email_subject = "FixIt Umdoni Foreman Login Details"
        email_message = f'''
        Dear {foreman},
        Your account has been successfully created.
        Email: {email}
        Password: {password}
        Please use these credentials to log in.
        Regards,
        The Maintenance Team
        '''
        send_email(email, email_subject, email_message)
        
    return render_template('maintenance_team.html', num_users=num_users,maintenance_Team=maintenance_Team,num_in_progress_issues=num_in_progress_issues,num_in_finished_issues=num_in_finished_issues)

@admin.route('/maintenance-queries')
def maintenance_queries():
    """Render the maintenance queries page."""
    return render_template('maintenance_queries.html')

@admin.route('/maintenance-users')
def maintenance_users():
    """Render the maintenance users page."""
    return render_template('maintenance_users.html')
