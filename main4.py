from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)

all_books = []

@app.route('/')
def home():
    return render_template('index4.html', books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form
        new_book = {
            "title": data['title'],
            "author": data['author'],
            "rating": data['rating']
        }
        all_books.append(new_book)

        # NOTE: You can use the redirect method from flask to redirect to another route
        # e.g. in this case to the home page after the form has been submitted.
        return redirect(url_for('home'))
    return render_template('add1.html')


if __name__ == "__main__":
    app.run(debug=True)

