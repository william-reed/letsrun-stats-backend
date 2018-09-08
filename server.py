import os
import atexit
import json

from flask import Flask
from mysql.connector import connection

app = Flask(__name__)

db = connection.MySQLConnection(user=os.environ['MYSQL_USER'], password=os.environ['MYSQL_PASSWORD'], host='127.0.0.1',
                                database=os.environ['LETSRUN_DB'])
cursor = db.cursor()
API_PREFIX = "/api"
POST_COUNT = "SELECT COUNT(*) FROM posts WHERE author = %s"


@app.route("/")
def hello():
    return "Home"


@app.route(API_PREFIX + "/<username>")
def stats(username):
    cursor.execute(POST_COUNT, (username,))
    result = cursor.fetchone()
    return json.dumps({"posts": result})


def cleanup():
    cursor.close()
    db.close()
    print('Goodbye')


atexit.register(cleanup)
app.run()
