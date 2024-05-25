from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def query_db(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='vkr-v1'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/period')
def period():
    return render_template("period.html")


@app.route('/lectures')
def lectures():
    return render_template("lectures.html")


@app.route('/photos')
def photos():
    query = "SELECT * FROM `periods_photo` WHERE 1"
    periods_photo = query_db(query)
    return render_template("photos.html", file_names=periods_photo)


if __name__ == '__main__':
    app.run(debug=True)
