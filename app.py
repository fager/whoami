#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request
from dns import resolver        # DNS query of client IP
from dns import reversename     # Reverse lookup if client IP


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def main():
    ip=request.remote_addr
    return render_template('info.html', 
        ip=ip, 
        reverse=get_client_reverse_lookup(ip), 
        parent_dict=parse_http_headers(request)
    )

@app.route('/hello/')
#@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/info', methods=['GET'])
def client_info():
    return render_template('info.html', ip=request.remote_addr, parent_dict=parse_http_headers(request))



def parse_http_headers(req):

    headers = {}

    for header in req.headers:
        headers[header[0]] = header[1]
    return headers

def get_client_reverse_lookup(ip):
    try:
        addr = reversename.from_address(ip)
        return resolver.query(addr, "PTR")[0]
    except:
        return "No reverse lookup available"


if __name__ == "__main__":
    app.run()