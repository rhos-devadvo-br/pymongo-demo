from psycogreen.gevent import patch_psycopg
patch_psycopg()

from gevent.monkey import patch_all
patch_all()

from os import getenv
import sys
import signal
from pymongo import MongoClient
from flask import Flask, request, redirect, render_template


flask_server = Flask(__name__)
flask_server.config['SECRET_KEY'] = \
    getenv('FLASK_KEY') or \
    '_6ZPJgtzFHMSlxcl609RryDmHO35g7Yd4xEyySJLK_s='  # Don't use this in production, generate a secret random key!


@flask_server.route('/', methods=['GET'])
def hello_world():
    motd=get_motd()
    message_list=get_messages()
    return render_template('main.jinja', motd=motd, message_list=message_list)


@flask_server.route('/', methods=['POST'])
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


if __name__ == '__main__':
    try:
        dbname = getenv('DATABASE_NAME')
        dbuser = getenv('DATABASE_USER')
        dbpass = getenv('DATABASE_PASSWORD')
        client = MongoClient(
            'mongodb://{}:{}@mongodb/{}'.format(dbuser, dbpass, dbname)
        )
        db = client[dbname]
        database_enabled = True
    except:
        database_enabled = False
    finally:
        flask_server.run(
            host=getenv('FLASK_HOST') or "0.0.0.0",
            port=getenv('FLASK_PORT') or 5000,
            debug=getenv('FLASK_DEBUG') or True
        )
