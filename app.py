from os import environ
import sys
import signal
from pymongo import MongoClient
from flask import Flask, request, redirect, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    motd=get_motd()
    message_list=get_messages()
    return render_template('main.jinja', motd=motd, message_list=message_list)


@app.route('/', methods=['POST'])
def save_message():
    if database_enabled:
        message = request.form['text']
        db.messages.insert_one({"text":message})
    return redirect('/')


def get_messages():
    if database_enabled:
        try:
            return [message for message in db.messages.find()]
        except:
            return None
    else:
        return None


def get_motd():
    try:
        message = open('/webconfig/motd','r').read()
        return message
    except:
        return None


def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)


if __name__ == '__main__':
    try:
        dbname = environ['database-name']
        dbuser = environ['database-user']
        dbpass = environ['database-password']
        client = MongoClient(
            'mongodb://{}:{}@mongodb/{}'.format(dbuser, dbpass, dbname)
        )
        db = client[dbname]
        database_enabled = True
    except:
        database_enabled = False

    signal.signal(signal.SIGTERM, sigterm_handler)
    try:
        app.run(host='0.0.0.0', port=8080)
    finally:
        print('Exiting...')
