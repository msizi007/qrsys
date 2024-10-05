from flask import Blueprint, render_template, flash, redirect, url_for, request
from forms import StudentForm, BusForm, DriverForm, TeacherForm, ParentForm, ScannerForm
from models import Student, Bus, Driver, Teacher, Parent, Scanner, Scan, db
from setup import session, app
from scanner import  Scanner as ScannerObj
from threading import Thread

admin = Blueprint('admin', __name__)
with app.app_context():
    SCANNER = ScannerObj(None)

@admin.route('/dashboard')
def dashboard():
    students_count = len(Student.query.all())
    buses_count = len(Bus.query.all())
    drivers_count = len(Driver.query.all())
    parents_count = len(Parent.query.all())
    teachers_count = len(Teacher.query.all())
    scanners_count = len(Scanner.query.all())
    return render_template('admin/dashboard.html',
                            students_count=students_count,
                            buses_count=buses_count,
                            drivers_count=drivers_count,
                            parents_count=parents_count,
                            teachers_count=teachers_count,
                            scanners_count=scanners_count)


@admin.route('/students')
def students():
    students_data = Student.query.all()
    return render_template('admin/students.html', students=students_data)


@admin.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        # Handle form submission and save the student to the database
        new_student = Student(
            number=form.number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            DOB=form.DOB.data,
            physical_address=form.physical_address.data,
            email_address=form.email_address.data,
            phone_number=form.phone_number.data,
        )
        db.session.add(new_student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('admin.students'))

    return render_template('admin/add_student.html', form=form)


@admin.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        # Handle form submission and update the student in the database
        student.number = form.number.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.DOB = form.DOB.data
        student.physical_address = form.physical_address.data
        student.email_address = form.email_address.data
        student.phone_number = form.phone_number.data

        db.session.commit()

        flash(f'Student @{student.number} updated successfully!', 'success')
        return redirect(url_for('admin.students'))
    print(form.errors)
    return render_template('admin/edit_student.html', form=form, student=student)


@admin.route('/confirm_delete_student/<int:student_id>', methods=['POST'])
def confirm_delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        return render_template('admin/confirm_delete.html', student=student)


@admin.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting student. Please try again.', 'danger')

    return redirect(url_for('admin.students'))


@admin.route('/buses')
def buses():
    buses_data = Bus.query.all()
    return render_template('admin/buses.html', buses=buses_data)


@admin.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    form = BusForm()
    all_drivers = Driver.query.all()
    print([driver.id for driver in all_drivers])
    if form.validate_on_submit():
        # Handle form submission and save the buses to the database
        new_bus = Bus(
            number=form.number.data,
            schedule=form.schedule.data,
            driver_id=form.driver_id.data
        )
        db.session.add(new_bus)
        db.session.commit()

        flash('Bus added successfully!', 'success')
        return redirect(url_for('admin.buses'))

    return render_template('admin/add_bus.html', form=form)


@admin.route('/edit_bus/<int:bus_number>', methods=['GET', 'POST'])
def edit_bus(bus_number):
    bus = Bus.query.get_or_404(bus_number)
    form = BusForm(obj=bus)
    if form.validate_on_submit():
        # Handle form submission and update the bus in the database
        bus.number = form.number.data
        bus.schedule = form.schedule.data
        bus.driver_id = form.driver_id.data

        db.session.commit()

        flash(f'Bus @{bus.number} updated successfully!', 'success')
        return redirect(url_for('admin.buses'))

    return render_template('admin/edit_bus.html', form=form, bus=bus)


@admin.route('/delete_bus/<int:bus_number>', methods=['GET', 'POST'])
def delete_bus(bus_number):
    bus = Student.query.get_or_404(bus_number)
    db.session.delete(bus)
    db.session.commit()

    flash('Bus deleted successfully!', 'success')
    return redirect(url_for('admin.buses'))


