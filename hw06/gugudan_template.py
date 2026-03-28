from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
       
   return render_template("gugudan.html")
@app.route("/gugudan")
def gugudan():
        dan = request.args.get('dan',default =2,type =int)
        resp = "<html>"
        resp += "<head><title>Gugudan</title><head>"
        resp +="<body>"
    
        for x in range(1,10):
            resp += (f"{dan} x {x} = {dan*x}<br>")
            

        resp += "</body>"
        resp += "</html>"

        return resp

app.run(debug=True)