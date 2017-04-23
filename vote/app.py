from flask import Flask, render_template, request, make_response, g, redirect
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()
redis_host = os.getenv('REDIS_HOST', "redis")
appRoot = os.getenv('APPLICATION_ROOT', "/")

app = Flask(__name__)
app.config["APPLICATION_ROOT"] = appRoot

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host=redis_host, db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

def redirectToRoot():
    return redirect(appRoot)

if __name__ == "__main__":
    from werkzeug.wsgi import DispatcherMiddleware

    if not appRoot == "/":
        app.wsgi_app = DispatcherMiddleware(redirectToRoot(), {
            appRoot: app.wsgi_app
        })

    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
