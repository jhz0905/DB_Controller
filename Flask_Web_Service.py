from flask import Flask, render_template, request
import subprocess, traceback, os

# Flask 애플리케이션 생성
app = Flask(__name__)

# 첫 번째 라우트 생성
@app.route('/')
def home():
    return render_template('Console.html')

# Flask 애플리케이션 생성 전 현재 작업 디렉토리를 스크립트 위치로 변경
os.chdir(os.path.dirname(os.path.abspath(__file__)))

@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        # 절대 경로로 DB_Controller.py 실행
        script_path = os.path.abspath("DB_Controller.py")
        print("DB_Controller.py path:", script_path)

        process = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )

        # 실행 결과 처리
        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr}</pre>", 500
        return f"DB_Controller Output: <pre>{process.stdout}</pre>", 200
    except Exception as e:
        # Flask 터미널에 예외 출력
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500

# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
