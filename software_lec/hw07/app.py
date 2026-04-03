from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():  
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/strawberry")
def strawberry():
    return render_template("strawberry.html")

if __name__ == "__main__":
    app.run(debug=True)

    #템플릿은 붕어빵틀이래
    #붕어빵틀은 html파일이래
    #붕어빵틀에 재료를 넣어서 붕어빵을 만들듯이
    #html파일에 데이터를 넣어서 웹페이지를 만들 수 있어
    # {}는 html파일에서 데이터를 넣을 때 사용하는 문법이래