@admin.route('/drivers')
def drivers():
    drivers_data = Driver.query.all()
    return render_template('admin/drivers.html', drivers=drivers_data)


@admin.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    form = DriverForm()
    if form.validate_on_submit():
        # Handle form submission and save the driver to the database
        driver = Driver(
            id=form.id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            DOB=form.DOB.data,
            physical_address=form.physical_address.data,
            email_address=form.email_address.data,
            phone_number=form.phone_number.data,
        )
        db.session.add(driver)
        db.session.commit()

        flash('Driver added successfully!', 'success')
        return redirect(url_for('admin.drivers'))

    return render_template('admin/add_driver.html', form=form)


@admin.route('/edit_driver/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    driver = Driver.query.get(driver_id)
    form = DriverForm(obj=driver)
    if form.validate_on_submit():
        # Handle form submission and update the driver in the database
        driver.id = form.id.data
        driver.first_name = form.first_name.data
        driver.last_name = form.last_name.data
        driver.gender = form.gender.data
        driver.DOB = form.DOB.data
        driver.physical_address = form.physical_address.data
        driver.email_address = form.email_address.data
        driver.phone_number = form.phone_number.data

        db.session.commit()

        flash(f'Driver @{driver.id} updated successfully!', 'success')
        return redirect(url_for('admin.drivers'))

    return render_template('admin/edit_driver.html', form=form, driver=driver)


@admin.route('/delete_driver/<int:driver_id>', methods=['GET', 'POST'])
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()

    flash('Driver deleted successfully!', 'success')
    return redirect(url_for('admin.drivers'))


@admin.route('/teachers')
def teachers():
    teachers_data = Teacher.query.all()
    return render_template('admin/teachers.html', teachers=teachers_data)


@admin.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        # Handle form submission and save the teacher to the database
        teacher = Teacher(
            id=form.id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            DOB=form.DOB.data,
            physical_address=form.physical_address.data,
            email_address=form.email_address.data,
            phone_number=form.phone_number.data,
        )
        db.session.add(teacher)
        db.session.commit()

        flash('Teacher added successfully!', 'success')
        return redirect(url_for('admin.teachers'))

    return render_template('admin/add_teacher.html', form=form)


@admin.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    form = TeacherForm(obj=teacher)
    if form.validate_on_submit():
        # Handle form submission and update the teacher in the database
        teacher.id = form.id.data
        teacher.first_name = form.first_name.data
        teacher.last_name = form.last_name.data
        teacher.gender = form.gender.data
        teacher.DOB = form.DOB.data
        teacher.physical_address = form.physical_address.data
        teacher.email_address = form.email_address.data
        teacher.phone_number = form.phone_number.data

        db.session.commit()

        flash(f'Teacher @{teacher.id} updated successfully!', 'success')
        return redirect(url_for('admin.teachers'))

    return render_template('admin/edit_teacher.html', form=form, teacher=teacher)


@admin.route('/delete_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()

    flash('Driver deleted successfully!', 'success')
    return redirect(url_for('admin.teachers'))


@admin.route('/parents')
def parents():
    parents_data = Parent.query.all()
    return render_template('admin/parents.html', parents=parents_data)


@admin.route('/add_parent', methods=['GET', 'POST'])
def add_parent():
    form = ParentForm()
    if form.validate_on_submit():
        # Handle form submission and save the parent to the database
        parent = Teacher(
            id=form.id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            DOB=form.DOB.data,
            physical_address=form.physical_address.data,
            email_address=form.email_address.data,
            phone_number=form.phone_number.data,
        )
        db.session.add(parent)
        db.session.commit()

        flash('Parent added successfully!', 'success')
        return redirect(url_for('admin.parents'))

    return render_template('admin/add_parent.html', form=form)


@admin.route('/edit_parent/<int:parent_id>', methods=['GET', 'POST'])
def edit_parent(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    form = ParentForm(obj=parent)
    if form.validate_on_submit():
        # Handle form submission and update the parent in the database
        parent.id = form.id.data
        parent.first_name = form.first_name.data
        parent.last_name = form.last_name.data
        parent.gender = form.gender.data
        parent.DOB = form.DOB.data
        parent.physical_address = form.physical_address.data
        parent.email_address = form.email_address.data
        parent.phone_number = form.phone_number.data

        db.session.commit()

        flash(f'Parent @{parent.id} updated successfully!', 'success')
        return redirect(url_for('admin.parents'))

    return render_template('admin/edit_parent.html', form=form, parent=parent)


@admin.route('/delete_parent/<int:parent_id>', methods=['GET', 'POST'])
def delete_parent(parent_id):
    parent = Teacher.query.get_or_404(parent_id)
    db.session.delete(parent)
    db.session.commit()

    flash('Driver deleted successfully!', 'success')
    return redirect(url_for('admin.parents'))

@admin.route('/classes')
def classes():
    pass


@admin.route('/logs')
def logs():
    pass

@admin.route('/scanners')
def scanners():
    scanners_data = Scanner.query.all()
    return render_template('admin/scanners.html', scanners=scanners_data)

@admin.route('/add_scanner', methods=['GET', 'POST'])
def add_scanner():
    form = ScannerForm()
    if form.validate_on_submit():
        # Handle form submission and save the scanner to the database
        scanner = Scanner(
            id=form.id.data,
            location=form.location.data,
            status='0'
        )
        db.session.add(scanner)
        db.session.commit()

        flash('scanner added successfully!', 'success')
        return redirect(url_for('admin.scanners'))
    
    return render_template('admin/add_scanner.html', form=form)


@admin.route('/edit_scanner/<int:scanner_id>', methods=['GET', 'POST'])
def edit_scanner(scanner_id):
    scanner = scanner.query.get_or_404(scanner_id)
    form = ScannerForm(obj=scanner)
    if form.validate_on_submit():
        # Handle form submission and update the scanner in the database
        scanner.id = form.id.data
        scanner.location = form.first_name.data
        scanner.status = form.last_name.data

        db.session.commit()

        flash(f'scanner @{scanner.id} updated successfully!', 'success')
        return redirect(url_for('admin.scanners'))

    return render_template('admin/edit_scanner.html', form=form, scanner=scanner)


@admin.route('/delete_scanner/<int:scanner_id>', methods=['GET', 'POST'])
def delete_scanner(scanner_id):
    scanner = Scanner.query.get_or_404(scanner_id)
    db.session.delete(scanner)
    db.session.commit()

    flash('Driver deleted successfully!', 'success')
    return redirect(url_for('admin.scanners'))


@admin.route('/activate_scanner/<int:scanner_id>', methods=['GET', 'POST'])
def activate_scanner(scanner_id):
    global SCANNER
    scanner = Scanner.query.get_or_404(scanner_id)
    scanner.status = '1'
    db.session.commit()
    with app.app_context():
            SCANNER = ScannerObj(scanner_id)
    return render_template('admin/activate_scanner.html', scanner_id=scanner_id)


@admin.route('/activated_scanner')
def activated_scanner():

    scanner_thread = Thread(target=SCANNER.activate)
    scanner_thread.start()

    return redirect(url_for('admin.scanners'))


@admin.route('/deactivate_scanner/<int:scanner_id>', methods=['GET', 'POST'])
def deactivate_scanner(scanner_id):
    scanner = Scanner.query.get_or_404(scanner_id)
    scanner.status = '0'
    db.session.commit()

    return render_template('admin/deactivate_scanner.html', scanner_id=scanner_id)      


@admin.route('/deactivated_scanner')
def deactivated_scanner():
    def activate(): 
        
        SCANNER.deactivate()

    scanner_thread = Thread(target=activate)
    scanner_thread.start()

    return redirect(url_for('admin.scanners'))