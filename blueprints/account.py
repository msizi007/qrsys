from flask import Blueprint, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from models import Parent, db
import json
from setup import session, request, gmail
import random
from string import ascii_uppercase

account = Blueprint('account', __name__)
ALPHA_NUMERICS = 'A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0,1,2,3,4,5,6,7,8,9'.split(',')

@account.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.validate_on_submit(), form.errors)
    if form.validate_on_submit():
        existing_email = Parent.query.filter_by(email_address=form.email_address.data).first()
        if existing_email:
            flash('Email already exists!', 'danger')
            return redirect(url_for('account.register'))

        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('account.register'))

        new_parent = Parent(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            DOB=form.DOB.data,
            physical_address=form.physical_address.data,
            email_address=form.email_address.data,
            phone_number=form.phone_number.data,
            password=form.password.data
        )

        db.session.add(new_parent)
        db.session.commit()

        flash('Registration Successful!', 'success')
        return redirect(url_for('account.login'))
    else:
        for _, msg in form.errors.items():
            flash(msg[0], 'danger')
    return render_template('account/register.html', form=form)


@account.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == 'Parent':
            parent = Parent.query.filter_by(email_address=form.email_address.data).first()
            if parent:
                # Check if the provided password matches the hashed password in the database
                if form.password.data == parent.password:
                    flash('Login successful!', 'success')
                    session.permanet = True
                    session['parent_id'] = parent.id
                    return redirect(url_for('parent.index'))
                else:
                    flash('Invalid email or password. Please try again.', 'danger')
            else:
                flash('No user found, with the provided email address', 'danger')
            return render_template('account/login.html', form=form)
        if form.role.data == 'Admin':
            admin = None
            with open('admin.json', 'r') as file:
                data = json.load(file)

            email_address, password = data.get('email_address'), data.get('password')

            if form.email_address.data == email_address and form.password.data == password:
                session.permanent = True
                session['Active'] = True
                flash('Login successful!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
    else:
        for _, msg in form.errors.items():
            flash(msg[0], 'danger')

    return render_template('account/login.html', form=form)

@account.route('/fogort_password', methods=['GET', 'POST'])
def fogort_password():
    if request.method == 'POST':
        email = request.form.get('email')
        valid_user = Parent.query.filter_by(email_address=email).first()
        if valid_user:
            # Send email with password reset link
            new_password = ''.join([random.choice(ALPHA_NUMERICS) for x in range(8)])
            gmail.send(email, 'Password Reset', f"Your new password: {new_password}")
            valid_user.password = new_password
            db.session.commit()
            flash('Password reset has been sent to your email address.', 'success')
            return redirect(url_for('account.login'))
        else:
            flash('No user found with the provided email address.', 'danger')
            
    return render_template('account/fogort_password.html')
