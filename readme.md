# Yoga Booking Web Application
This is a Yoga Booking web application built using Flask, SQLAlchemy, and Flask-Login. The application allows users to register, log in, book yoga classes, view available and past bookings, and cancel reservations. It also includes an admin interface where administrators can manage yoga classes (add, edit, delete), monitor bookings, and manage users.

## Features
### User Functionality
- **User Registration**: Users can register for an account with a unique username and password.
Login: Registered users can log in securely to access their dashboard.


- **Booking System**: Users can book available yoga classes, view upcoming and past bookings, and cancel their reservations.


- **Authentication & Authorization**: User authentication is managed with Flask-Login, and certain actions (like booking or cancelling classes) require users to be logged in.


- **CSRF Protection**: Forms are protected against cross-site request forgery attacks with flask-wtf.
Admin Functionality


- **Admin Dashboard**: Admin users have access to a special dashboard where they can manage all yoga classes.


- **Class Management**: Admins can:
    - Add new yoga classes
    - Edit existing yoga classes
    - Delete classes


- **User and Booking Management**: Admins can view who has booked specific classes and monitor participant counts.


- **Authentication & Authorization for Admins**: Admins are identified with a boolean flag (is_admin), and access to admin routes is restricted to users with admin privileges.


### Tech Stack
- Flask: Python web framework used to build the app
- Flask-Login: Used for user authentication
- Flask-WTF: Provides form handling and CSRF protection
- Flask-SQLAlchemy: Manages database interactions
- Flask-Migrate: Database migrations
- SQLite: Lightweight database used for storing data (can be switched to a more robust database like PostgreSQL or MySQL)
- Bootstrap: Frontend styling

