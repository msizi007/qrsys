from flask import Blueprint, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from models import Parent, Student, db
import json
from setup import session, request, gmail
import random

parent = Blueprint('parent', __name__)

@parent.route('/')
@parent.route('/index')
def index():
    return render_template('parent/index.html')

@parent.route('/students_log')
def students_log():
    return render_template('parent/students_log.html')

@parent.route('/student_history')
def student_history():
    return render_template('parent/student_history.html')


@parent.route('/notifications')
def notifications():
    return render_template('parent/notifications.html')

@parent.route('/link_student', methods=['GET', 'POST'])
def link_student():
    if request.method == 'POST':
        # Handle form submission and link the parent to a student
        student_num = request.form.get('studentNumber')
        child_email = request.form.get('childEmail')
        student = Student.query.get(student_num)

        if student:
            if student.email_address == child_email:
                # generate 6 random numbers as OTP
                OTP_code = ''
                OTP_code = ''.join([str(random.randint(0, 10)) for _ in range(6)])
                gmail.send(child_email, 'Parental Account Link', f"""
Dear {student.first_name}
                           
Your OPT code is {OTP_code}. Do not share this with anyone, as it can give away your account to someone else. Only your parent should receive this
""")
                session['otp_code'] = OTP_code
                session['linked_student_number'] = student.number
                return redirect(url_for('parent.verify_student'))
            else:
                flash('Not a valid email address. Check the account and try again later.', 'danger')
        else:
            flash('No student found with the provided student number.', 'danger')
    return render_template('parent/link_student.html')


@parent.route('/verify_student', methods=['GET', 'POST'])
def verify_student():
    if request.method == 'POST':
        
        # Handle form submission and verify the OTP code
        OTP_code = request.form.get('OTP')
        print(session.get('otp_code'), OTP_code, session.get('otp_code')==OTP_code)
        if OTP_code == session.get('otp_code'):
            student = Student.query.get(session.get('linked_student_number'))
            student.parent_id = session.get('parent_id')
            db.session.commit()
            flash(f'Sucess: {student.number} linked sucessfully!', 'success')
            return redirect(url_for('parent.index'))
        else:
            flash('Invalid OTP code. Please try again.', 'danger')
    return render_template('parent/verify_student.html')

@parent.route('/settings')
def settings():
    return render_template('parent/settings.html')
