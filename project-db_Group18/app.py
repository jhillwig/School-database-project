from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import config
 
# Configuration for pymysql
db = config.dbserver
 
app = Flask(__name__)
app.secret_key = 'university_portal_secret_key_2025'
app.debug = True
 
# ─────────────────────────────────────────────────────────────
# DB HELPER
# ─────────────────────────────────────────────────────────────
def get_cursor():
    global db
    try:
        db.ping(reconnect=True)
    except Exception:
        db = config.dbserver
    return db.cursor(pymysql.cursors.DictCursor)
 
# ─────────────────────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────────────────────
def logged_in():
    return 'user_id' in session
 
def is_role(role):
    return session.get('role') == role
 
def admin_required():
    if not logged_in() or not is_role('admin'):
        return redirect(url_for('login'))
    return None
 
def instructor_required():
    if not logged_in() or not is_role('instructor'):
        return redirect(url_for('login'))
    return None
 
def student_required():
    if not logged_in() or not is_role('student'):
        return redirect(url_for('login'))
    return None
 
# ─────────────────────────────────────────────────────────────
# LOGIN / LOGOUT
# ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if logged_in():
        role = session.get('role')
        if role == 'admin':      return redirect(url_for('adminDashboard'))
        if role == 'instructor': return redirect(url_for('instructorDashboard'))
        if role == 'student':    return redirect(url_for('studentDashboard'))
    return redirect(url_for('login'))
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('index.html')
 
    username = request.form['username']
    password = request.form['password']
    cursor = get_cursor()
    
    # ---- ADMIN ----
    try:
        cursor.execute("SELECT * FROM Admin WHERE name=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
    except pymysql.Error as e:
        print(e); admin = None

    if admin:
        session["role"] = 'admin'
        session["user"] = admin['name']
        session["username"] = admin['name']
        session["user_id"] = admin['a_ID']
        cursor.close()
        return redirect(url_for('adminDashboard'))
    

    # ---- INSTRUCTOR ----
    try:
        cursor.execute("SELECT * FROM Instructor WHERE name=%s AND password=%s", (username, password))
        instructor = cursor.fetchone()
    except pymysql.Error as e:
        print(e); instructor = None

    if instructor:
        session["role"] = 'instructor'
        session["user"] = instructor['name']
        session["username"] = instructor['name']
        session["user_id"] = instructor['i_ID']
        cursor.close()
        return redirect(url_for('instructorDashboard'))
    

    # ---- Student ----
    try:
        cursor.execute("SELECT * FROM Student WHERE name=%s AND password=%s", (username, password))
        student = cursor.fetchone()
    except pymysql.Error as e:
        print(e); student = None    

    cursor.close()

    if student:
        session["role"] = 'student'
        session["user"] = student['name']
        session["username"] = student['name']
        session["user_id"] = student['s_ID']
        return redirect(url_for('studentDashboard'))

    return render_template('index.html', error="Invalid username or password")

 
@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')
 
# ═════════════════════════════════════════════════════════════
# ADMIN ROUTES
# ═════════════════════════════════════════════════════════════
 
@app.route('/admin/dashboard')
def adminDashboard():
    g = admin_required()
    if g: return g
    cursor = get_cursor()
    stats = {}
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM Instructor"); 
        stats['instructors'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) AS count FROM Student");    
        stats['students']    = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) AS count FROM Course");     
        stats['courses']     = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) AS count FROM Section");    
        stats['sections']    = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) AS count FROM Department"); 
        stats['departments'] = cursor.fetchone()['count']
    except pymysql.Error as e:
        print(e)
    cursor.close()
 
    cursor2 = get_cursor()
    recent_instructors, recent_students = [], []
    try:
        cursor2.execute("SELECT * FROM Instructor ORDER BY i_ID DESC LIMIT 6")
        recent_instructors = cursor2.fetchall()
        cursor2.execute("SELECT * FROM Student ORDER BY s_ID DESC LIMIT 6")
        recent_students = cursor2.fetchall()
    except pymysql.Error as e:
        print(e)
    cursor2.close()
    return render_template('dashboard_admin.html',
                           stats=stats,
                           recent_instructors=recent_instructors,
                           recent_students=recent_students)
 
# ── CRUD INSTRUCTOR ──────────────────────────────────────────
def _load_instructor_data():
    cursor = get_cursor()
    data, depts = [], []
    try:
        cursor.execute("CALL lookInstructorAll();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookAllDepartments();")
        depts = [r['dept_name'] for r in cursor2.fetchall()]
    except pymysql.Error as e: print(e)
    cursor2.close()
    return data, depts
 
