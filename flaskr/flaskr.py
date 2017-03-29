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
    PASSWORD='hogwarts'
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

@app.route('/show_entries')
def show_entries():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Student")
    rows = cur.fetchall();
    return render_template('show_entries.html', rows = rows)

 
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/professors')
def professors():
    con = sqlite3.connect("hogwarts.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Professors")
    rows = cur.fetchall();
    return render_template('professors.html', rows = rows)

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

@app.route('/deleteStud', methods=['POST'])
def deleteStud():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from Student where stuId = ?', [request.form['studDelete']])
    db.commit()
    flash('Entry was succesfully removed')
    return redirect(url_for('show_entries'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run()


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
