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

# Main page
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
    #return render_template('hello.html', name=name)
    return "Hello"


@app.route('/user/<username>/')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/info/', methods=['GET'])
def client_info():
    return render_template('info.html', ip=request.remote_addr, parent_dict=parse_http_headers(request))

# Return IP address of visitor
@app.route('/ip/')
def ip():
    return request.remote_addr

# Return reverse DNS lookup of visitor IP
@app.route('/reverse/')
def reverse():
    reverse_lookup = str(get_client_reverse_lookup(request.remote_addr))
    return reverse_lookup

# Return User-Agent
@app.route('/ua/')
def ua():
    #parse_http_headers(request)
    return get_specific_header(parse_http_headers(request), "User-Agent")

# Return User-Agent
@app.route('/lang/')
def lang():
    #parse_http_headers(request)
    return get_specific_header(parse_http_headers(request), "Accept-Language")


# Loop over HTTP headers and return a dictionnary filled by them
def parse_http_headers(req):

    headers = {}

    for header in req.headers:
        headers[header[0]] = header[1]
    return headers

# Make reverse DNS lookup from IP address
def get_client_reverse_lookup(ip):
    try:
        addr = reversename.from_address(ip)
        return resolver.query(addr, "PTR")[0]
    except:
        return "No reverse lookup available"


# Get chosen header from headers
def get_specific_header(headers, ua):
    
    # Loop through headers to find and return the needed header
    for h in headers:
        if h == ua:
            return headers[h]

    # End of the loop. No needed header was detected
    return "No " + ua + " header sended"


if __name__ == "__main__":
    app.run()