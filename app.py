from flask import Flask, render_template_string
import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_MODE = os.getenv("DATABASE_MODE")


app = Flask(__name__)

conn_info = {
    "host": DATABASE_URL,
    "port": DATABASE_PORT,
    "dbname": DATABASE_NAME,
    "user": DATABASE_USER,
    "sslmode": DATABASE_MODE
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Motivational Quote</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #667eea, #764ba2);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .card {
            background: rgba(0,0,0,0.4);
            padding: 40px;
            border-radius: 12px;
            max-width: 600px;
            text-align: center;
            font-size: 22px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="card">
        "{{ quote }}"
    </div>
</body>
</html>
"""

@app.route("/")
def quote():
    with psycopg.connect(**conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT quotes FROM quotes ORDER BY RANDOM() LIMIT 1;")
            quote = cur.fetchone()[0]
    return render_template_string(HTML_TEMPLATE, quote=quote)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)