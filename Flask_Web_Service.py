from flask import Flask, render_template, request
import subprocess, traceback, os, sys, io

# Flask 애플리케이션 생성
app = Flask(__name__)

# 첫 번째 라우트 생성
@app.route('/')
def home():
    return render_template('Console.html')

# Flask 애플리케이션 생성 전 현재 작업 디렉토리를 스크립트 위치로 변경
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 표준 출력 및 표준 에러를 UTF-8로 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        # 절대 경로로 DB_Controller.py 실행
        script_path = os.path.abspath("DB_Controller.py")
        print("DB_Controller.py path:", script_path)

        # UTF-8 환경 변수 설정
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )

        # 디버그 출력
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)

        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr or 'No error message'}</pre>", 500
        return f"DB_Controller Output: <pre>{process.stdout or 'No output generated'}</pre>", 200
    except subprocess.TimeoutExpired:
        return "Error: DB_Controller.py execution timed out.", 500
    except Exception as e:
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500

# 웹 서버 실행
if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
