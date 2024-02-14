from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db
from sqlalchemy import TIMESTAMP,func


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    # Relationship with ReportedIssue
    reported_issues = db.relationship('ReportedIssue', backref='user', lazy=True)

# ReportedIssue model
class ReportedIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maintenance_issue = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(225), nullable=False)
    picture = db.Column(db.String(100))
    address = db.Column(db.String(255), nullable=False)
    progress = db.Column(db.String(255), nullable=False)
    date = db.Column(db.TIMESTAMP(timezone=True), default=func.now())
    maintenance_team= db.Column(db.String(100), nullable=False)


    # Foreign key to associate with User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class MaintenanceTeam(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    foreman_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)