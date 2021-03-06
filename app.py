import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(300))

    def __repr__(self):
        return self.title


@app.route('/')
@app.route('/home')
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("index.html", data=articles)


@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        if 'image' not in request.files:
            return 'there is no file1 in form!'
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        image = request.files['image']

        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        article = Article(title=title, intro=intro, text=text, image=path)
        image.save(path)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"

    else:
        return render_template("create_article.html")


if __name__ == "__main__":
    app.run(debug=True)

