from flask import Blueprint, render_template

user = Blueprint('user',__name__)

# Route for the home page
@user.route('/')
def home():
    # Render the home page template
    return render_template("home_page.html")

# Route for the login page
@user.route('/login', methods=['GET', 'POST'])
def login():
    # Render the login page template
    return render_template("login_page.html")

# Route for the signup page
@user.route('/signup', methods=['GET', 'POST'])
def signup():
    # Render the signup page template
    return render_template("signup_page.html")
# Route for the signup page
@user.route('/user', methods=['GET', 'POST'])
def userpage():
    # Render the signup page template
    return render_template("user_dashboard.html")

@user.route('/dash', methods=['GET', 'POST'])
def dash():
    # Render the signup page template
    return render_template("user_report_page.html")
