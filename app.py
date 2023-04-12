
from flask import Flask
from flask import render_template #дает возможность брать html файлы из любого 
# места но обязательно название папки где храняться : templates
from flask import request #библиотека закпросов
from flask import redirect#оба импорта(redirect & url_form)для блока try except
from flask import url_for
from flask_sqlalchemy import SQLAlchemy#создание библиотеки SQL - бд
# from datetime import datetime #библиотека датт
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# создание модели при добавление на сайт статей
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    articles = db.relationship('Article', backref='category_name')

    def __repr__(self):
        return f'Category: {self.id} - {self.name}'
    

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(50), nullable=False, unique=True)
    introduction = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Article: {self.id} - {self.title}'



# вставка перменных в html фаил
# @app.route('/test')
# def something():
#     number = 123
#     name = 'Максим'
#     return render_template('test.html', n=number, name = name)

# использование циклов



@app.route('/')
def index():
    latest_articles = Article.query.order_by(Article.pub_date.desc())[:3]#выведит три самых новых статьи 

    return render_template('index.html', articles=latest_articles)


# @app.route('/user/<int:user_id>')
# def index(user_id):
#     return f'Пользователь номер: {user_id}'

@app.route('/blog')
def blog():
    category = Category.query.filter_by(name='Блог').first()
    articles =Article.query.filter_by(category_id=category.id)


    return render_template('blog.html', articles=articles)

@app.route('/news')
def news():
    category = Category.query.filter_by(name='Новости').first()
    articles =Article.query.filter_by(category_id=category.id)


    return render_template('news.html', articles=articles)

# работа с наследованием позволяет работать с типовыми шаблонами

@app.route('/new_post', methods=['GET','Post'])
def new_post():
    if request.method == 'POST':
        category_id = request.form['category_select']#обращение к данным из html файла
        title = request.form['title']
        introduction = request.form['introduction']
        article_text = request.form['article_text']

        article = Article(category_id=category_id, 
                          title=title, 
                          introduction=introduction,
                            text = article_text)
        
        #исключение ошибок при добавлении статей в бд
        try:
            db.session.add(article)
            db.session.commit()

            return redirect(url_for('index'))
        
        except Exception as error:
            return f'Возникла ошибка! -> {error}'

    else:
        categories = Category.query.all()

        return render_template('new_post.html', categories=categories)
    
@app.route('/detail_post/<int:article_id>')
def detailed_post(article_id):
    article = Article.query.get_or_404(article_id)

    return render_template('detailed.html', article=article)


if __name__ == '__main__':# позволяет запускать напрямую через терминала
    app.run(debug=True)

















































