from flask import Flask, render_template, redirect, request, url_for, g, jsonify, make_response, session
from flask_login import LoginManager
login_manager = LoginManager()
from flask_session import Session
import pymongo
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Flask'

client = pymongo.MongoClient("mongodb+srv://m001-student:m001-mongodb-basics@sandbox.frwq2ks.mongodb.net/?retryWrites=true&w=majority")
db = client.antony_test
c = db.movie
b=db.blacklist
a= db.users

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    wraps(f)
    def secure_function(*args, **kwargs):
        try:
            x = session["name"]
            if not x:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        except:
            return redirect(url_for("login"))
    return secure_function


@app.route("/movie")
def movie():
    items = c.find()
    return render_template('movie.html',items=items)

@app.route("/movie/add",methods=['POST','GET'], endpoint='func1')
@login_required
def add_movie():
    if request.method=="POST":
        name = request.form.get('name')
        year = request.form.get('year')
        yr= int(year)
        genre = request.form.get('genre')
        c.insert_one({"name":name, "year": yr, "genre":genre,"up":0, "down":0})
        #newLine
        a.update_many({}, {"$set": {name: False}})
    return render_template('add_movie.html')

@app.route("/movie/delete",methods=['POST','GET'], endpoint='func2')
@login_required
def del_movie():
    # a.delete_many({"password": "123"})
    if request.method=="POST":
        name = request.form.get('name')
        c.delete_many({"name":name})
    return render_template('del_movie.html')

@app.route("/movie/sort/name")
def sort_name():
    srt = c.find().sort("name")
    return render_template('movie.html',items=srt)

@app.route("/movie/sort/year")
def sort_year():
    srt = c.find().sort("year")
    return render_template('movie.html',items=srt)

@app.route("/movie/sort/votes")
def sort_votes():
    eachMov = c.find()
    for mov in eachMov:
        up = mov["up"]
        down = mov["down"]
        totalVotes = up-down
        t = str(totalVotes)
        query = {"name": mov["name"]}
        c.update_one(query, {"$set": {"totalVotes": totalVotes}})
    srt = c.find().sort("totalVotes", -1)
    return render_template('movie.html',items=srt)

@app.route("/movie/favGenre",methods=['POST','GET'], endpoint='func3')
@login_required
def fav_genre():
    genre = request.args.get('genre')
    srt = c.find({"genre":genre})
    return render_template('movie.html',items=srt)

@app.route("/movie/upvote/<name>",endpoint="func4")
@login_required
def upvote(name):
    x = a.find_one({'user': session["name"]})
    if not x[name]:
        query = {"name":name}
        inc = {"$inc":{"up":1}}
        c.update_one(query,inc)
        #newline
        query2 = {"user": session["name"]}
        newvalues2 = {"$set": {name: True}}
        a.update_one(query2, newvalues2)
    else:
        return "Already voted"
    return redirect(url_for('movie'))

@app.route("/movie/downvote/<name>", endpoint="func5")
@login_required
def downvote(name):
    x = a.find_one({'user': session["name"]})
    if not x[name]:
        query = {"name":name}
        inc = {"$inc":{"down":1}}
        c.update_one(query,inc)
        #newline
        query2 = {"user": session["name"]}
        newvalues2 = {"$set": {name: True}}
        a.update_one(query2, newvalues2)
    else:
        return "Already voted"
    return redirect(url_for('movie'))

@app.route('/login', methods =["POST","GET"])
def login():
    if request.method == 'POST':
        name = request.form.get("name")
        password = request.form.get("password")
        x = a.find_one({'user': name, 'password': password})
        if x:
            session["name"] = name
            return redirect(url_for("movie"))
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['name']
        password = request.form['password']
        a.insert_one({'user': user, 'password': password})
        #newline
        query = {'user': user}
        documents = c.find()
        for doc in documents:
            name = doc["name"]
            newvalues = {"$set":{name:False}}
            a.update_one(query, newvalues)
        return redirect(url_for("login"))
    return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    session.pop("name", None)
    return redirect("login")


if __name__ == '__main__':
    app.run(debug=True, port=5001)