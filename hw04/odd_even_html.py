from flask import Flask, request

app = Flask(__name__)

# 1. 숫자를 입력하는 메인 페이지
@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="kr">
    <head>
        <meta charset="UTF-8">
        <title>홀짝 판별기</title>
    </head>
    <body>
        <h2>홀수인가요? 짝수인가요?</h2>
        <form method="GET" action="/check">
            <label>숫자 입력:
                <input type="number" name="num" required>
            </label>
            <button type="submit">판별하기</button>
        </form>
    </body>
    </html>
    """

# 2. 결과를 계산해서 보여주는 페이지
@app.route("/check")
def check_odd_even():
    # 사용자가 입력한 'num'이라는 이름의 데이터를 가져옵니다.
    # 기본값은 0으로 설정하고 숫자로 변환합니다.
    num = request.args.get('num', default=0, type=int)
    
    # 홀짝 판별 로직
    if num % 2 == 0:
        result_text = f"입력하신 숫자 {num}은(는) <b>짝수</b>입니다."
    else:
        result_text = f"입력하신 숫자 {num}은(는) <b>홀수</b>입니다."

    # 결과를 HTML 형식으로 반환합니다.
    resp = f"""
    <html>
    <head><title>판별 결과</title></head>
    <body>
        <h2>판별 결과</h2>
        <p>{result_text}</p>
        <hr>
        <a href="/">다시 입력하기</a>
    </body>
    </html>
    """
    return resp

if __name__ == "__main__":
    app.run(debug=True)