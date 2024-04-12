from flask import *
import sqlite3
from datetime import date

conn = sqlite3.connect("static/tododb.db",check_same_thread=False)
conn.row_factory = sqlite3.Row

app=Flask(__name__)

def fetch_data():
    curosor = conn.cursor()
    statement = '''SELECT * from todo'''
    curosor.execute('SELECT * FROM "todo" WHERE "Status" LIKE "%0%"')
    output  = curosor.fetchall()
    return output

def hist_data():
    curosor = conn.cursor()
    curosor.execute('SELECT * FROM "todo" WHERE "Status" LIKE "%1%"')
    output  = curosor.fetchall()
    return output


def count_rows():
    output = fetch_data()
    count = 0
    for i in output:
        count = count+1
    return count

# @app.route('/checked_row', methods = ['GET','POST'])
# def checked_row():
#     if request.method == 'POST':
#         value = request.form['delbtn']
#         cursor = conn.cursor()
#         cursor.execute(f'UPDATE "todo" SET "Status"=1 WHERE "Message"="{value}"')
#         conn.commit()
#     output = fetch_data()
#     count = count_rows()
#     return render_template('index.html',output  = output,count = count )\

@app.route('/checked_row', methods = ['GET','POST'])
def checked_row():
    if request.method == 'POST':
        value = request.form['delbtn']
        cursor = conn.cursor()
        today = date.today()
        cursor.execute(f'UPDATE "todo" SET "Status"=1,"Timestamp"="{today}" WHERE "Message"="{value}"')
        conn.commit()
    return redirect('/')

@app.route('/del_hist', methods=['GET','POST'])
def delete_hist():
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todo where "Status" > 0')
        conn.commit()
    return redirect('/')

@app.route('/add_row',methods=['GET','POST'])
def add_row():
    if request.method == 'POST':
        value = request.form['addtext']
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO "todo"("Message","Status","Timestamp") VALUES ("{value}",0,NULL);')
        conn.commit()
    return redirect('/')
    
@app.route('/')

def home():
    output = fetch_data()
    count = count_rows()
    hist = hist_data()
    return render_template('index.html',output  = output,count = count,hist=hist )

if __name__ == '__main__':
    app.run(debug = True)