from flask import Flask, render_template,request, session, redirect, url_for
from pymongo import MongoClient
from chatresponse import botResponse, chat_history
from flask_pymongo import PyMongo
from flask_login import logout_user
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb+srv://sowjanya:souji6819@cluster0-k3zzh.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient("mongodb+srv://sowjanya:souji6819@cluster0-k3zzh.mongodb.net/test?retryWrites=true&w=majority")
mongo=PyMongo(app)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = client.db.chat
    print(type(users))
    present_user = users.find_one({'username' : request.form['username']})
    print(str(present_user))

    if present_user:
        if(request.form['password'] == present_user['password']):
    
            session['username'] = request.form['username']
            return render_template('mychat.html')
    

    return 'invalid input'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.chat
        present = users.find_one({'username' : request.form['username']})

        if present is None:
            
            users.insert({'username' : request.form['username'],'E-mail' :  request.form['E-mail'],'password' : request.form['pass']})
            session['username'] = request.form['username']
            return render_template('mychat.html')

        return 'username taken'

    return render_template('register.html')

@app.route("/chatresponse", methods = ["GET","POST"] )
def resp():
    data = request.json
    chat_history(session["username"])
    
    return botResponse(data["user"], session["username"])



@app.route("/get_userrname", methods = ["GET","POST"] )
def uname():
    if(session["username"] != ""):
        print('username:' +str(session["username"]))
        a = chat_history(session["username"])
        r = {"username":session["username"], "bot":a["bot"], "user":a["user"]}
        # r = {"username":session["username"], "bot":"dummy", "user":"dummy"}
        return r
    return ""

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect(url_for('index'))

    else:
        return 'User already logged out.'

if __name__=='__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
