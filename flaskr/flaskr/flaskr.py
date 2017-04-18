# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hogwarts.db'),
    SECRET_KEY='development key',
    USERNAME='Dumbledore',
    PASSWORD='hogwarts',
    USERNAME2='Harry'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'hogwarts_db'):
        g.hogwarts_db = connect_db()
    return g.hogwarts_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'hogwarts_db'):
        g.hogwarts_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('createdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

 
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME']:
            if request.form['password'] == app.config['PASSWORD']:
                error = 'Invalid username or password'
                session['logged_in'] = True
                flash('You were logged in')
                session['admin'] = True
                return redirect(url_for('home'))
            else:
                error = 'Invalid password'
        elif request.form['username'] == app.config['USERNAME2']:
            if request.form['password'] == app.config['PASSWORD']:
                error = 'Invalid username or password'
                session['logged_in'] = True
                flash('You were logged in')
                session['admin'] = False		
                return redirect(url_for('home'))
            else:
                error = 'Invalid password'
        else:
            error = 'Invalid Username'
            
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run()

# STUDENTS STUFF
@app.route('/show_entries')
def show_entries():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Student")
    rows = cur.fetchall();
    return render_template('show_entries.html', rows = rows)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into Student(stuId, lastName, firstName, GPA, House, Schedule) values (?, ?, ?, ?, ?, ?)',
                 [request.form['stuId'], request.form['lastName'], request.form['firstName'], request.form['GPA'],request.form['House'], request.form['Schedule']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/deleteStud', methods=['POST'])
def deleteStud():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Student where stuId = ?', [request.form['studDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('show_entries'))

@app.route('/edit/',methods=['GET', 'POST'])
def editStud():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	student = request.form['stuId']
        db.execute('update Student set GPA=?, Schedule=? where stuId=' + student,
            [request.form['GPA'], request.form['Schedule']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('show_entries'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select stuId, lastName, firstName, GPA, House, Schedule from Student where stuId=stuId')
        entries = [{"stuId" : row[0], "lastName" : row[1], "firstName" : row[2], "GPA" : row[3], "House" : row[4], "Schedule" : row[5]} for row in cur.fetchall()]
        return render_template('edit_entries.html', entries=entries)


#PROFESSORS STUFF
@app.route('/professors')
def professors():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Professors")
    rows = cur.fetchall();
    return render_template('professors.html', rows = rows)

@app.route('/addProf', methods=['POST'])
def add_prof():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into Professors(ProfID, name, subject) values (?, ?, ?)',
                 [request.form['ProfID'], request.form['name'], request.form['subject']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('professors'))

@app.route('/deleteProf', methods=['POST'])
def deleteProf():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Professors where ProfID = ?', [request.form['profDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('professors'))

@app.route('/editProf/',methods=['GET', 'POST'])
def editProf():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	professors = request.form['ProfID']
        db.execute('update Professors set subject=? where ProfID=' + professors,
            [request.form['subject']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('professors'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select ProfID, name, subject from Professors where ProfID=ProfID')
        entries = [{"ProfID" : row[0], "name" : row[1], "subject" : row[2]} for row in cur.fetchall()]
        return render_template('edit_professors.html', entries=entries)

#CLASSES STUFF

@app.route('/classes')
def classes():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Classes")
    rows = cur.fetchall();
    return render_template('classes.html', rows = rows)

@app.route('/editClass/',methods=['GET', 'POST'])
def editClass():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	classes = request.form['classTitle']
        db.execute('update Classes set classTitle=? where classTitle=' + classes,
            [request.form['ProdID']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('classes'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select classTitle, ProfID, NumStud from Classes where classTitle=ClassTitle')
        entries = [{"classTitle" : row[0], "ProfID" : row[1], "NumStud" : row[2]} for row in cur.fetchall()]
        return render_template('edit_classes.html', entries=entries)

@app.route('/addClass', methods=['POST'])
def add_class():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into Classes(classTitle, ProfID, NumStud) values (?, ?, ?)',
                 [request.form['classTitle'], request.form['ProfID'], request.form['NumStud']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('classes'))

@app.route('/deleteClass', methods=['POST'])
def deleteClass():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Classes where classTitle = ?', [request.form['classDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('classes'))

#Room STUFF

@app.route('/room')
def room():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Room")
    rows = cur.fetchall();
    return render_template('room.html', rows = rows)

@app.route('/editRoom/',methods=['GET', 'POST'])
def editRoom():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	room = request.form['RoomId']
        db.execute('update Room set RoomId=? where RoomId=' + room,
            [request.form['classTaught']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('room'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select RoomId, classTaught, Condition from Room where RoomId=RoomId')
        entries = [{"RoomId" : row[0], "classTaught" : row[1], "Condition" : row[2]} for row in cur.fetchall()]
        return render_template('edit_room.html', entries=entries)

@app.route('/addRoom', methods=['POST'])
def add_room():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into Room(RoomId, classTaught, Condition) values (?, ?, ?)',
                 [request.form['RoomId'], request.form['classTaught'], request.form['Condition']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('room'))

@app.route('/deleteRoom', methods=['POST'])
def deleteRoom():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Room where RoomId = ?', [request.form['roomDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('room'))

#Grades STUFF

@app.route('/grades')
def Grades():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Grades")
    rows = cur.fetchall();
    return render_template('grades.html', rows = rows)

@app.route('/editGrades/',methods=['GET', 'POST'])
def editGrades():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	grades = request.form['GPA']
        db.execute('update Grades set GPA=? where GPA=' + grades,
            [request.form['stuId']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('Grades'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select Semester, GPA, stuId from Grades where stuId=stuId')
        entries = [{"Semester" : row[0], "GPA" : row[1], "stuId" : row[2]} for row in cur.fetchall()]
        return render_template('edit_grades.html', entries=entries)

#Wand STUFF

@app.route('/wand')
def wand():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Wand")
    rows = cur.fetchall();
    return render_template('wand.html', rows = rows)

#House STUFF

@app.route('/House')
def House():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from House")
    rows = cur.fetchall();
    return render_template('house.html', rows = rows)

#Book STUFF

@app.route('/Books')
def Books():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Books")
    rows = cur.fetchall();
    return render_template('books.html', rows = rows)

@app.route('/addBook', methods=['POST'])
def add_book():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into Books(bID, classRequired, NumPages) values (?, ?, ?)',
                 [request.form['bID'], request.form['classRequired'], request.form['NumPages']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('Books'))

@app.route('/deleteBook', methods=['POST'])
def deleteBook():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Books where bID = ?', [request.form['bookDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('Books'))

#Extra Curricular STUFF

@app.route('/EC')
def EC():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from ExtraCurricular")
    rows = cur.fetchall();
    return render_template('e_c.html', rows = rows)

@app.route('/editEC/',methods=['GET', 'POST'])
def editEC():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        db = get_db()
	club = request.form['Clubs']
        db.execute('update ExtraCurricular set Clubs=? where Clubs=' + club,
            [request.form['Season']])
        db.commit()
        flash('Entry was successfully edited')
        return redirect(url_for('EC'))
    elif request.method != 'POST':
        db = get_db()      
	cur = db.execute('select Clubs, Season from ExtraCurricular where Clubs=Clubs')
        entries = [{"Clubs" : row[0], "Season" : row[1]} for row in cur.fetchall()]
        return render_template('edit_ec.html', entries=entries)

@app.route('/addEC', methods=['POST'])
def add_EC():
    if not session.get('logged_in'):
	abort(401)
    db = get_db()
    db.execute('insert into ExtraCurricular(Clubs, Season) values (?, ?, ?)',
                 [request.form['Clubs'], request.form['Season']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('EC'))

@app.route('/deleteEC', methods=['POST'])
def deleteEC():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from ExtraCurricular where Clubs= ?', [request.form['ecDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('EC'))

