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
    #return render_template('index.html')
    return '/'

@app.route('/hello/')
#@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/method', methods=['HEAD', 'GET'])
def client_info():
    #parent_dict = [{'A':'val1','B':'val2'}]
    #headers=parse_request(request)
    print(request.headers)
    return render_template('hello.html', ip=request.remote_addr, parent_dict=parse_request(request))



def parse_request(req):
    ##print(req.headers)

    headers = {}

    for header in req.headers:
        #response += header[0] + " : " + header[1] +  "<br/>"
        headers[header[0]] = header[1]

    print(headers)
    return headers


if __name__ == "__main__":
    app.run()