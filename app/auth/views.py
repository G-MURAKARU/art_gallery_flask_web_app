from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from . import auth
from forms import RegistrationForm, LoginForm
from .. import db, bcrypt
from ..models import Customer


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(customerName=form.name.data, email=form.email.data, address=form.address.data, password=hashed_password)
        db.session.add(customer)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            next_page = request.args.get('next')
            if customer.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.homepage'))
            return redirect(next_page) if next_page else redirect(url_for('home.homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password.')
    return render_template('auth/login.html', title='Login', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('auth.login'))


# @auth.route("/account")
# @login_required
# def account():
#     return render_template('account.html', title='Account')
