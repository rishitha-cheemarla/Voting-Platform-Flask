from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key
# Function to create a new SQLite connection and cursor
def get_db_connection():
    conn = sqlite3.connect('myproject.db') #connect to duck db here (first get VS Code and Pip)
    conn.row_factory = sqlite3.Row
    return conn

# Creating the student_info table 
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_info (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            number_811 TEXT NOT NULL,
            class_time TEXT NOT NULL,
            group_number TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize the database when the app is running

# Creating the polls table 
def init_polls_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS polls (
            id INTEGER PRIMARY KEY,
            poll_id TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

init_polls_db()

# Creating the votes table 
def init_votes_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            poll_id TEXT NOT NULL,
            number_811 TEXT NOT NULL,
            day TEXT,
            "group" TEXT NOT NULL,
            "group1" TEXT NOT NULL,
            "group2" TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

init_votes_db()

# Route for the student information form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        number_811 = request.form['811']
        class_time = request.form['class-time']
        group_number = request.form['group-number']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO student_info (name, number_811, class_time, group_number) VALUES (?, ?, ?, ?)",
                       (name, number_811, class_time, group_number))

        conn.commit()
        conn.close()

    return render_template('index.html')

# Display the "Create Poll" page
@app.route('/create_poll', methods=['GET'])
def create_poll():
    return render_template('poll.html')

# Handle the form submission and store the poll ID
@app.route('/create_poll', methods=['POST'])
def submit_poll():
    poll_id = request.form['poll_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO polls (poll_id) VALUES (?)', (poll_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('create_poll'))

# Route for voting in a poll
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        poll_id = request.form['poll_id']
        number_811 = request.form['811']
        passcode = request.form['passcode']
        day = request.form['day']
        group = request.form['vote_option']
        group1 = request.form['vote_option1']
        group2 = request.form['vote_option2']

       

        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute('''
            INSERT INTO votes (poll_id, number_811, day, "group", "group1", "group2")
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (poll_id, number_811, day, group, group1, group2))

        conn.commit()
        conn.close()
        flash('Vote submitted successfully', 'success')

    return render_template('voting.html')

if __name__ == '__main__':
    app.run(debug=True)