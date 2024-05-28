from flask import Flask, render_template, request, redirect
from urllib.parse import quote
import mysql.connector

app = Flask(__name__)


def query_db(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='Daniil',
        password='(pvXEM1(HAlOqmCm',
        database='vkr-v1',
        charset='utf8mb4'
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
    encoded_file_names = [(file[0], quote(file[1])) for file in periods_photo]
    return render_template("photos.html", file_names=encoded_file_names)


if __name__ == '__main__':
    app.run(debug=True)
