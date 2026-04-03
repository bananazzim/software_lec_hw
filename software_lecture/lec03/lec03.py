from rich.panel import Panel
dan = 5
print(Panel.fit(f"구구단 [red]{dan}단!", border_style="red"))
print(Panel.fit("\n".join(["{} * {} = {}".format(dan, i+1, dan * (i+1)) for i in range(1, 10)])))
