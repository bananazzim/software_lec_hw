from flask import Flask

app = Flask(__name__)

@app.route("/gugu/<dan>")
def gugudan(dan):
    dan= int(dan)
    resp = "<html>"
    resp += "<head><title>Gugudan</title><head>"
    resp +="<body>"
    for x in range(1,10):
        resp += f"{dan} x {x} = <font color = 'blue'>{dan*x}</font>"
        resp += "<br>"

    resp += "</body>"
    resp += "</html>"
    print(resp)

    return resp

app.run(debug=True)
