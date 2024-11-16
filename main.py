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


@app.route("/list", methods=["GET"])
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


@app.route("/add", methods=["POST"])
def add_conversion():
    data = request.get_json()
    from_currency = data.get("from_currency")
    to_currency = data.get("to_currency")
    rate = data.get("rate")
    conn = psycopg2.connect(database="currency_db", user="postgres",
                            password="admin", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO currency (from_currency, to_currency, rate) VALUES (%s, %s, %s)",
        (from_currency, to_currency, rate)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "message": "Conversion added successfully.",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate
    })


@app.route("/convert", methods=["GET"])
def convert():
    from_currency = request.args.get("from_currency")
    to_currency = request.args.get("to_currency")
    amount = request.args.get("amount", type=float)
    conn = psycopg2.connect(database="currency_db", user="postgres",
                            password="admin", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        "SELECT rate FROM currency WHERE from_currency = %s AND to_currency = %s",
        (from_currency, to_currency)
    )
    rate_result = cur.fetchone()
    rate = rate_result[0]
    converted_amount = float(amount) * rate
    cur.close()
    conn.close()
    return jsonify({
        "converted_amount": converted_amount,
        "to_currency": to_currency,
        "from_currency": from_currency,
        "rate": rate,
        "amount": amount
    })


if __name__ == '__main__':
    app.run(debug=True)
