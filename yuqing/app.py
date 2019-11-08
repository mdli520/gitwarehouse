from flask import Flask,render_template,redirect,request
import os
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SECRET_KET'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/cucnews'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db1 = pymysql.connect('localhost', 'root', '1234', 'cucnews')
db= SQLAlchemy(app)
cursor = db1.cursor()
Session = sessionmaker(bind=db)
bootstrap = Bootstrap(app)
session = Session()


class News(db.Model):
    __tablename__ = 'news_test'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    newsurl = db.Column(db.String(255))
    newsfrom = db.Column(db.String(255))
    pageviews = db.Column(db.String(255))
    newsdate = db.Column(db.String(255))
    newsarticle = db.Column(db.Text)
    def __repr__(self):
        return '<News %r>' %self.title


# sql = "select  * from news_test where pageviews>5000 order by pageviews desc "
# try:
#     rscount=cursor.execute(sql)     #返回记录数
#     rs=cursor.fetchall()
#     text=""
#     for r in rs:
#         # print(r)
#         print(r[1],"阅读量：",r[4])
# except:
#         print("Error")



@app.route('/list/')
def list():
    news = News.query.all()

    return render_template('list.html', news=news)
# @app.route('/index')
# def index:


@app.route('/',methods=['GET','POST'])
def index():
    return redirect('/search')

@app.route('/search')
def search():
    db1 = pymysql.connect('localhost', 'root', '1234', 'cucnews')
    cursor = db1.cursor()
    wanted = request.args.get('wanted',type = str)
    if not wanted:
        wanted = "大数据"

    sql = "select  * from news_test where newsarticle like '%%%s%%'order by newsarticle desc "%wanted
    try:
        rscount = cursor.execute(sql)  # 返回记录数
        rs = cursor.fetchall()
        # text = ""
        # for r in rs:
        #     print(r)
        #     print(r[1], "阅读量：", r[4])
    except:
        print("Error")
    db1.close()
    return render_template('index.html',rs = rs,count = rscount)
if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()

    app.run()


