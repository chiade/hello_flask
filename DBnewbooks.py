from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f"<Book {self.title}>"

# #CREATE RECORD
# with app.app_context():
#     new_book = Book(id=4, title="Harry ", author="J.K", rating=9.35)
#     db.create_all()
#     db.session.add(new_book)
#     db.session.commit()

# ##READ ALL RECORDS
# all_books = db.session.query(Book).all()
# ##READ A RECORD BY QUERY
# book = Book.query.filter_by(title="Harry Potter").first()
# ##UPDATE A RECORD BY QUERY
# book_to_update = Book.query.filter_by(title="Harry Potter").first()
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()
# ##UPDATE RECORD BY PRIMARY KEY
# book_id = 1
# book_to_update = Book.query.get(book_id)
# book_to_update.title = "Harry Potter and the Globet of Fire"
# db.session.commit()
# ##DELETE RECORD BY PRIMARY KEY
# book_id = 2
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()

@app.route('/')
def home():
    #READ ALL RECORDS
    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template('index4.html', books=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        #CREATE RECORD
        with app.app_context():
            new_book = Book(
                title=data['title'],
                author=data['author'],
                rating=data['rating']
            )
            db.create_all()
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add1.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        with app.app_context():
            data = request.form
            #UPDATE RECORD
            book_id = data['id']
            book_to_update = db.session.get(Book, book_id)
            book_to_update.rating = data['rating']
            db.session.commit()
            return redirect(url_for('home'))

    book_id = request.args.get('id')
    with app.app_context():
        book_selected = db.session.get(Book, book_id)
    return render_template('edit_rating.html', book=book_selected)

@app.route('/delete')
def delete():
    with app.app_context():
        book_id = request.args.get('id')

        #DELETE RECORD BY ID
        book_to_delete = db.session.get(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
