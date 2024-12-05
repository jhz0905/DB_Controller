import pymysql, msvcrt, re, os, sys
import curses # noqa

print("Step 1: Script started.")

print("----------------------------------------------------------")
print("|                               Last Update 2024. 11. 20 |")
print("|                                                        |")
print("|                                                        |")
print("|                   DB Controller v1.0                   |")
print("|                                                        |")
print("|                  Made By HyeonJoon Jo                  |")
print("|                                                        |")
print("----------------------------------------------------------")

print("Press Enter to Continue")

function_selector = ''  # 기능 선택 변수
os_selector = ''        # 운영체제 선택 변수
log_list = list()       # 로그 리스트 (사용자 입력 저장용)
query = ''              # SQL 쿼리 문자열 변수
results = []            # SQL 쿼리 결과 저장 리스트
iosxr_log_pattern = r"%\w+-\w+-\d-\w+"     #log pattern
ios_log_pattern = r"%\w+-\d-\w+"     #log pattern

print("----------------------------------------------------------")
print("|                       [ 1 ] 조회                       |")
print("|                       [ 2 ] 추가                       |")
print("|                       [ 3 ] 삭제                       |")
print("----------------------------------------------------------")

while True:
    function_selector = input("원하는 기능을 입력 해 주세요. (Ex. 1) : ")
    if function_selector in ['1', '2', '3']:
        break
    else:
        print("\n1 ~ 3 까지의 숫자만 입력해주세요.")

print("\n----------------------------------------------------------")
print("|         조회/수정 할 운영체제를 선택 해 주세요.        |")
print("|                       [ 1 ] IOS                        |")
print("|                       [ 2 ] IOS-XR                     |")
print("----------------------------------------------------------")

while True:
    os_selector = input("조회 할 운영체제를 입력 해 주세요. (Ex. 1) : ")
    if os_selector in ['1', '2']:
        break
    else:
        print("\n1 ~ 2 까지의 숫자만 입력해주세요.")

#################### 기능 구현 ######################
try:
    # MySQL에 연결
    conn = pymysql.connect(
        host='10.12.100.150',  # MySQL 서버 IP
        port=3306,             # MySQL 포트
        user='root',           # MySQL 사용자 이름
        password='cisco123',   # MySQL 비밀번호
        database='logdb'       # MySQL 데이터베이스 이름
    )

    # 커서 생성
    cursor = conn.cursor()
    
    # 데이터 조회 기능
    if function_selector == '1':

        # 데이터 조회(IOS)
        if os_selector == '1':

            query = "SELECT * FROM ios;"  
            cursor.execute(query)

            # 결과 가져오기
            results = cursor.fetchall()
            print("\nQuery Results:")
            for row in results:
                print(f"ID: {row[0]}, Title: {row[1]}, Date Added: {row[2].strftime('%Y-%m-%d %H:%M:%S')}")

        # 데이터 조회(IOS-XR) 
        elif os_selector == '2':
   
            query = "SELECT * FROM iosxr;"  
            cursor.execute(query)

            # 결과 가져오기
            results = cursor.fetchall()
            print("Query Results:")
            for row in results:
                print(row)

    # 데이터 추가 기능
    elif function_selector == '2':
        print("\n데이터 추가를 위해 입력 모드를 실행합니다.")
        print("\n##### 입력 모드 실행 중(아래에 입력 해 주세요). #####")
        print("* exit를 입력하면 입력 모드를 종료합니다. *")

        while True:
            qurey_title = ''
            log_list.append(input("> "))

            if log_list[-1] != "exit":
                if os_selector == "1":
                    if not re.search(ios_log_pattern, log_list[-1]):
                        print("입력한 문자열이 유효하지 않습니다. 형식: %문자-숫자-문자")
                        log_list.pop()  # 잘못된 입력 제거
                    else:    
                        query = "INSERT IGNORE INTO ios (title) VALUES (%s);"
                        query_title = re.search(ios_log_pattern, log_list[-1]).group()
                        cursor.execute(query, (query_title,))
                if os_selector == "2":
                    if not re.search(iosxr_log_pattern, log_list[-1]):
                        print("입력한 문자열이 유효하지 않습니다. 형식: %문자-문자-숫자-문자")
                        log_list.pop()  # 잘못된 입력 제거
                    else:    
                        query = "INSERT IGNORE INTO iosxr (title) VALUES (%s);"
                        query_title = re.search(iosxr_log_pattern, log_list[-1]).group()
                        cursor.execute(query, (query_title,))

            elif log_list[-1] == "exit":
                log_list.pop()
                break

    # 데이터 삭제 기능(기능 구현 중)
    elif function_selector == '3':
        pass

    else:
        pass


except pymysql.MySQLError as e:
    print(f"\nError occurred: {e}")
    print("DB와 연결이 실패했습니다. 확인해주세요.")

finally:
    # ID 재정렬
    print("\nResetting AUTO_INCREMENT values...")
        
    # 1단계: AUTO_INCREMENT 값 재설정
    cursor.execute("ALTER TABLE iosxr AUTO_INCREMENT = 1;")
    cursor.execute("ALTER TABLE ios AUTO_INCREMENT = 1;")
        
    # 2단계: ID 컬럼 값 재정렬
    cursor.execute("SET @COUNT = 0;")
    cursor.execute("UPDATE iosxr SET id = @COUNT:= @COUNT + 1;")
    cursor.execute("SET @COUNT = 0;")
    cursor.execute("UPDATE ios SET id = @COUNT:= @COUNT + 1;")

    # 변경 사항 저장
    print("AUTO_INCREMENT values reset successfully.")

    # 커서 및 연결 닫기
    conn.commit()
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
