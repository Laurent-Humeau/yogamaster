from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, TimeField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class YogaCourseForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    instructor = StringField('Instructor', validators=[DataRequired()])
    max_participants = IntegerField('Max Participants', validators=[DataRequired()])
    submit = SubmitField('Create Class')


class EditYogaCourseForm(FlaskForm):
    course_id = IntegerField('Course ID', validators=[DataRequired()], render_kw={"hidden": True})
    class_name = StringField('Class Name', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    instructor = StringField('Instructor', validators=[DataRequired()])
    max_participants = IntegerField('Max Participants', validators=[DataRequired()])
    submit = SubmitField('Update Class')


class AddYogaClassForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    instructor = StringField('Instructor', validators=[DataRequired()])
    max_participants = IntegerField('Max Participants', validators=[DataRequired()])
    submit = SubmitField('Add Class')

class BookClassForm(FlaskForm):
    course_id = HiddenField('Course ID')
    submit = SubmitField('Book Class')

class CancelClassForm(FlaskForm):
    course_id = HiddenField('Course ID')
    submit = SubmitField('Cancel Class')

class DeleteClass(FlaskForm):
    course_id = HiddenField('Course ID')
    submit = SubmitField('Delete Class')

