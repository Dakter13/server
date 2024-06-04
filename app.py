from flask import Flask, render_template, request, redirect
from urllib.parse import quote
import mysql.connector

app = Flask(__name__)


def query_db(query, params=None):
    conn = mysql.connector.connect(
        host='localhost',
        user='Daniil',
        password='(pvXEM1(HAlOqmCm',
        database='vkr-v1',
        charset='utf8mb4'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def render_data():
    tags_filter = request.args.get("tags")
    period_filter = request.args.get("period")

    query = """
    SELECT 
        pp._id AS photo_id, 
        pp.file_name AS file_name, 
        pp.photo_title, 
        pp.source, 
        GROUP_CONCAT(DISTINCT t.name_tegs) AS tags, 
        p.name AS period 
    FROM 
        periods_photo pp
    LEFT JOIN 
        photo_tag pt ON pp._id = pt.photo_id
    LEFT JOIN 
        tegs t ON pt.teg_id = t._id
    LEFT JOIN 
        periods_photo_id ppi ON pp._id = ppi.photo_id
    LEFT JOIN 
        period p ON ppi.period_id = p._id
    """

    if tags_filter:
        query += " AND t.name_tegs LIKE %s"
        tags_filter = f"%{tags_filter}%"

    if period_filter:
        query += " AND p.name LIKE %s"
        period_filter = f"%{period_filter}%"

    query += " pp._id, pp.file_name, pp.photo_title, pp.source, p.name "
    query += " Order by p._id"

    if tags_filter:
        periods_photo = query_db(query, (tags_filter,))
    elif period_filter:
        periods_photo = query_db(query, (period_filter,))
    else:
        periods_photo = query_db(query)

    tegs = query_db("SELECT DISTINCT name_tegs FROM tegs")
    all_tags = [row['name_tegs'] for row in tegs]

    photos_by_period = {}
    for file in periods_photo:
        period = file['period']
        if period is None:
            continue
        if period not in photos_by_period:
            photos_by_period[period] = []
        photos_by_period[period].append((
                                        file['photo_id'], quote(file['file_name']), file['photo_title'], file['source'],
                                        file['tags'], file['period']))

    return photos_by_period, all_tags


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/period')
def period():
    return render_template("period.html")


@app.route('/lectures')
def lectures():
    photos_by_period, all_tags = render_data()
    periods = query_db("SELECT DISTINCT name FROM period")
    all_periods = [row['name'] for row in periods]
    selected_period = request.args.get('period', all_periods[0])
    return render_template("lectures.html",
                           photos_by_period=photos_by_period,
                           all_tags=all_tags,
                           all_periods=all_periods,
                           selected_period=selected_period)


@app.route('/photos')
def photos():
    photos_by_period, all_tags = render_data()
    return render_template("photos.html", photos_by_period=photos_by_period, all_tags=all_tags)


if __name__ == '__main__':
    app.run(debug=True)
