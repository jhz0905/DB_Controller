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
        # 디버깅 출력: 현재 작업 디렉토리
        print("Current working directory:", os.getcwd())

        script_path = os.path.abspath("DB_Controller.py")
        print("DB_Controller.py path:", script_path)

        # UTF-8 환경 변수 설정
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            env=env
            timeout = 30
        )

        # 디버깅 출력: 실행 결과
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)

        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr or 'Unknown error'}</pre>", 500
        return f"DB_Controller Output: <pre>{process.stdout or 'No output'}</pre>", 200
    except subprocess.TimeoutExpired:
        print("Error: DB_Controller.py execution timed out.")
        return "Error: DB_Controller.py execution timed out.", 500
    except Exception as e:
        print("An unexpected error occurred:")
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500


# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
