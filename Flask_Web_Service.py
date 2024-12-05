from flask import Flask, render_template, request
import subprocess

# Flask 애플리케이션 생성
app = Flask(__name__)

# 첫 번째 라우트 생성
@app.route('/')
def home():
    return render_template('Console.html')

@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        # DB_Controller.py 실행
        process = subprocess.run(["python3", "DB_Controller.py"], capture_output=True, text=True)
        # 결과 출력
        return f"DB_Controller Output: <pre>{process.stdout}</pre>", 200
    except Exception as e:
        return f"Error: {e}", 500

# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
