from setup import db, app


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    DOB = db.Column(db.Date)
    physical_address = db.Column(db.String)
    email_address = db.Column(db.String)
    phone_number = db.Column(db.String)
    password = db.Column(db.String)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    DOB = db.Column(db.Date)
    physical_address = db.Column(db.String)
    email_address = db.Column(db.String)
    phone_number = db.Column(db.String)
    password = db.Column(db.String)


class Scanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    status = db.Column(db.String)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    DOB = db.Column(db.Date)
    physical_address = db.Column(db.String)
    email_address = db.Column(db.String)
    phone_number = db.Column(db.String)


class Bus(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    schedule = db.Column(db.String)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))


class Student(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    DOB = db.Column(db.Date)
    physical_address = db.Column(db.String)
    email_address = db.Column(db.String)
    phone_number = db.Column(db.String)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    bus_number = db.Column(db.Integer, db.ForeignKey('bus.number'))


class Scan(db.Model):
    scan_id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String, db.ForeignKey('student.number'))
    scanner_id = db.Column(db.Integer, db.ForeignKey('scanner.id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


class Class(db.Model):
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
    student_number = db.Column(db.String, db.ForeignKey('student.number'), primary_key=True)
    grade = db.Column(db.Integer)
    subject = db.Column(db.String)
    classroom = db.Column(db.String)

with app.app_context():
    db.create_all()
