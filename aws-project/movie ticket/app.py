from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# AWS RDS MySQL Configuration
db = pymysql.connect(
    host="movieticket.cr8ma4u8uyyk.ap-southeast-2.rds.amazonaws.com",
    user="admin",
    password="Rakesh123",
    database="movie_db"
)

cursor = db.cursor()

USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("booking"))
        else:
            return "<h2>Invalid Login</h2>"

    return render_template("login.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        name = request.form["customer_name"]
        email = request.form["email"]
        movie = request.form["movie_name"]
        seats = request.form["seats"]
        date = request.form["booking_date"]

        sql = """
        INSERT INTO bookings
        (customer_name,email,movie_name,seats,booking_date)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(sql,(name,email,movie,seats,date))
        db.commit()

        return render_template("success.html")

    return render_template("booking.html")


@app.route("/bookings")
def bookings():

    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()

    return render_template("bookings.html", bookings=data)


if __name__ == "__main__":
    app.run(debug=True)