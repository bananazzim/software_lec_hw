color = "red"
dan = 5
filename = "gugudan.html"
with open(filename, "w",encoding="utf-8") as f:
    f.write("<html>\n")
    f.write("<head><title>Gugudan</title></head>")
    f.write("<body>\n")
    f.write("<h1>5단 연산<h1>\n")
    for i in range(9):
        f.write(f"{dan} * {i+1} = <font color='{color}'>{dan* (i+1)}</font><br>\n")
    f.write("</body>\n")
    f.write("</html>\n")