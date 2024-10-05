from flask_wtf import FlaskForm
from wtforms import (TextAreaField, StringField, SubmitField, TelField, EmailField,
                      PasswordField, SelectField, DateField, RadioField, BooleanField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import Driver, Bus, app

class RegistrationForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    DOB = DateField(label='DOB', validators=[DataRequired()])
    physical_address = StringField(label='Physical Address', validators=[DataRequired()])
    email_address = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', 'password must match')])
    submit_btn = SubmitField('Register')


class LoginForm(FlaskForm):
    role = RadioField(label='Role', choices=[('Parent', 'Parent'), ('Admin', 'Administrator'), ('Teacher', 'Teacher')])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_btn = SubmitField('Login')


class StudentForm(FlaskForm):
    number = StringField('Student Number', validators=[DataRequired(), Length(min=8, max=8)])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    DOB = DateField(label='DOB', validators=[DataRequired()])
    physical_address = StringField(label='Physical Address', validators=[DataRequired()])
    email_address = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    bus_number = SelectField(label='Bus Number', validators=[DataRequired()])
    submit_btn = SubmitField('Add Student')

    def __init__(self):
        super(StudentForm, self).__init__()
        with app.app_context():
            # Fetch the updated list of drivers from the database
            self.bus_number.choices = [(bus.number, f'BUS #{bus.number}') for bus in Bus.query.all()]


class BusForm(FlaskForm):
    number = StringField('Bus Number', validators=[DataRequired(), Length(min=4, max=4)])
    schedule = TextAreaField('Schedule', validators=[DataRequired()])
    driver_id = SelectField(label='Driver ID', validators=[DataRequired()])
    submit_btn = SubmitField('Add Bus')

    def __init__(self):
        super(BusForm, self).__init__()
        with app.app_context():
            # Fetch the updated list of drivers from the database
            self.driver_id.choices = [(driver.id, f'#{driver.id} - {driver.first_name}') for driver in Driver.query.all()]


class DriverForm(FlaskForm):
    id = StringField(label='Driver ID', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    DOB = DateField(label='DOB', validators=[DataRequired()])
    physical_address = StringField(label='Physical Address', validators=[DataRequired()])
    email_address = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit_btn = SubmitField('Register')


class TeacherForm(FlaskForm):
    id = StringField(label='Teacher ID', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    DOB = DateField(label='DOB', validators=[DataRequired()])
    physical_address = StringField(label='Physical Address', validators=[DataRequired()])
    email_address = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit_btn = SubmitField('Register Teacher')


class ParentForm(FlaskForm):
    id = StringField(label='Parent ID', validators=[DataRequired()])
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    gender = SelectField(label='Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    DOB = DateField(label='DOB', validators=[DataRequired()])
    physical_address = StringField(label='Physical Address', validators=[DataRequired()])
    email_address = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    phone_number = TelField(label='Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit_btn = SubmitField('Register')

class ScannerForm(FlaskForm):
    id = StringField(label='Parent ID', validators=[DataRequired()])
    location = StringField(label='Location', validators=[DataRequired()])
    submit_btn = SubmitField('Add Scanner')