@app.route('/admin/instructor', methods=['GET', 'POST'])
def crudInstructor():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            cursor = get_cursor()
            try:
                cursor.execute("CALL addInstructor(%s,%s,%s,%s);",
                               [request.form['id'], request.form['name'],
                                request.form['dept'], request.form['salary']])
                db.commit()
                flash('Instructor added successfully.', 'success')
            except pymysql.Error as e:
                flash(f'Error: {e}', 'danger')
            cursor.close()
        elif action == 'update':
            cursor = get_cursor()
            try:
                cursor.execute("CALL updateInstructor(%s,%s,%s,%s);",
                               [request.form['id'], request.form['name'],
                                request.form['dept'], request.form['salary']])
                db.commit()
                flash('Instructor updated.', 'success')
            except pymysql.Error as e:
                flash(f'Error: {e}', 'danger')
            cursor.close()
        elif action == 'delete':
            cursor = get_cursor()
            try:
                cursor.execute("CALL removeInstructor(%s);", [request.form['ID']])
                db.commit()
                flash('Instructor removed.', 'success')
            except pymysql.Error as e:
                flash(f'Cannot delete: instructor may be assigned to sections. ({e})', 'danger')
            cursor.close()
    data, depts = _load_instructor_data()
    return render_template('administrator/crud_instructor.html', data=data, depts=depts)
 
# ── CRUD STUDENT ─────────────────────────────────────────────
def _load_student_data():
    cursor = get_cursor()
    data, depts = [], []
    try:
        cursor.execute("CALL lookStudentAll();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookAllDepartments();")
        depts = [r['dept_name'] for r in cursor2.fetchall()]
    except pymysql.Error as e: print(e)
    cursor2.close()
    return data, depts
 
@app.route('/admin/student', methods=['GET', 'POST'])
def crudStudent():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            cursor = get_cursor()
            credits = request.form.get('credits') or 0
            try:
                cursor.execute("CALL addStudent(%s,%s,%s,%s);",
                               [request.form['id'], request.form['name'],
                                request.form['dept'], credits])
                db.commit()
                flash('Student added successfully.', 'success')
            except pymysql.Error as e:
                flash(f'Error: {e}', 'danger')
            cursor.close()
        elif action == 'update':
            cursor = get_cursor()
            try:
                cursor.execute("CALL updateStudent(%s,%s,%s,%s);",
                               [request.form['id'], request.form['name'],
                                request.form['dept'], request.form.get('credits', 0)])
                db.commit()
                flash('Student updated.', 'success')
            except pymysql.Error as e:
                flash(f'Error: {e}', 'danger')
            cursor.close()
        elif action == 'delete':
            cursor = get_cursor()
            try:
                cursor.execute("CALL removeStudent(%s);", [request.form['ID']])
                db.commit()
                flash('Student removed.', 'success')
            except pymysql.Error as e:
                flash(f'Cannot delete: student may be enrolled in sections. ({e})', 'danger')
            cursor.close()
    data, depts = _load_student_data()
    return render_template('administrator/crud_student.html', data=data, depts=depts)
 
# ── CRUD COURSE ──────────────────────────────────────────────
def _load_course_data():
    cursor = get_cursor()
    data, depts, prereqs_map = [], [], {}
    try:
        cursor.execute("CALL lookAllCourses();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookAllDepartments();")
        depts = [r['dept_name'] for r in cursor2.fetchall()]
    except pymysql.Error as e: print(e)
    cursor2.close()
    cursor3 = get_cursor()
    try:
        cursor3.execute("SELECT p.course_ID, p.prereq_id, c.title FROM Prereq p JOIN Course c ON c.course_ID=p.prereq_id ORDER BY p.course_ID")
        for row in cursor3.fetchall():
            prereqs_map.setdefault(row['course_ID'], []).append((row['prereq_id'], row['title']))
    except pymysql.Error as e: print(e)
    cursor3.close()
    return data, depts, prereqs_map
 
