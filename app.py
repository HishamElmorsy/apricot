from flask import Flask, render_template, request, redirect, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2.extras


load_dotenv()


app = Flask(__name__)
app.secret_key = "your_secret_key"  


DATABASE_URL = os.environ.get("DATABASE_URL")



#cursor = conn.cursor()

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    sort = request.args.get("sort", "")
    page = request.args.get("page", 1, type=int)
    per_page = 20
    query = request.args.get("q", "").strip()

    deals = []

    if query:
        response = requests.get(
            "https://www.cheapshark.com/api/1.0/deals",
            params={
                'title': query,
                'exact': 0,
                'onSale': 1,
                'pageSize': 60
            }
        )
        deals = response.json() if response.status_code == 200 else []
    else:
        response = requests.get(
            "https://www.cheapshark.com/api/1.0/deals",
            params={
                'storeID': 1,
                'upperPrice': 15,
                'pageSize': 60
            }
        )
        deals = response.json() if response.status_code == 200 else []

    for deal in deals:
        deal['savings'] = float(deal.get('savings', 0))
        deal['salePrice'] = float(deal.get('salePrice', 0))
        deal['normalPrice'] = float(deal.get('normalPrice', 0))

    if sort == "discount":
        deals.sort(key=lambda x: x["savings"], reverse=True)
    elif sort == "price":
        deals.sort(key=lambda x: x["salePrice"])

    total_pages = max(1, (len(deals) + per_page - 1) // per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_deals = deals[start:end]

    return render_template("index.html",
                           deals=paginated_deals,
                           sort=sort,
                           page=page,
                           total_pages=total_pages,
                           query=query)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id, hashed_password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            flash("Logged in successfully!")
            return redirect("/")
        else:
            flash("Invalid username or password.", "error")
            return redirect("/login")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Username already exists.")
            return redirect("/register")

        flash("Registered successfully! Please log in.")
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect("/")

@app.route("/wishlist")
def wishlist():
    if "user_id" not in session:
        flash("Please login to view your wishlist.")
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # هنا تستخدم DictCursor
    cursor.execute("SELECT * FROM wishlist WHERE user_id = %s", (session["user_id"],))
    games = cursor.fetchall()
    return render_template("wishlist.html", games=games)


@app.route("/wishlist/remove", methods=["POST"])
def remove_from_wishlist():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    game_id = request.form.get("game_id")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND cheapshark_game_id = %s", (session["user_id"], game_id))
    conn.commit()
    flash("Game removed from your wishlist.")
    return redirect("/wishlist")

@app.route("/wishlist/add", methods=["POST"])
def add_to_wishlist():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    game_title = request.form.get("game_title")  # ← هنا لازم تتأكد إنه مش None أو فاضي
    game_id = request.form.get("game_id")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO wishlist (user_id, game_title, cheapshark_game_id) VALUES (%s, %s, %s)",
            (session["user_id"], game_title, game_id)
        )
        conn.commit()
        flash("Game added to your wishlist!")
    except psycopg2.IntegrityError:
        conn.rollback()
        flash("Game is already in your wishlist.")
    return redirect("/")




@app.route("/autocomplete")
def autocomplete():
    term = request.args.get("term", "").strip()
    if not term:
        return jsonify(results=[])

    response = requests.get(f"https://www.cheapshark.com/api/1.0/games?title={term}&limit=5")
    if response.status_code != 200:
        return jsonify(results=[])

    games = response.json()
    titles = [game.get("external", "") for game in games]
    return jsonify(results=titles)

@app.route("/load_more")
def load_more():
    page = int(request.args.get("page", 0))
    sort = request.args.get("sort", "")
    q = request.args.get("q", "").lower()

    response = requests.get(f"https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=15&pageSize=20&pageNumber={page}")
    if response.status_code != 200:
        return {"deals": []}

    deals = response.json()

    if q:
        deals = [deal for deal in deals if q in deal["title"].lower()]

    for deal in deals:
        deal["savings"] = float(deal.get("savings", "0"))
        deal["salePrice"] = float(deal.get("salePrice", "0"))

    if sort == "discount":
        deals.sort(key=lambda x: x["savings"], reverse=True)
    elif sort == "price":
        deals.sort(key=lambda x: x["salePrice"])

    return {"deals": deals}





if __name__ == "__main__":
    app.run(debug=True)
