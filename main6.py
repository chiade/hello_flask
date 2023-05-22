from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import random

app = Flask(__name__)
db = SQLAlchemy()

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Cafe {self.name}>"

    def to_dict(self):
        #Method 1:
        dictionary = {}
        #Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry where the key/value is name/value of column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        #Method 2: Alternatively use dictionary comprehension to do same thing
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index6.html")

@app.route('/random') #GET is allowed on all routes by default
def get_random_cafe():
    with app.app_context():
        cafes = db.session.query(Cafe).all()
        random_cafe = random.choice(cafes)
        #simply convert the random_cafe data record to a dictionary of key-value pairs
        return jsonify(
            cafe=random_cafe.to_dict()
            # cafe={
            # #Omit id from response
            # # "id": random_cafe.id,
            # "name": random_cafe.name,
            # "map_url": random_cafe.map_url,
            # "img_url": random_cafe.img_url,
            # "location": random_cafe.location,
            #
            # #Put some properties in a sub-category
            # "amenities": {
            #     "seats": random_cafe.seats,
            #     "has_toilet": random_cafe.has_toilet,
            #     "has_wifi": random_cafe.has_wifi,
            #     "has_sockets": random_cafe.has_sockets,
            #     "can_take_calls": random_cafe.can_take_calls,
            #     "coffee_price": random_cafe.coffee_price,
            # }
        # }
        )

@app.route('/all')
def get_all_cafes():
    with app.app_context():
        cafes = db.session.query(Cafe).all()
        #This uses a List Comprehension
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

@app.route('/search')
def get_cafe_at_location():
    query_location = request.args.get('loc')
    with app.app_context():
        cafes = db.session.query(Cafe).filter_by(location=query_location).all()
        if cafes:
            return jsonify(cafe=[cafe.to_dict() for cafe in cafes])
        else:
            return jsonify(error={"Not found": "Sorry, we do not have a cafe at that location."}), 404

@app.route('/add', methods=['POST'])
def post_new_cafe():
    data = request.form
    new_cafe = Cafe(
        name=data.get('name'),
        map_url=data.get('map_url'),
        location=data.get('loc'),
        has_sockets=bool(data.get('sockets')),
        has_toilet=bool(data.get('toilet')),
        has_wifi=bool(data.get('wifi')),
        can_take_calls=bool(data.get('calls')),
        seats=data.get('seats'),
        coffee_price=data.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added new cafe."})

@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def patch_new_price(cafe_id):
    new_price = request.args.get('new_price')
    with app.app_context():
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            cafe.coffee_price = new_price
            db.session.commit()
            return jsonify(response={"success": "Successfully updated price."}), 200
        else:
            return jsonify(error={"Not found": "Sorry, cafe with that id is not found in database."}), 404

@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    with app.app_context():
        if api_key == 'TopSecretAPIKey':
            cafe = db.session.query(Cafe).get(cafe_id)
            if cafe:
                db.session.delete(cafe)
                db.session.commit()
                return jsonify(response={"success": "Successfully deleted cafe from database."}), 200
            else:
                return jsonify(error={"Not found": "Sorry, cafe with that id is not found in database."}), 404
        else:
            return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure ypou have correct api_key."}), 403

if __name__ == '__main__':
    app.run(debug=True)
