
from flask import Flask, request, make_response, jsonify
import random, time, os, threading, requests
import ast


app = Flask(__name__)

@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    # 0 is valid → check None
    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    save_last("add", (a, b), a + b)
    return make_response(jsonify(s=a + b), 200)


@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    save_last("sub", (a, b), a - b)
    return make_response(jsonify(s=a - b), 200)


@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    # FIX: accept zero properly
    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    save_last("mul", (a, b), a * b)
    return make_response(jsonify(s=a * b), 200)


@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    if b == 0:
        return make_response("Division by zero\n", 400)

    save_last("div", (a, b), a / b)
    return make_response(jsonify(s=a / b), 200)


@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)

    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    if b == 0:
        return make_response("Division by zero\n", 400)

    res = a % b
    save_last("mod", (a, b), res)
    return make_response(jsonify(s=res), 200)


@app.route('/random')
def rand():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)

    # FIX: accept zero, reject missing
    if a is None or b is None:
        return make_response("Invalid input\n", 400)

    if a > b:
        return make_response("Invalid input\n", 400)

    res = random.randint(a, b)
    save_last("random", (a, b), res)
    return make_response(jsonify(s=res), 200)


@app.route('/reduce')
def reduce():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=str)

    if op is None or lst is None:
        return make_response("Invalid operator\n", 400)

    # FIX: protect eval
    try:
        lst = eval(lst)
        if not isinstance(lst, list):
            return make_response("Invalid list\n", 400)
    except:
        return make_response("Invalid list\n", 400)

    # perform operations
    if op == 'add':
        res = sum(lst)

    elif op == 'sub':
        if len(lst) == 0:
            return make_response("Invalid list\n", 400)
        res = lst[0] - sum(lst[1:])

    elif op == 'mul':
        res = 1
        for i in lst:
            res *= i

    elif op == 'div':
        if len(lst) == 0:
            return make_response("Invalid list\n", 400)
        res = lst[0]
        for i in lst[1:]:
            if i == 0:
                return make_response("Division by zero\n", 400)
            res /= i

    else:
        return make_response(f"Invalid operator: {op}", 400)

    save_last("reduce", (op, lst), res)
    return make_response(jsonify(s=res), 200)


@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

mock_save_last = None
def save_last(op, args, res):
    try:
        timestamp = time.time()
        payload = {'timestamp': timestamp, 'op': op, 'args': args, 'res': res}
        requests.post('http://db-manager:5000/notify', json=payload, timeout=1)
    except:
        # Do nothing if DB manager is not available
        pass

        

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

