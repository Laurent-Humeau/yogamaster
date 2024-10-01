from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_migrate import Migrate
from forms import RegistrationForm, AddYogaClassForm, EditYogaCourseForm, LoginForm, BookClassForm, CancelClassForm, DeleteClass
from flask_wtf import CSRFProtect
import config


# App settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yoga.db'
app.config['SECRET_KEY'] = config.secret_key
db = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


# Models
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password = db.Column(db.String(length=100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Many-to-many relationship with YogaCourse
    booked_classes = db.relationship('YogaCourse', secondary='bookings',
                                     backref=db.backref('booked_users', lazy='dynamic'))


# YogaCourse model
class YogaCourse(db.Model):
    __tablename__ = 'yogacourse'  # Explicitly define table name
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False, default=0)
    current_participants = db.Column(db.Integer, nullable=False, default=0)


#  many-to-many relationship between User and YogaCourse
bookings = db.Table('bookings',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                    db.Column('course_id', db.Integer, db.ForeignKey('yogacourse.id'), primary_key=True)
                    )

# Routes

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password, please try again.', category='danger')

    return render_template('user/index.html', form=form)




@app.route("/learn_more_beginner")
def learn_more_beginner():
    return render_template('user/learn_more_beginner.html')

@app.route("/learn_more_intermediate")
def learn_more_intermediate():
    return render_template('user/learn_more_intermediate.html')

@app.route("/learn_more_meditation")
def learn_more_meditation():
    return render_template('user/learn_more_meditation.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        confirm_password = form.confirm_password.data


        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', category='danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', category='success')
        return redirect(url_for('login'))

    return render_template("user/register.html", form=form)


@app.route("/dashboard", methods=['GET'])
@login_required
def user_dashboard():
    now = datetime.datetime.now().date()

    upcoming_classes = YogaCourse.query.join(bookings).filter(
        bookings.c.user_id == current_user.id,
        YogaCourse.date >= now
    ).all()

    available_classes = YogaCourse.query.filter(
        YogaCourse.date >= now
    ).all()

    past_booked_classes = YogaCourse.query.join(bookings).filter(
        bookings.c.user_id == current_user.id,
        YogaCourse.date < now
    ).all()

    # Sort by date
    upcoming_classes = sorted(upcoming_classes, key=lambda x: x.date)
    available_classes = sorted(available_classes, key=lambda x: x.date)
    past_booked_classes = sorted(past_booked_classes, key=lambda x: x.date)

    book_class_form = BookClassForm()
    cancel_class_form = CancelClassForm()

    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('user/dashboard.html',
                           upcoming_classes=upcoming_classes,
                           user=current_user,
                           available_classes=available_classes, past_booked_classes=past_booked_classes, book_class_form=book_class_form, cancel_class_form=cancel_class_form)


@app.route("/book_class", methods=['POST'])
@login_required
def book_class():
    form = BookClassForm()

    if form.validate_on_submit():
        course_id = form.course_id.data
        class_to_book = YogaCourse.query.get(course_id)

        if class_to_book:
            if class_to_book.current_participants < class_to_book.max_participants:
                if class_to_book not in current_user.booked_classes:
                    current_user.booked_classes.append(class_to_book)
                    class_to_book.current_participants += 1
                    class_to_book.max_participants -= 1
                    db.session.commit()
                    flash('Booking confirmed!', category='success')
                    return redirect(url_for('user_dashboard'))
                else:
                    flash('You have already booked this class.', category='warning')
            else:
                flash('Class is fully booked.', category='warning')
        else:
            flash('Class not found.', category='danger')

    return redirect(url_for('user_dashboard'))



@app.route("/cancel_booking", methods=['POST'])
@login_required
def cancel_booking():
    form = CancelClassForm()
    if form.validate_on_submit():
        course_id = request.form.get('course_id')
        class_to_cancel = YogaCourse.query.filter_by(id=course_id).first()

        if class_to_cancel and class_to_cancel in current_user.booked_classes:
            current_user.booked_classes.remove(class_to_cancel)
            class_to_cancel.current_participants -= 1
            class_to_cancel.max_participants += 1
            db.session.commit()
            flash('Booking canceled successfully!', category='success')
        else:
            flash('Cancellation failed. Class might not be booked or doesn\'t exist.', category='danger')

    return redirect(url_for('user_dashboard'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('login'))


# master yoda is admin login and pwd
@app.route('/admin/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    edit_form = EditYogaCourseForm()
    add_form = AddYogaClassForm()
    delete_form = DeleteClass()

    courses = YogaCourse.query.all()
    courses = sorted(courses, key=lambda x: x.date, reverse=True)

    return render_template('admin/admin_dashboard.html', courses=courses, edit_form=edit_form, add_form=add_form, delete_form=delete_form)


@app.route('/admin/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if not current_user.is_admin:
        abort(403)

    form = AddYogaClassForm()

    if form.validate_on_submit():

        new_class = YogaCourse(
            class_name=form.class_name.data,
            date=form.date.data,
            time=form.time.data,
            instructor=form.instructor.data,
            max_participants=form.max_participants.data
        )


        db.session.add(new_class)
        db.session.commit()

        flash('Class added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    edit_form = EditYogaCourseForm()
    delete_form = DeleteClass()
    return render_template('admin/admin_dashboard.html', form=form, edit_form=edit_form, delete_form=delete_form)


@app.route('/includes/edit_modal', methods=['GET', 'POST'])
@login_required
def edit_class():
    if not current_user.is_admin:
        abort(403)

    course_id = request.form.get('course_id') or request.args.get('course_id')
    course = YogaCourse.query.get(course_id)

    if not course:
        flash("Course not found.", "danger")
        return redirect(url_for('admin_dashboard'))

    form = EditYogaCourseForm(obj=course)

    if form.validate_on_submit():


        try:
            course.class_name = form.class_name.data
            course.date = form.date.data
            course.time = form.time.data
            course.instructor = form.instructor.data
            course.max_participants = form.max_participants.data
            db.session.commit()
            flash("Class updated successfully!", "success")
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for('admin_dashboard'))


    add_form = AddYogaClassForm()
    delete_form = DeleteClass()
    return render_template('includes/edit_modal.html', form=form, course=course, edit_form=form, add_form=add_form, delete_form=delete_form)




@app.route('/admin/delete_class', methods=['POST'])
@login_required
def delete_class():
    if not current_user.is_admin:  # Check if the user is an admin
        abort(403)  # Forbid access if not an admin

    if request.method == 'POST':
        # Get the course ID from the form
        course_id = request.form.get('course_id')

        # Fetch the course from the database
        course = YogaCourse.query.get(course_id)

        if not course:
            flash("Course not found.", "danger")
            return redirect(url_for('admin_dashboard'))  # Redirect if course not found

        form = DeleteClass()  # Instantiate the delete form
        if form.validate_on_submit():
            try:
                # Delete the course from the database
                db.session.delete(course)

                # Commit changes to the database
                db.session.commit()

                flash("Class deleted successfully!", "success")
            except Exception as e:
                db.session.rollback()  # Rollback in case of any errors
                flash(f"An error occurred while deleting the class: {str(e)}", "danger")

            return redirect(url_for('admin_dashboard'))  # Redirect after processing the form
    add_form = AddYogaClassForm()
    edit_form = EditYogaCourseForm()
    return render_template('includes/delete_modal.html', form=form, course=course, add_form=add_form, edit_form=edit_form)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
