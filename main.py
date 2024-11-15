from flask import Flask, request, jsonify
import psycopg2


app = Flask(__name__)


conn = psycopg2.connect(database="currency_db", user="postgres",
                        password="admin", host="localhost", port="5432")
cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS currency (
    id serial PRIMARY KEY,
    from_currency VARCHAR(3),
    to_currency VARCHAR(3),
    rate FLOAT);""")
cur.execute("SELECT COUNT(*) FROM currency;")
row_count = cur.fetchone()[0]
if row_count == 0:
    cur.execute("""INSERT INTO currency (from_currency, to_currency, rate) VALUES
                ('USD', 'EUR', 0.85),
                ('EUR', 'USD', 1.18),
                ('USD', 'CAD', 1.41),
                ('CAD', 'USD', 0.71)""")
conn.commit()
cur.close()
conn.close()


@app.route("/list")
def list_conversions():
    conn = psycopg2.connect(database="currency_db", user="postgres",
                            password="admin", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT from_currency, to_currency, rate FROM currency;")
    conversions = cur.fetchall()
    cur.close()
    conn.close()
    conversions_list = [
        {
            'from_currency': from_curr,
            'to_currency': to_curr,
            'rate': rate
        }
        for from_curr, to_curr, rate in conversions
    ]
    return jsonify(conversions_list)


if __name__ == '__main__':
    app.run(debug=True)
