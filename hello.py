from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1 style="text-align: center">Hello, world!</h1>' \
           '<p>This is a paragraph.</p>' \
           '<img src="https://media3.giphy.com/media/K1tgb1IUeBOgw/giphy.gif?cid=ecf05e47lwzrmju9nxd07jv9kmei812auoopdnjktf7xg388&rid=giphy.gif&ct=g" width=70%>'

#Different routes using the app.route decorator
def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper

@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined

def say_bye():
    return 'Bye!'

#Creating variable paths and converting the path to a specified data type
@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"

if __name__ == "__main__":
    #Run the spp in debug mode to auto-reload
    app.run(debug=True)

# ----------------- #Advanced Python Decorator functions ----------------------
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper

@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User('Des')
new_user.is_logged_in = True
create_blog_post(new_user)