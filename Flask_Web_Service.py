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
        # Flask의 현재 디렉토리 출력
        print("Current working directory:", os.getcwd())
        
        # 절대 경로 확인
        script_path = os.path.abspath("DB_Controller.py")
        print("DB_Controller.py path:", script_path)

        # DB_Controller.py 실행
        process = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )

        # 실행 결과 출력
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)

        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr}</pre>", 500
        return f"DB_Controller Output: <pre>{process.stdout}</pre>", 200
    except Exception as e:
        # 예외 처리와 디버그 정보 출력
        print("An error occurred while processing the request:")
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500


# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
