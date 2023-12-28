# Import Flask modules
from flask import Blueprint, render_template

# Create the admin blueprint
admin = Blueprint('admin', __name__)

# Define a route within the admin blueprint
@admin.route('/admin')
def admin_route():
    return render_template('admin-base.html')


@admin.route('/main')
def maintan():
    return render_template('maintenance_team.html')