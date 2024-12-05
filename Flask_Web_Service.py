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
        # 클라이언트에서 전달된 데이터 받기
        data = request.get_json()
        function_selector = data.get('function_selector')
        os_selector = data.get('os_selector')

        if function_selector not in ['1', '2', '3']:
            return jsonify({"output": "Invalid function selector. Please select 1, 2, or 3."}), 400
        if os_selector not in ['1', '2']:
            return jsonify({"output": "Invalid OS selector. Please choose 1 for IOS or 2 for IOS-XR."}), 400

        # DB_Controller.py 실행
        script_path = os.path.abspath("DB_Controller.py")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.run(
            ["python", script_path, function_selector, os_selector],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )

        if process.returncode != 0:
            return jsonify({"output": process.stderr}), 500

        return jsonify({"output": process.stdout})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "DB_Controller.py execution timed out."}), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"output": str(e)}), 500

if __name__ == "__main__":
    app.run(host="10.12.100.150", port=5000, debug=True)
