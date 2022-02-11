from flask import Flask, render_template, request
import requests
import smtplib

my_email = "amir77mahdi76@gmail.com"
my_pass = "qgwmryabasnkhljh"
posts = requests.get("https://api.npoint.io/cbfb488a9e7c87eb47d5").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["get", "post"])
def contact():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        msg = request.form["message"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, my_pass)
            connection.sendmail(from_addr=my_email,
                                to_addrs=email,
                                msg=f"Subject:Contact Message\n\nUsername: {username}\n"
                                    f"Email: {email}\nPhone number: {phone_number}\nMessage: {msg}")
        return render_template("contact.html", message="Successfully send your message")
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
