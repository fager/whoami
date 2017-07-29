#!/usr/bin/env python3
 
# export FLASK_APP=app.py
# export FLASK_DEBUG=1
# flask run

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from dns import resolver        # DNS query of client IP
from dns import reversename     # Reverse lookup if client IP
import dicttoxml                # Dictionnary to xml
import json                     # Dictionnary to json



app = Flask(__name__)
app.config['DEBUG'] = True

# Main page
@app.route("/", methods=['GET'])
@app.route("/index/", methods=['GET'])
def main():
    ip = get_ip(parse_http_headers(request), request.remote_addr)
    port = request.environ.get('REMOTE_PORT')
    return render_template('index.html', 
        ip = ip, 
        port = port,
        reverse = get_client_reverse_lookup(ip), 
        parent_dict = parse_http_headers(request)
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
    return render_template('index.html', ip=request.remote_addr, parent_dict=parse_http_headers(request))

# Return IP address of visitor
@app.route('/ip/')
def ip():
    return get_ip(parse_http_headers(request), request.remote_addr)

# Return reverse DNS lookup of visitor IP
@app.route('/reverse/')
def reverse():
    reverse_lookup = str(get_client_reverse_lookup(get_ip(parse_http_headers(request), request.remote_addr)))
    return reverse_lookup

# Return User-Agent
@app.route('/ua/')
def ua():
    return get_specific_header(parse_http_headers(request), "User-Agent")

# Return User-Agent
@app.route('/lang/')
def lang():
    return get_specific_header(parse_http_headers(request), "Accept-Language")

# Return remote port
@app.route('/port/')
def port():
    return str(request.environ.get('REMOTE_PORT'))

# Return visitor info in json or xml format
@app.route('/raw/<type>/')
def raw(type=None):
    response = make_response(set_headers_format(type, request))

    # Add "Content-Type = text/xml" to header response
    if type == "xml":
        response.headers['Content-Type'] = 'text/xml'
        return response
    if type == "json":
        response.headers['Content-Type'] = 'application/json'
        return response


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
def get_specific_header(headers, hdr):
    
    # Loop through headers to find and return the needed header
    for h in headers:
        if h == hdr:
            return headers[h]

    # End of the loop. No needed header was detected
    return "No " + hdr + " header sended"


# Get the IP of client.
# If behind a reverse proxy (ex. in a docker-compose container with Nginx in front)
# with X-Real-IP or X-Forwarded-For set, return the remote IP.
def get_ip(headers, rmtip):
    for i in headers:
        # Look for 'X-Real-IP' header first
        if i == "X-Real-Ip":
            return headers[i]
        # Else look for 'X-Forwarded-For'
        elif i == "X-Forwarded-For":
            return headers[i]


    # Else return request.remote_addr
    # if no 'X-Real-Ip' or 'X-Forwarded-For'
    return rmtip

# Return headers in json or xml format
def set_headers_format(format, req):
    if format == "xml":
        return dicttoxml.dicttoxml(req.headers).decode("utf-8")
    if format == "json":
        return json.dumps(parse_http_headers(req))


if __name__ == "__main__":
    app.run()