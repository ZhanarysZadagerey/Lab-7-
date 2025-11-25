import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

ALLOWED_MATH_OPS = ['add', 'sub', 'mul', 'div', 'mod', 'random', 'reduce', 'crash']
ALLOWED_STR_OPS = ['lower', 'upper', 'concat', 'reduce', 'crash']

#CHANGE URLS TO MATCH THE NAMES AND PORTS OF THE SERVICES IN THE DOCKER-COMPOSE FILE
STRING_URL = 'http://string:5000'
CALC_URL = 'http://calc:5000'
DB_MANAGER_URL = 'http://db-manager:5000'


ids = {} #CAREFUL, THIS IS NOT FOR MULTIUSER AND MULTITHREADING, JUST FOR DEMO PURPOSES

app = Flask(__name__, instance_relative_config=True)

def create_app():
    return app

def reduce(request, url):
    op = request.args.get('op')
    lst = request.args.get('lst')
    return url + f'/reduce?op={op}&lst={lst}'

@app.route('/calc/<op>')
def math(op):
    if op not in ALLOWED_MATH_OPS:
        return make_response('Invalid operation\n', 400)
    try:
        
        if(op == 'crash'):
            URL = CALC_URL + f'/crash'
        elif op == 'reduce':
            URL = reduce(request, CALC_URL)
        else:
            a = request.args.get('a')
            b = request.args.get('b')
            if a is None or b is None:
                return make_response('Invalid input\n', 400)
            URL = CALC_URL + f'/{op}?a={a}&b={b}'
        x = requests.get(URL)
        x.raise_for_status()
        res = x.json()
        return res
    except HTTPError:
        return make_response(x.content, x.status_code)
    except ConnectionError:
        return make_response('Calculator service is down\n', 500)

@app.route('/str/<op>')
def string(op):
    if op not in ALLOWED_STR_OPS:
        return make_response('Invalid operation\n', 400)
    if op == 'reduce':
        URL = reduce(request, STRING_URL)
        json_response = string_request(URL)
        return json_response
    
    a = request.args.get('a', type=str)
    if not a:
        return make_response('Invalid input\n', 400)

    if op == 'lower':
        json_response = string_request(STRING_URL + f'/{op}?a={a}')
    elif op == 'crash':
        json_response = string_request(STRING_URL + f'/crash')
    elif op == 'upper':
        json_response = string_request(STRING_URL + f'/{op}?a={a}')
    else:
        b = request.args.get('b', type=str)
        if not b:
            return make_response('Invalid input\n', 400)
        json_response = string_request(STRING_URL + f'/{op}?a={a}&b={b}')
    return json_response

def string_request(URL_API):
    try:
        x = requests.get(URL_API)
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('String service is down\n', 500)
    except HTTPError:
        return make_response(x.content, x.status_code)

@app.route('/getAll')
def getAll():
    try:
        x = requests.get(DB_MANAGER_URL + '/getAll')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('DB Manager service is down\n', 500)
    except HTTPError:
        return make_response(x.content, x.status_code)