@app.route('/admin/course', methods=['GET', 'POST'])
def crudCourse():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        cursor = get_cursor()
        try:
            if action == 'add':
                cursor.execute("CALL insertCourse(%s,%s,%s,%s);",
                               [request.form['course_id'], request.form['title'],
                                request.form['dept'], request.form['credits']])
                db.commit(); flash('Course added.', 'success')
            elif action == 'update':
                cursor.execute("CALL updateCourse(%s,%s,%s,%s);",
                               [request.form['course_id'], request.form['title'],
                                request.form['dept'], request.form['credits']])
                db.commit(); flash('Course updated.', 'success')
            elif action == 'delete':
                cursor.execute("CALL removeCourse(%s);", [request.form['course_id']])
                db.commit(); flash('Course deleted.', 'success')
            elif action == 'add_prereq':
                cursor.execute("CALL insertPrereq(%s,%s);",
                               [request.form['course_id'], request.form['prereq_id']])
                db.commit(); flash('Prerequisite added.', 'success')
            elif action == 'remove_prereq':
                cursor.execute("CALL removePrereq(%s,%s);",
                               [request.form['course_id'], request.form['prereq_id']])
                db.commit(); flash('Prerequisite removed.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
    data, depts, prereqs_map = _load_course_data()
    return render_template('administrator/crud_course.html',
                           data=data, depts=depts, prereqs_map=prereqs_map)
 
# ── CRUD SECTION ─────────────────────────────────────────────
def _load_section_data():
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL lookAllSectionsAdmin();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor(); courses = []
    try:
        cursor2.execute("CALL lookAllCourses();"); courses = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    cursor3 = get_cursor(); timeslots = []
    try:
        cursor3.execute("CALL lookAllTimeSlots();"); timeslots = cursor3.fetchall()
    except pymysql.Error as e: print(e)
    cursor3.close()
    return data, courses, timeslots
 
@app.route('/admin/section', methods=['GET', 'POST'])
def crudSection():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        cursor = get_cursor()
        try:
            if action == 'add':
                ts   = request.form.get('time_slot_id') or None
                bldg = request.form.get('building')     or None
                room = request.form.get('room_number')  or None
                cursor.execute("CALL addSection(%s,%s,%s,%s,%s,%s,%s);",
                               [request.form['sec_id'], request.form['course_id'],
                                request.form['semester'], request.form['year'],
                                ts, bldg, room])
                db.commit(); flash('Section added.', 'success')
            elif action == 'update':
                bldg = request.form.get('building')    or None
                room = request.form.get('room_number') or None
                cursor.execute("CALL updateSectionRoom(%s,%s,%s);",
                               [request.form['sec_id'], bldg, room])
                db.commit(); flash('Section updated.', 'success')
            elif action == 'delete':
                cursor.execute("CALL removeSection(%s);", [request.form['sec_id']])
                db.commit(); flash('Section removed.', 'success')
        except pymysql.Error as e:
            flash(f'Cannot delete: students may be enrolled. ({e})', 'danger')
        cursor.close()
    data, courses, timeslots = _load_section_data()
    return render_template('administrator/crud_section.html',
                           data=data, courses=courses, timeslots=timeslots)
 
# ── CRUD DEPARTMENT ──────────────────────────────────────────
@app.route('/admin/department', methods=['GET', 'POST'])
def crudDepartment():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        cursor = get_cursor()
        try:
            if action == 'add':
                cursor.execute("CALL insertDepartment(%s,%s,%s);",
                               [request.form['dept_name'],
                                request.form.get('building') or None,
                                request.form.get('budget') or 0])
                db.commit(); flash('Department added.', 'success')
            elif action == 'update':
                cursor.execute("CALL updateDepartment(%s,%s,%s);",
                               [request.form['dept_name'],
                                request.form.get('building') or None,
                                request.form.get('budget') or 0])
                db.commit(); flash('Department updated.', 'success')
            elif action == 'delete':
                cursor.execute("CALL removeDepartment(%s);", [request.form['dept_name']])
                db.commit(); flash('Department deleted.', 'success')
        except pymysql.Error as e:
            flash(f'Cannot delete: linked records exist. ({e})', 'danger')
        cursor.close()
    cursor = get_cursor(); data = []
    try:
        cursor.execute("CALL lookAllDepartmentsFull();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('administrator/crud_department.html', data=data)
 
# ── CRUD TIMESLOT ────────────────────────────────────────────
@app.route('/admin/timeslot', methods=['GET', 'POST'])
def crudTimeslot():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        cursor = get_cursor()
        try:
            if action == 'add':
                cursor.execute("CALL insertTimeSlot(%s,%s,%s,%s);",
                               [request.form['ts_id'], request.form['day'],
                                request.form['start_hr'], request.form['end_hr']])
                db.commit(); flash('Time slot added.', 'success')
            elif action == 'update':
                cursor.execute("CALL updateTimeSlot(%s,%s,%s,%s);",
                               [request.form['ts_id'], request.form['day'],
                                request.form['start_hr'], request.form['end_hr']])
                db.commit(); flash('Time slot updated.', 'success')
            elif action == 'delete':
                cursor.execute("CALL removeTimeSlot(%s);", [request.form['ts_id']])
                db.commit(); flash('Time slot deleted.', 'success')
        except pymysql.Error as e:
            flash(f'Cannot delete: used by sections. ({e})', 'danger')
        cursor.close()
    cursor = get_cursor(); data = []
    try:
        cursor.execute("CALL lookAllTimeSlots();"); data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('administrator/crud_timeslot.html', data=data)
 
# ── CRUD CLASSROOM ───────────────────────────────────────────
@app.route('/admin/classroom', methods=['GET', 'POST'])
def crudClassroom():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        cursor = get_cursor()
        try:
            cursor.execute("CALL updateSectionRoom(%s,%s,%s);",
                           [request.form['sec_id'],
                            request.form.get('building') or None,
                            request.form.get('room_number') or None])
            db.commit(); flash('Classroom updated.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
    cursor = get_cursor(); data, timeslots = [], []
    try:
        cursor.execute("""
            SELECT s.sec_ID, s.course_ID, c.title, s.semester, s.year,
                   s.building, s.room_number, s.time_slot_ID,
                   ts.day, ts.start_hr, ts.end_hr
            FROM Section s
            LEFT JOIN Course c ON c.course_ID = s.course_ID
            LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
            ORDER BY s.building, s.room_number, s.year DESC
        """)
        data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookAllTimeSlots();"); timeslots = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    return render_template('administrator/crud_classroom.html', data=data, timeslots=timeslots)
 
# ── ASSIGN TEACHERS ──────────────────────────────────────────
@app.route('/admin/assign', methods=['GET', 'POST'])
def adminAssign():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        action = request.form.get('action')
        cursor = get_cursor()
        try:
            if action == 'assign':
                sec_id = request.form['sec_id']
                cursor.execute("SELECT course_ID, semester, year FROM Section WHERE sec_ID=%s", [sec_id])
                sec = cursor.fetchone()
                if sec:
                    cursor.execute("CALL assignInstructor(%s,%s,%s,%s);",
                                   [request.form['i_id'], sec['course_ID'], sec_id, sec['semester']])
                    db.commit(); flash('Instructor assigned.', 'success')
            elif action == 'remove':
                cursor.execute("CALL dropInstructor(%s,%s);",
                               [request.form['i_id'], request.form['sec_id']])
                db.commit(); flash('Assignment removed.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
 
    cursor = get_cursor(); assigns, instructors, sections = [], [], []
    try:
        cursor.execute("CALL lookAllTeaches();");        assigns     = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookInstructorAll();");   instructors = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    cursor3 = get_cursor()
    try:
        cursor3.execute("CALL lookAllSectionsAdmin();"); sections    = cursor3.fetchall()
    except pymysql.Error as e: print(e)
    cursor3.close()
    return render_template('administrator/instructorClasses.html',
                           assigns=assigns, instructors=instructors, sections=sections)
 
# ── ADMIN PROFILE ────────────────────────────────────────────
@app.route('/admin/profile', methods=['GET', 'POST'])
def adminProfile():
    g = admin_required()
    if g: return g
    if request.method == 'POST':
        user_id  = session['user_id']
        uname    = request.form.get('username', '').strip()
        new_pw   = request.form.get('new_password', '').strip()
        cursor = get_cursor()
        try:
            if uname:
                cursor.execute("UPDATE Users SET username=%s WHERE user_id=%s", [uname, user_id])
                session['username'] = uname
            if new_pw:
                cursor.execute("UPDATE Users SET password_hash=%s WHERE user_id=%s",
                               [generate_password_hash(new_pw), user_id])
            db.commit(); flash('Profile updated.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
    return render_template('administrator/updateAdministrator.html', success=False)
 
# ═════════════════════════════════════════════════════════════
# INSTRUCTOR ROUTES
# ═════════════════════════════════════════════════════════════
 
def _instructor_sections(i_id):
    cursor = get_cursor(); sections = []
    try:
        cursor.execute("CALL lookInstructorSections(%s);", [i_id])
        sections = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return sections
 
@app.route('/instructor/dashboard')
def instructorDashboard():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    cursor = get_cursor(); instructor = None
    try:
        cursor.execute("CALL lookInstructorID(%s);", [i_id])
        instructor = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
    sections = _instructor_sections(i_id)
    cursor2 = get_cursor(); advisee_count = 0
    try:
        cursor2.execute("SELECT COUNT(*) FROM Advises WHERE i_ID=%s", [i_id])
        row = cursor2.fetchone()
        if row:
            advisee_count = list(row.values())[0]
    except pymysql.Error as e: print(e)
    finally:
        cursor2.close()
    return render_template('dashboard_instructor.html',
                           instructor=instructor, sections=sections, advisee_count=advisee_count)
 
# ── TEACHING SEARCH ──────────────────────────────────────────
@app.route('/instructor/teaching', methods=['GET', 'POST'])
def searchTeaching():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    if request.method == 'GET':
        return render_template('instructor/sectionTeaching.html')
    semester = request.form['semester']
    year     = request.form['year']
    cursor = get_cursor(); data = []
    try:
        cursor.execute("""
            SELECT t.sec_ID, t.course_ID, c.title, t.semester, t.year,
                   s.building, s.room_number, ts.day, ts.start_hr, ts.end_hr
            FROM Teaches t
            JOIN Course c ON c.course_ID = t.course_ID
            LEFT JOIN Section s ON s.sec_ID = t.sec_ID
            LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
            WHERE t.i_ID = %s AND t.semester = %s AND t.year = %s
            ORDER BY t.sec_ID
        """, [i_id, semester, year])
        data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('instructor/sectionTeaching.html',
                           data=data, semester=semester, year=year)
 
# ── ROSTER ───────────────────────────────────────────────────
@app.route('/instructor/roster', methods=['GET', 'POST'])
def searchRoster():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    my_sections = _instructor_sections(i_id)
    if request.method == 'GET':
        return render_template('instructor/searchRoster.html', my_sections=my_sections)
    sec_id = request.form['sec_id']
    cursor = get_cursor(); data = []
    try:
        cursor.execute("CALL lookSectionRoster(%s);", [sec_id])
        data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('instructor/searchRoster.html',
                           my_sections=my_sections, data=data, selected_sec=sec_id)
 
# ── GRADES ───────────────────────────────────────────────────
@app.route('/instructor/grades', methods=['GET', 'POST'])
def updateGrades():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    my_sections = _instructor_sections(i_id)
    if request.method == 'GET':
        return render_template('instructor/updateGrades.html', my_sections=my_sections)
 
    action = request.form.get('action')
    sec_id = request.form['sec_id']
 
    if action == 'load':
        cursor = get_cursor(); students = []
        try:
            cursor.execute("CALL lookSectionRoster(%s);", [sec_id])
            students = cursor.fetchall()
        except pymysql.Error as e: print(e)
        cursor.close()
        return render_template('instructor/updateGrades.html',
                               my_sections=my_sections, students=students, sec_id=sec_id)
 
    if action == 'submit':
        cursor = get_cursor()
        try:
            cursor.execute("CALL assignGrade(%s,%s,%s);",
                           [request.form['s_id'], sec_id,
                            request.form['grade'].strip().upper()])
            db.commit()
        except pymysql.Error as e: print(e)
        cursor.close()
        cursor2 = get_cursor(); students = []
        try:
            cursor2.execute("CALL lookSectionRoster(%s);", [sec_id])
            students = cursor2.fetchall()
        except pymysql.Error as e: print(e)
        cursor2.close()
        return render_template('instructor/updateGrades.html',
                               my_sections=my_sections, students=students,
                               sec_id=sec_id, success=True)
 
# ── ADVISEES ─────────────────────────────────────────────────
@app.route('/instructor/advisor', methods=['GET', 'POST'])
def instructorAdvisor():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    if request.method == 'POST':
        action = request.form['action']
        s_id   = request.form['s_id']
        cursor = get_cursor()
        try:
            if action == 'add':
                cursor.execute("CALL addAdvisor(%s,%s);", [i_id, s_id])
                db.commit(); flash('Student added as advisee.', 'success')
            elif action == 'remove':
                cursor.execute("CALL removeAdvisor(%s,%s);", [i_id, s_id])
                db.commit(); flash('Advisee removed.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
 
    cursor = get_cursor(); advisees, all_students = [], []
    try:
        cursor.execute("CALL lookInstructorAdvisees(%s);", [i_id])
        advisees = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor()
    try:
        cursor2.execute("CALL lookStudentAll();")
        all_students = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    return render_template('instructor/instructorAdvisor.html',
                           advisees=advisees, all_students=all_students)
 
# ── REMOVE STUDENT FROM SECTION ──────────────────────────────
@app.route('/instructor/remove', methods=['GET', 'POST'])
def instructorRemoveStudent():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    my_sections = _instructor_sections(i_id)
    if request.method == 'GET':
        return render_template('instructor/removeStudent.html', my_sections=my_sections)
 
    action = request.form.get('action')
    sec_id = request.form['sec_id']
 
    if action == 'load':
        cursor = get_cursor(); students = []
        try:
            cursor.execute("CALL lookSectionRoster(%s);", [sec_id])
            students = cursor.fetchall()
        except pymysql.Error as e: print(e)
        cursor.close()
        return render_template('instructor/removeStudent.html',
                               my_sections=my_sections, students=students, sec_id=sec_id)
 
    if action == 'remove':
        cursor = get_cursor()
        try:
            cursor.execute("CALL dropStudent(%s,%s);", [request.form['s_id'], sec_id])
            db.commit(); flash('Student removed from section.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
        cursor2 = get_cursor(); students = []
        try:
            cursor2.execute("CALL lookSectionRoster(%s);", [sec_id])
            students = cursor2.fetchall()
        except pymysql.Error as e: print(e)
        cursor2.close()
        return render_template('instructor/removeStudent.html',
                               my_sections=my_sections, students=students, sec_id=sec_id)
 
# ── PREREQUISITES ────────────────────────────────────────────
@app.route('/instructor/prereqs', methods=['GET', 'POST'])
def updatePrereqs():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    cursor = get_cursor(); instructor = None
    try:
        cursor.execute("CALL lookInstructorID(%s);", [i_id])
        instructor = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
 
    if request.method == 'POST':
        action  = request.form.get('action')
        cid     = request.form['course_id']
        prereq  = request.form['prereq_id']
        cursor2 = get_cursor()
        try:
            if action == 'add':
                cursor2.execute("CALL insertPrereq(%s,%s);", [cid, prereq])
                db.commit(); flash('Prerequisite added.', 'success')
            elif action == 'remove':
                cursor2.execute("CALL removePrereq(%s,%s);", [cid, prereq])
                db.commit(); flash('Prerequisite removed.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor2.close()
 
    courses, all_courses, prereqs_map = [], [], {}
    cursor3 = get_cursor()
    try:
        if instructor:
            cursor3.execute("SELECT * FROM Course WHERE dept_name=%s ORDER BY course_ID", [instructor['dept_name']])
            courses = cursor3.fetchall()
    except pymysql.Error as e: print(e)
    cursor3.close()
    cursor4 = get_cursor()
    try:
        cursor4.execute("CALL lookAllCourses();"); all_courses = cursor4.fetchall()
    except pymysql.Error as e: print(e)
    cursor4.close()
    cursor5 = get_cursor()
    try:
        cursor5.execute("SELECT p.course_ID, p.prereq_id, c.title FROM Prereq p JOIN Course c ON c.course_ID=p.prereq_id")
        for row in cursor5.fetchall():
            prereqs_map.setdefault(row['course_ID'], []).append((row['prereq_id'], row['title']))
    except pymysql.Error as e: print(e)
    cursor5.close()
    return render_template('instructor/updatePrereqs.html',
                           courses=courses, all_courses=all_courses, prereqs_map=prereqs_map)
 
# ── INSTRUCTOR PROFILE ───────────────────────────────────────
@app.route('/instructor/profile', methods=['GET', 'POST'])
def updateInstructorProfile():
    g = instructor_required()
    if g: return g
    i_id = session['user_id']
    cursor = get_cursor(); instructor = None
    try:
        cursor.execute("CALL lookInstructorID(%s);", [i_id])
        instructor = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor(); depts = []
    try:
        cursor2.execute("CALL lookAllDepartments();")
        depts = [r['dept_name'] for r in cursor2.fetchall()]
    except pymysql.Error as e: print(e)
    cursor2.close()
 
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dept = request.form.get('dept', instructor['dept_name'] if instructor else '')
        cursor3 = get_cursor()
        try:
            cursor3.execute("UPDATE Instructor SET name=%s, dept_name=%s WHERE i_ID=%s",
                            [name, dept, i_id])
            db.commit()
        except pymysql.Error as e: print(e)
        cursor3.close()
        uname  = request.form.get('username', '').strip()
        new_pw = request.form.get('new_password', '').strip()
        cursor4 = get_cursor()
        try:
            if uname:
                cursor4.execute("UPDATE Users SET username=%s WHERE user_id=%s", [uname, i_id])
                session['username'] = uname
            if new_pw:
                cursor4.execute("UPDATE Users SET password_hash=%s WHERE user_id=%s",
                                [generate_password_hash(new_pw), i_id])
            db.commit(); flash('Profile updated.', 'success')
        except pymysql.Error as e:
            flash(f'Username taken or error: {e}', 'danger')
        cursor4.close()
        cursor5 = get_cursor()
        try:
            cursor5.execute("CALL lookInstructorID(%s);", [i_id])
            instructor = cursor5.fetchone()
        except pymysql.Error as e: print(e)
        cursor5.close()
        return render_template('instructor/updateInstructor.html',
                               instructor=instructor, depts=depts, success=True)
 
    return render_template('instructor/updateInstructor.html',
                           instructor=instructor, depts=depts, success=False)
 
# ═════════════════════════════════════════════════════════════
# STUDENT ROUTES
# ═════════════════════════════════════════════════════════════
 
@app.route('/student/dashboard')
def studentDashboard():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    cursor = get_cursor(); student = None
    try:
        cursor.execute("CALL lookStudent(%s);", [s_id])
        student = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor(); classes = []
    try:
        cursor2.execute("CALL lookStudentClasses(%s);", [s_id])
        classes = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    return render_template('dashboard_student.html', student=student, classes=classes)
 
# ── MY CLASSES: REGISTER / DROP ──────────────────────────────
@app.route('/student/classes', methods=['GET', 'POST'])
def studentClasses():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    if request.method == 'POST':
        action = request.form.get('action')
        sec_id = request.form['sec_id']
        cursor = get_cursor()
        try:
            if action == 'register':
                cursor.execute("SELECT course_ID, semester FROM Section WHERE sec_ID=%s", [sec_id])
                sec = cursor.fetchone()
                if sec:
                    cursor.execute("CALL enrollStudent(%s,%s,%s,%s);",
                                   [s_id, sec['course_ID'], sec_id, sec['semester']])
                    db.commit(); flash('Registered successfully!', 'success')
            elif action == 'drop':
                cursor.execute("CALL dropStudent(%s,%s);", [s_id, sec_id])
                db.commit(); flash('Class dropped.', 'success')
        except pymysql.Error as e:
            flash(f'Error: {e}', 'danger')
        cursor.close()
 
    cursor2 = get_cursor(); my_classes, available = [], []
    try:
        cursor2.execute("CALL lookStudentClasses(%s);", [s_id])
        my_classes = cursor2.fetchall()
    except pymysql.Error as e: print(e)
    cursor2.close()
    cursor3 = get_cursor()
    try:
        cursor3.execute("CALL lookAllSections();")
        available = cursor3.fetchall()
    except pymysql.Error as e: print(e)
    cursor3.close()
    enrolled_ids = {r['sec_ID'] for r in my_classes}
    return render_template('student/studentClass.html',
                           my_classes=my_classes, available=available, enrolled_ids=enrolled_ids)
 
# ── GRADES ───────────────────────────────────────────────────
@app.route('/student/grades')
def studentGrades():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    cursor = get_cursor(); grades = []
    try:
        cursor.execute("""
            SELECT tk.course_ID, c.title, c.credits,
                   tk.semester, s.year, tk.grade
            FROM Takes tk
            JOIN Course c ON c.course_ID = tk.course_ID
            LEFT JOIN Section s ON s.sec_ID = tk.sec_ID
            WHERE tk.s_ID = %s
            ORDER BY s.year DESC, tk.semester
        """, [s_id])
        grades = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('student/checkGrade.html', grades=grades)
 
# ── BROWSE COURSES BY SEMESTER ───────────────────────────────
@app.route('/student/courses', methods=['GET', 'POST'])
def studentCourses():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    if request.method == 'GET':
        return render_template('student/checkCourse.html')
    semester = request.form['semester']
    year     = request.form['year']
    cursor = get_cursor(); data = []
    try:
        cursor.execute("CALL lookSectionsBySemester(%s,%s);", [semester, year])
        data = cursor.fetchall()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor(); enrolled_ids = set()
    try:
        cursor2.execute("SELECT sec_ID FROM Takes WHERE s_ID=%s", [s_id])
        enrolled_ids = {r['sec_ID'] for r in cursor2.fetchall()}
    except pymysql.Error as e: print(e)
    cursor2.close()
    return render_template('student/checkCourse.html',
                           data=data, semester=semester, year=year, enrolled_ids=enrolled_ids)
 
# ── SECTION INFO ─────────────────────────────────────────────
@app.route('/student/section', methods=['GET', 'POST'])
def studentSectionInfo():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    if request.method == 'GET':
        return render_template('student/sectionInfo.html')
    sec_id = request.form['sec_id'].strip()
    cursor = get_cursor(); section = None
    try:
        cursor.execute("""
            SELECT s.sec_ID, s.course_ID, s.semester, s.year,
                   s.time_slot_ID, s.building, s.room_number,
                   c.title, c.credits, c.dept_name,
                   ts.day, ts.start_hr, ts.end_hr
            FROM Section s
            LEFT JOIN Course c ON c.course_ID = s.course_ID
            LEFT JOIN Time_Slot ts ON ts.time_slot_ID = s.time_slot_ID
            WHERE s.sec_ID = %s
        """, [sec_id])
        section = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
 
    instructor = None
    cursor2 = get_cursor()
    try:
        cursor2.execute("""
            SELECT i.name, i.dept_name
            FROM Teaches t JOIN Instructor i ON i.i_ID = t.i_ID
            WHERE t.sec_ID = %s LIMIT 1
        """, [sec_id])
        instructor = cursor2.fetchone()
    except pymysql.Error as e: print(e)
    cursor2.close()
 
    is_enrolled = False
    cursor3 = get_cursor()
    try:
        cursor3.execute("SELECT 1 FROM Takes WHERE s_ID=%s AND sec_ID=%s", [s_id, sec_id])
        is_enrolled = cursor3.fetchone() is not None
    except pymysql.Error as e: print(e)
    cursor3.close()
 
    return render_template('student/sectionInfo.html',
                           section=section, instructor=instructor,
                           is_enrolled=is_enrolled, sec_id=sec_id)
 
# ── ADVISOR INFO ─────────────────────────────────────────────
@app.route('/student/advisor')
def studentAdvisorInfo():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    cursor = get_cursor(); advisor = None
    try:
        cursor.execute("CALL lookStudentAdvisor(%s);", [s_id])
        advisor = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
    return render_template('student/advisorInfo.html', advisor=advisor)
 
# ── STUDENT PROFILE ──────────────────────────────────────────
@app.route('/student/profile', methods=['GET', 'POST'])
def updateStudent():
    g = student_required()
    if g: return g
    s_id = session['user_id']
    cursor = get_cursor(); student = None
    try:
        cursor.execute("CALL lookStudent(%s);", [s_id])
        student = cursor.fetchone()
    except pymysql.Error as e: print(e)
    cursor.close()
    cursor2 = get_cursor(); depts = []
    try:
        cursor2.execute("CALL lookAllDepartments();")
        depts = [r['dept_name'] for r in cursor2.fetchall()]
    except pymysql.Error as e: print(e)
    cursor2.close()
 
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dept = request.form.get('dept', student['dept_name'] if student else '')
        cursor3 = get_cursor()
        try:
            cursor3.execute("UPDATE Student SET name=%s, dept_name=%s WHERE s_ID=%s",
                            [name, dept, s_id])
            db.commit()
        except pymysql.Error as e: print(e)
        cursor3.close()
        uname  = request.form.get('username', '').strip()
        new_pw = request.form.get('new_password', '').strip()
        cursor4 = get_cursor()
        try:
            if uname:
                cursor4.execute("UPDATE Users SET username=%s WHERE user_id=%s", [uname, s_id])
                session['username'] = uname
            if new_pw:
                cursor4.execute("UPDATE Users SET password_hash=%s WHERE user_id=%s",
                                [generate_password_hash(new_pw), s_id])
            db.commit(); flash('Profile updated.', 'success')
        except pymysql.Error as e:
            flash(f'Username taken or error: {e}', 'danger')
        cursor4.close()
        cursor5 = get_cursor()
        try:
            cursor5.execute("CALL lookStudent(%s);", [s_id])
            student = cursor5.fetchone()
        except pymysql.Error as e: print(e)
        cursor5.close()
        return render_template('student/updateStudent.html',
                               student=student, depts=depts, success=True)
 
    return render_template('student/updateStudent.html',
                           student=student, depts=depts, success=False)

# ─────────────────────────────────────────────────────────────
@app.route('/admin/queries')
def adminQueries():
    g = admin_required()
    if g: return g
    return render_template('administrator/additionalFunctionality.html')

@app.route('/admin/deptAvgGrade', methods=['GET', 'POST'])
def deptGradeAvg():
    g = admin_required()
    if g: return g

    if request.method == 'GET':
        return render_template('administrator/additionalFunctionality.html')

    dept_name = request.form['department']
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL deptAvgGrade(%s);", [dept_name])
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
    finally:
        cursor.close()
    return render_template('administrator/additionalFunctionality.html', data=data, department=dept_name)

@app.route('/admin/courseGradeAvg', methods=['GET', 'POST'])
def courseGradeAvg():
    g = admin_required()
    if g: return g

    if request.method == 'GET':
        return render_template('administrator/additionalFunctionality.html')

    course_id = request.form['course_id']
    start_year = request.form['start_year']
    end_year = request.form['end_year']
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL courseGradeAvg(%s, %s, %s);", [course_id, start_year, end_year])
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
    finally:
        cursor.close()
    return render_template('administrator/additionalFunctionality.html', data=data, course=course_id)

@app.route('/admin/studentsByDept', methods=['GET', 'POST'])
def studentsByDept():
    g = admin_required()
    if g: return g

    if request.method == 'GET':
        return render_template('administrator/additionalFunctionality.html')

    dept_name = request.form['department']
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL getStudentsByDept(%s);", [dept_name])
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
    finally:
        cursor.close()
    return render_template('administrator/additionalFunctionality.html', data=data, department=dept_name)

@app.route('/admin/bestWorstClasses', methods=['GET', 'POST'])
def bestWorstClasses():
    g = admin_required()
    if g: return g

    if request.method == 'GET':
        return render_template('administrator/additionalFunctionality.html')

    semester = request.form['semester']
    year = request.form['year']
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL bestWorstClasses(%s, %s);", [semester, year])
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
    finally:
        cursor.close()
    return render_template('administrator/additionalFunctionality.html', data=data, semester=semester, year=year)

@app.route('/admin/enrolledByDept', methods=['GET', 'POST'])
def enrolledByDept():
    g = admin_required()
    if g: return g

    if request.method == 'GET':
        return render_template('administrator/additionalFunctionality.html')

    dept_name = request.form['department']
    cursor = get_cursor()
    data = []
    try:
        cursor.execute("CALL enrolledStudentsByDept(%s);", [dept_name])
        data = cursor.fetchall()
    except pymysql.Error as e:
        print(e)
    finally:
        cursor.close()
    return render_template('administrator/additionalFunctionality.html', data=data, department=dept_name)
 
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(port=4500)