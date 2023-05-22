from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
my_email = "chiade1234@gmail.com"
password = "kbuyafgtorqfhlpo"
app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post['id'] == index:
            requested_post = blog_post
    return render_template("post1.html", post=requested_post)

@app.route('/about')
def about():
    return render_template("about.html")

# @app.route('/contact')
# def contact():
#     return render_template("contact1.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact1.html", msg_sent=True)
    return render_template("contact1.html", msg_sent=False)

# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])
#     return "<h1>Successfully sent your message</h1>"

# @app.route("/login", methods=["POST"])
# def receive_data():
#     name = request.form["username"]
#     password = request.form["password"]
#     return f"<h1>Name: {name}, Password: {password}</h1>"

def send_email(name, email, phone, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="chia_desmond@hotmail.com",
            msg=email_message
        )

if __name__ == "__main__":
    app.run(debug=True)