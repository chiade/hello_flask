import datetime
import requests
from flask import Flask, render_template
import random
from post import Post

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("blog.html", all_posts=post_objects)

@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)

# @app.route('/')
# def home():
#     random_number = random.randint(1, 10)
#     current_year = datetime.datetime.now().year
#     return render_template('example.html', num=random_number, year=current_year)

# @app.route('/guess/<name>')
# def guess(name):
#     gender_url = f"https://api.genderize.io?name={name}"
#     gender_response = requests.get(gender_url)
#     gender_data = gender_response.json()
#     gender = gender_data["gender"]
#     age_url = f"https://api.agify.io?name={name}"
#     age_response = requests.get(age_url)
#     age_data = age_response.json()
#     age = age_data["age"]
#     return render_template('guess.html', name=name, gender=gender, age=age)
#
# @app.route("/blog/<num>")
# def get_blog(num):
#     blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
#     response = requests.get(blog_url)
#     all_posts= response.json()
#     return render_template('blog.html', posts=all_posts)

if __name__ == "__main__":
    app.run(debug=True)