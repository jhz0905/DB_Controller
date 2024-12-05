import pymysql, re, sys

print("Step 1: Script started.")

def execute_db_task(function_selector, os_selector):
    try:
        # MySQL에 연결
        conn = pymysql.connect(
            host='10.12.100.150',  # MySQL 서버 IP
            port=3306,             # MySQL 포트
            user='root',           # MySQL 사용자 이름
            password='cisco123',   # MySQL 비밀번호
            database='logdb',      # MySQL 데이터베이스 이름
            connect_timeout=10     # 타임아웃 설정
        )
        print("Database connected successfully.")
        cursor = conn.cursor()

        # 데이터 조회 기능
        if function_selector == '1':
            query = "SELECT * FROM ios" if os_selector == '1' else "SELECT * FROM iosxr"
            cursor.execute(query)
            results = cursor.fetchall()

            # 결과를 포맷된 문자열로 가공
            query_results = "\n".join(
                f"ID: {row[0]}, Title: {row[1]}, Date Added: {row[2].strftime('%Y-%m-%d %H:%M:%S')}"
                for row in results
            )

            print("Query Results:")
            print(query_results)  # 터미널 출력용
            return query_results  # Flask 또는 다른 호출자로 반환

        # 데이터 추가 기능
        elif function_selector == '2':
            print("Insert functionality not implemented yet.")
            return "Insert functionality not implemented."

        # 데이터 삭제 기능
        elif function_selector == '3':
            print("Delete functionality not implemented yet.")
            return "Delete functionality not implemented."

        else:
            print("Invalid function selector.")
            return "Invalid function selector."

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return f"Database error: {e}"

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            print("Connection closed.")

# Standalone test
if __name__ == "__main__":
    print("Step 2: Simulating task execution.")
    function_selector = sys.argv[1] if len(sys.argv) > 1 else '1'
    os_selector = sys.argv[2] if len(sys.argv) > 2 else '1'

    # execute_db_task 호출 후 터미널에 결과를 출력하지 않음
    result = execute_db_task(function_selector, os_selector)
    print("Execution complete.")  # 간단한 실행 완료 메시지만 출력
