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
    query = """
    SELECT 
        pp._id AS photo_id, 
        pp.file_name AS file_name, 
        pp.photo_title, 
        pp.source,
        GROUP_CONCAT(DISTINCT t.name_tegs ORDER BY t.name_tegs SEPARATOR ', ') AS tags, 
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
    WHERE 1=1
    """

    tags_filter = request.args.get("tags")
    period_filter = request.args.get("period", None)

    params = []

    if tags_filter:
        query += """
        AND pp._id IN (
            SELECT pt.photo_id
            FROM photo_tag pt
            JOIN tegs t ON pt.teg_id = t._id
            WHERE t.name_tegs LIKE %s
        )
        """
        params.append(f"%{tags_filter}%")

    if period_filter:
        query += " AND p.name LIKE %s"
        params.append(f"%{period_filter}%")

    query += """
    GROUP BY pp._id, pp.file_name, pp.photo_title, pp.source, p.name
    ORDER BY p._id
    """

    periods_photo = query_db(query, tuple(params))

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
            file['tags'], file['period']
        ))

    return photos_by_period, all_tags, period_filter


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/period')
def period():
    return render_template("period.html")


@app.route('/paper')
def paper():
    return render_template("paper.html")


@app.route('/lectures')
def lectures():
    photos_by_period, all_tags, period = render_data()
    periods = query_db("SELECT DISTINCT name FROM period")
    all_periods = [row['name'] for row in periods]
    selected_period = request.args.get('period', all_periods[0] if all_periods else None)
    return render_template("lectures.html",
                           photos_by_period=photos_by_period,
                           all_tags=all_tags,
                           period=period,
                           all_periods=all_periods,
                           selected_period=selected_period)


@app.route('/photos')
def photos():
    photos_by_period, all_tags, period = render_data()
    return render_template("photos.html",
                           photos_by_period=photos_by_period,
                           all_tags=all_tags,
                           period=period)


if __name__ == '__main__':
    app.run(debug=True)
