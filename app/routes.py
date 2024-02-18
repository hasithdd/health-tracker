from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect already logged-in users

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    health_data = HealthData.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', health_data=health_data)

@app.route('/input_data', methods=['GET', 'POST'])
@login_required
def input_data():
    form = InputDataForm()
    if form.validate_on_submit():
        health_data = HealthData(steps=form.steps.data, sleep_hours=form.sleep_hours.data,
                                 heart_rate=form.heart_rate.data, user_id=current_user.id)
        db.session.add(health_data)
        db.session.commit()
        flash('Health data recorded successfully!')
        return redirect(url_for('input_data'))
    return render_template('input_data.html', title='Input Data', form=form)

@app.route('/goal_settings', methods=['GET', 'POST'])
@login_required
def goal_settings():
    form = GoalSettingsForm()
    if form.validate_on_submit():
        # Process goal settings form
        flash('Goals updated successfully!')
        return redirect(url_for('goal_settings'))
    return render_template('goal_settings.html', title='Goal Settings', form=form)
