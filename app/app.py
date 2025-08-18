from difflib import get_close_matches
PRODUCT_LIST = [
    "Domates","Salatalık","Patlıcan","Patates","Soğan","Sivri Biber",
    "Biber","Kapya","Fini","Dolma","Fasulye","Limon",
    "Karpuz","Kavun","Elma","Armut","Muz","Çilek","Kivi","Erik"
]

def fix_product_name(name):
    name = name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ö", "o")
    matches = get_close_matches(name, [p.lower().replace("ı","i").replace("ğ","g").replace("ş","s").replace("ü","u").replace("ö","o").replace("ç","c") for p in PRODUCT_LIST], n=1, cutoff=0.7)
    if matches:
        # Orijinal isimle eşleştir
        for p in PRODUCT_LIST:
            if p.lower().replace('ı', 'i').replace('ğ', 'g').replace('ş', 's').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c') == matches[0]:
                return p
    return name.capitalize()

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app=Flask(__name__)
DATABASE = "orders.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/reset", methods=["POST"])
def reset_orders():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/")
def index():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.execute("SELECT product, unit, SUM(quantity) as total FROM orders GROUP BY product, unit")
    totals = cursor.fetchall()
    # Şirketlere göre grupla
    company_orders = {}
    for order in orders:
        company = order["company"]
        company_orders.setdefault(company, []).append(order)
    conn.close()
    return render_template("index.html", orders=orders, totals=totals, company_orders=company_orders)

@app.route("/add", methods=["POST"])
def add_order():
    company=request.form["company"]
    product=request.form["product"]
    quantity=float(request.form["quantity"])
    unit=request.form.get("unit","kg")
    conn=get_db()
    cursor=conn.cursor()
    fixed_product=fix_product_name(product)
    #Aynı şirket ve ürün varsa miktarı güncelle
    cursor.execute("SELECT id, quantity FROM orders WHERE company=? AND product=? AND unit=?", (company,fixed_product, quantity, unit))
    row=cursor.fetchone()
    if row:
        new_quantity=row["quantity"] + quantity
        cursor.execute("UPDATE orders SET quantity=? WHERE id=?", (new_quantity, row["id"]))
    else:
        cursor.execute("INSERT INTO orders (company, product, quantity, unit) VALUES (?, ?, ?, ?)", (company, fixed_product, quantity, unit))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

#Toplu sipariş ekleme
@app.route("/bulk_add", methods=["POST"])
def bulk_add():
    company=request.form["company"]
    bulk_list=request.form["bulk_list"]
    conn=get_db()
    cursor=conn.cursor()
    for line in bulk_list.strip().split("\n"):
        line=line.strip()
        if not line:
            continue
        parts=line.split()
        product=""
        quantity=1
        unit="kg" #varsayılan birim
        if len(parts)==3:
            product,qty,unit=parts
        elif len(parts)==2:
            product, qty = parts
            unit = "kg" 
        else:
            product=" ".join(parts[:-2])
            qty=parts[-2]
            unit=parts[-1] if parts [-1] else "kg"  
        try:
            quantity=float(quantity.replace(",", "."))
        except:
            quantity=1
        fixed_product=fix_product_name(product)
        cursor.execute("INSERT INTO orders (company, product, quantity, unit) VALUES (?, ?, ?, ?)", (company, fixed_product, quantity, unit))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    #Create table if not exists
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        product TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()
    app.run(debug=True)
