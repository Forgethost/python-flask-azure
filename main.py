from flask import Flask, render_template, request, url_for, redirect
from dbaccess import *


app = Flask(__name__)


def get_summary(cursor, lookup_type, getdate):
    sqlstmt = """SELECT TOTAL_TWEETS, H1B_TWEETS,
                POSITIVE_TWEETS, NEGETIVE_TWEETS, NUETRAL_TWEETS
                FROM SUMMARY
                WHERE LOOKUP_TYPE = ?
                AND CONVERT(date, ENTRY_DATE) = ?"""
    cursor.execute(sqlstmt, (lookup_type, getdate))
    row = cursor.fetchone()
    return row

def build_chart_data(row):
    chart1data = "[['Type of posts','count']" + (","
    + r"['" + "Positive" + r"'," + str(row[2]) + r"]") + (","
    + r"['" + "Negetive" + r"'," + str(row[3]) + r"]") + (","
    + r"['" + "Nuetral" + r"'," + str(row[4]) + r"]") + "]"

    chart2data = "[ ['USCIS Twitter Post Type','count']" + (","
    + r"['" + "USCIS posts" + r"'," + str(row[0]) + r"]") + (","
    + r"['" + r"H-1B Posts" + r"'," + str(row[1]) + r"]") + " ]"

    return chart1data, chart2data


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/weekly')
def weekly():
    try:
        conn, cursor = conn_db()
        curr_date = get_current_date().strftime("%Y-%m-%d")
        row = get_summary(cursor, "WEEKLY", curr_date)

        if row == None:
            close_db(cursor)
            return render_template('500.html')
        else:
            chart1data, chart2data = build_chart_data(row)
            close_db(cursor)
            return render_template('gchart.html', chart1=chart1data, chart2=chart2data)

    except Exception as e:
        close_db(cursor)
        return render_template('505.html', e=e)


@app.route('/biweekly')
def biweekly():
    try:
        conn, cursor = conn_db()
        curr_date = get_current_date().strftime("%Y-%m-%d")
        row = get_summary(cursor, "BIWEEKLY", curr_date)

        if row == None:
            close_db(cursor)
            return render_template('500.html')
        else:
            chart1data, chart2data = build_chart_data(row)
            close_db(cursor)
            return render_template('gchart.html', chart1=chart1data, chart2=chart2data)

    except Exception as e:
        close_db(cursor)
        return render_template('505.html', e=e)


@app.route('/monthly')
def monthly():
    try:
        conn, cursor = conn_db()
        curr_date = get_current_date().strftime("%Y-%m-%d")
        row = get_summary(cursor, "MONTHLY", curr_date)

        if row == None:
            close_db(cursor)
            return render_template('500.html')
        else:
            chart1data, chart2data = build_chart_data(row)
            close_db(cursor)
            return render_template('gchart.html', chart1=chart1data, chart2=chart2data)

    except Exception as e:
        close_db(cursor)
        return render_template('505.html', e=e)


if __name__ == "__main__":
    app.run()

#@app.errorhandler(500)
#def severe_error(e):
#    render_template('506.html', 500)