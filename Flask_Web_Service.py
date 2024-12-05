from flask import Flask, request, jsonify
import subprocess, os, traceback

app = Flask(__name__)

@app.route('/run_db_controller', methods=['POST'])
def run_db_controller():
    try:
        function_selector = request.form.get('function_selector')
        os_selector = request.form.get('os_selector')

        if function_selector not in ['1', '2', '3']:
            return "Invalid function selector. Please select 1, 2, or 3.", 400

        if os_selector not in ['1', '2']:
            return "Invalid OS selector. Please choose 1 for IOS or 2 for IOS-XR.", 400

        # 절대 경로로 DB_Controller.py 실행
        script_path = os.path.abspath("DB_Controller_updated.py")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # DB_Controller.py 실행
        process = subprocess.run(
            ["python", script_path, function_selector, os_selector],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )

        if process.returncode != 0:
            return f"Error in DB_Controller: <pre>{process.stderr}</pre>", 500

        # 표준 출력 내용을 클라이언트로 반환
        return jsonify({"output": process.stdout})

    except subprocess.TimeoutExpired:
        return "Error: DB_Controller.py execution timed out.", 500
    except Exception as e:
        traceback.print_exc()
        return f"Unexpected error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
