from flask import Flask, request, render_template, jsonify
import subprocess, os, traceback

app = Flask(__name__)

# 루트 경로: Console.html 렌더링
@app.route('/')
def home():
    return render_template('Console.html')

# DB_Controller 실행
@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        # 절대 경로로 DB_Controller.py 실행
        script_path = os.path.abspath("DB_Controller.py")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # subprocess로 DB_Controller.py 실행
        process = subprocess.run(
            ["python", script_path, "1", "1"],  # 테스트로 '1', '1' 전달
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )

        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr}</pre>", 500

        # 표준 출력 내용을 클라이언트로 반환
        return jsonify({"output": process.stdout.strip()})

    except subprocess.TimeoutExpired:
        return "Error: DB_Controller.py execution timed out.", 500
    except Exception as e:
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
