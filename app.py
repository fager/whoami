#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return 'Hello !'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/method', methods=['HEAD', 'GET'])
def method():
    if request.method == 'HEAD':
        return 'HEAD'
    else:
        parse_request(request)
        return 'GET'
	


def parse_request(req):
    #print(jsonify({'ip': request.remote_addr}))
    print(req.remote_addr)
    print(req.headers)




if __name__ == "__main__":
    app.run()