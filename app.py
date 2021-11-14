from flask import Flask, jsonify, request, g, url_for, redirect, session, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisisasecret!'


def connect_db():
    sql = sqlite3.connect('C:/Users/Truc Duong/Desktop/Projects/flask_app/Database/hive.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1> Hello, Welcome to StudyHive </h1>'

@app.route('/home', methods = ['POST','GET'] )
@app.route('/home/<string:name>', methods =['POST', 'GET'])
def home(name=' '):
    session['name'] = name
    return '<h1>Hello {}, you are on the home page </h1>'.format(name)
 

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    
    else:
        name ='Not in Session'
    return jsonify({'key1': 'values','key2': [1,2,3], 'name' : name})

@app.route('/register')
def query():
    name = request.args.get('name')
    link = request.args.get('link')
    return '<h1> Hi {}. Your uploaded picture is from {} </h1>'.format(name,link)


@app.route('/theform', methods=['GET','POST'])
def theform():

    if request.method == 'GET':
        return '''<form method="POST" action = "/theform"> 
                        <input type="text" name ="name">
                        <input type="text" name ="link">
                        <input type="submit">Submit
                    </form>'''
    else:
        name = request.form['name']
        link = request.form['link']

        db = get_db()
        db.execute('insert into users (name, link) values (?,?)', [name,link])
        db.commit()


        return redirect(url_for('home', name = name, link = link))

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, link from users')
    results = cur.fetchall()

    return '<h1> The ID is {}. The name is {}. The link is {}. </h1>'.format(results[0]['id'], results[0]['name'], results[0]['link'])



if __name__ == '__main__':
    app.run()