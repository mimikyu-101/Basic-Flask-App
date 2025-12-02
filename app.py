from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

# Initialize Flask application
app = Flask(__name__)
Bcrypt = Bcrypt(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages
# Session and cookie security settings
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Mitigate CSRF

# Initialize database
db = SQLAlchemy(app)


# Database Model
class Employee(db.Model):
    """
    Employee model for storing employee information.
    
    Attributes:
        id: Primary key, auto-incremented
        first_name: Employee's first name
        last_name: Employee's last name
        email: Employee's email address (unique)
        phone: Employee's phone number
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, first_name, last_name, email, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password_hash = Bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        """String representation of Employee object"""
        return f"{self.id} - {self.first_name}"
    
class EmployeeForm(FlaskForm):
    """
    Form for creating and updating Employee records.
    
    Fields:
        first_name: Employee's first name
        last_name: Employee's last name
        email: Employee's email address
        phone: Employee's phone number
        submit: Submit button
    """
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100), Regexp(r'^[A-Za-z\s\-]+$', message="First name must contain only letters, spaces, or hyphens.")])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100), Regexp(r'^[A-Za-z\s\-]+$', message="Last name must contain only letters, spaces, or hyphens.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20), Regexp(r'^\+?[0-9\s]+$', message="Phone number must contain only numbers, spaces, or an optional leading +.")])
    password = StringField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField('Submit')


# Routes
# Custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Homepage route - displays all employees and handles new employee creation.
    
    GET: Display all employees in a table with a form to add new ones
    POST: Add a new employee to the database
    """
    form = EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get form data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data

            # Check if email already exists
            existing_employee = Employee.query.filter_by(email=email).first()
            if existing_employee:
                flash('An employee with this email already exists!', 'warning')
                return redirect(url_for('index'))

            # Create new employee
            try:
                new_employee = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    password=password
                )
                db.session.add(new_employee)
                db.session.commit()
                flash('Employee added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding employee: {str(e)}', 'danger')

            return redirect(url_for('index'))
        else:
            # Validation failed, re-render form with errors
            employees = Employee.query.all()
            return render_template("index.html", employees=employees, form=form)

    # GET request - display all employees
    employees = Employee.query.all()
    return render_template("index.html", employees=employees, form=form)


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    """
    Update employee route - displays form to edit employee and handles updates.
    
    Args:
        id: Employee ID to update
    
    GET: Display form pre-filled with employee data
    POST: Update employee information in database
    """
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get updated form data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone = form.phone.data

            # Validate form data
            if not all([first_name, last_name, email, phone]):
                flash('All fields are required!', 'danger')
                return redirect(url_for('update', id=id))

            # Check if email is being changed to one that already exists
            if email != employee.email:
                existing_employee = Employee.query.filter_by(email=email).first()
                if existing_employee:
                    flash('An employee with this email already exists!', 'warning')
                    return redirect(url_for('update', id=id))
        
            # Update employee
            try:
                employee.first_name = first_name
                employee.last_name = last_name
                employee.email = email
                employee.phone = phone
                db.session.commit()
                flash('Employee updated successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating employee: {str(e)}', 'danger')
                return redirect(url_for('update', id=id))
    
    # GET request - display update form
    return render_template("update.html", employee=employee, form=form)


@app.route("/delete/<int:id>")
def delete(id):
    """
    Delete employee route - removes employee from database.
    
    Args:
        id: Employee ID to delete
    """
    employee = Employee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        flash(f'Employee {employee.first_name} {employee.last_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'danger')
    
    return redirect(url_for('index'))


# Initialize database
def init_db():
    """
    Initialize the database by creating all tables.
    Run this function once to set up the database.
    
    Usage from Python shell:
        >>> from app import app, db
        >>> with app.app_context():
        ...     db.create_all()
    """
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        # Ensure session is permanent for all users
        from flask import session
        @app.before_request
        def make_session_permanent():
            session.permanent = True
    # Run the application in debug mode
    app.run(debug=True)
    # changes added manually for push conflict

