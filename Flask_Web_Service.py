def run_db_controller():
    process = subprocess.Popen(
        ["python", "DB_Controller.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    print("DB_Controller.py started.")  # 디버깅 메시지

    # 출력 읽기 스레드
    def read_output():
        for line in iter(process.stdout.readline, ''):
            print(f"Captured output: {line.strip()}")  # 디버깅 메시지
            output_queue.put(line.strip())  # 줄바꿈 제거 후 큐에 추가
        process.stdout.close()

    # 에러 읽기 스레드
    def read_error():
        for line in iter(process.stderr.readline, ''):
            print(f"Captured error: {line.strip()}")  # 디버깅 메시지
            output_queue.put(line.strip())  # 에러도 큐에 추가
        process.stderr.close()

    threading.Thread(target=read_output, daemon=True).start()
    threading.Thread(target=read_error, daemon=True).start()

    # 입력 처리
    while True:
        try:
            user_input = input_queue.get(timeout=1)  # 입력 대기
            print(f"Sending input to DB_Controller.py: {user_input}")  # 디버깅 메시지
            process.stdin.write(user_input + '\n')
            process.stdin.flush()
        except Empty:
            if process.poll() is not None:  # 프로세스 종료 확인
                break
    process.stdin.close()
    process.wait()
    output_queue.put(f"Process finished with exit code {process.returncode}")
