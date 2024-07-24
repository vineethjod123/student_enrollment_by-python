from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Student, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Change this to a more secure key

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

def admin_required(f):
    def wrap(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # Fix for the endpoint name issue
    return wrap

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        name = request.form['name']
        age = int(request.form['age'])
        address = request.form['address']
        course = request.form['course']
        
        new_student = Student(student_id=student_id, name=name, age=age, address=address, course=course)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/view')
@admin_required
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students=students)

@app.route('/modify/<int:student_id>', methods=['GET', 'POST'])
@admin_required
def modify_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if request.method == 'POST':
        if student:
            new_student_id = request.form.get('student_id')
            name = request.form.get('name')
            age = request.form.get('age')
            address = request.form.get('address')
            course = request.form.get('course')

            if new_student_id:
                student.student_id = int(new_student_id)
            if name:
                student.name = name
            if age:
                student.age = int(age)
            if address:
                student.address = address
            if course:
                student.course = course
            
            db.session.commit()
            return redirect(url_for('view_students'))
    return render_template('modify_student.html', student=student)

@app.route('/search', methods=['GET', 'POST'])
@admin_required
def search_student():
    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        student = Student.query.filter_by(student_id=student_id).first()
        return render_template('student_details.html', student=student)
    return render_template('search_student.html')

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
