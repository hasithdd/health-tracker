from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import InputDataForm, GoalSettingsForm
from app.models import HealthData

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
