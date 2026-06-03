from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():

    bulan = request.args.get(
        "bulan",
        datetime.now().strftime("%Y-%m")
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nominal FROM budget WHERE bulan=?",
        (bulan,)
    )

    budget_data = cursor.fetchone()

    budget = budget_data["nominal"] if budget_data else 0

    cursor.execute("""
        SELECT *
        FROM transaksi
        WHERE bulan=?
        ORDER BY id DESC
    """, (bulan,))

    transaksi = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(harga)
        FROM transaksi
        WHERE bulan=?
    """, (bulan,))

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    sisa = budget - total

    conn.close()

    return render_template(
        "index.html",
        bulan=bulan,
        budget=budget,
        total=total,
        sisa=sisa,
        transaksi=transaksi
    )


@app.route("/set_budget", methods=["POST"])
def set_budget():

    bulan = request.form["bulan"]
    nominal = request.form["nominal"].replace(".", "")
    nominal = int(nominal)

    conn = get_connection()

    conn.execute("""
        INSERT OR REPLACE INTO budget
        (bulan, nominal)
        VALUES (?, ?)
    """, (bulan, nominal))

    conn.commit()
    conn.close()

    return redirect(f"/?bulan={bulan}")


@app.route("/tambah_transaksi", methods=["POST"])
def tambah_transaksi():

    nama_barang = request.form["nama_barang"]
    harga = request.form["harga"].replace(".", "")
    harga = int(harga)

    sekarang = datetime.now()

    tanggal = sekarang.strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    bulan = sekarang.strftime("%Y-%m")

    conn = get_connection()

    conn.execute("""
        INSERT INTO transaksi
        (nama_barang, harga, tanggal, bulan)
        VALUES (?, ?, ?, ?)
    """, (
        nama_barang,
        harga,
        tanggal,
        bulan
    ))

    conn.commit()
    conn.close()

    return redirect(f"/?bulan={bulan}")


@app.route("/hapus/<int:id>")
def hapus(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM transaksi WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/hapus_budget/<bulan>")
def hapus_budget(bulan):

    conn = get_connection()

    conn.execute(
        "DELETE FROM budget WHERE bulan=?",
        (bulan,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)