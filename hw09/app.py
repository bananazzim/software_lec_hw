from flask import Flask, render_template
import os
import pandas as pd
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():  
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about_me.html")


@app.route("/blog_list")
def blog_list():
    posts = []
    csv_path = os.path.join(BASE_DIR, "blog_data.csv")
    df = pd.read_csv(csv_path, encoding="utf-8")
    for index, row in df.iterrows():
        posts.append(row.to_dict())

    print(posts)
    return render_template("blog_list.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)

    #템플릿에 다 박았는데 왜 첫화면만 나올까?
    #이제는 서버끼리의 url연결을 통해 이동하기때문이야
    #인덱스 안에 url주소를 수정해줘야해
