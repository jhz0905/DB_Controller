from flask import Flask, render_template, request
import subprocess, traceback, os

# Flask 애플리케이션 생성
app = Flask(__name__)

# 첫 번째 라우트 생성
@app.route('/')
def home():
    return render_template('Console.html')

@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        DB_Controller_path = os.path.abspath("DB_Controller.py")
        # DB_Controller.py 실행
        process = subprocess.run(
            ["python", DB_Controller_path], 
            capture_output=True, 
            text=True
        )
        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr}</pre>", 500
        return f"DB_Controller Output: <pre>{process.stdout}</pre>", 200
    except Exception as e:
        # 상세한 에러 메시지와 스택 트레이스를 터미널에 출력
        print("An error occurred while processing the request:")
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500

# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
