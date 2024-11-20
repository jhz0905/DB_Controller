import pymysql, msvcrt

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

function_selector = ''
os_selector = ''
log_list = list()

while True:
    key = msvcrt.getch()  # 키 입력 대기
    if key == b'\r':  # Enter 키 감지 (b'\r'은 엔터 키)
        print("initializing...")
        print("\n")
        print("\n")
        print("\n")
        break
    else:
        print("Please press Enter")

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
            print("Query Results:")
            for row in results:
                print(row)

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
        print("\n데이터 추가 모드를 실행합니다.")
        print("\n##### 입력 모드 실행 중(아래에 입력 해 주세요). #####")
        print("* exit를 입력하면 입력 모드를 종료합니다. *")

        while True:
            log_list.append(input("> "))
            if log_list[-1] == "exit":
                log_list.pop()
                break

    # 데이터 삭제 기능
    elif function_selector == '3':
        # ID 재정렬
        print("Resetting AUTO_INCREMENT values...")
        
        # 1단계: AUTO_INCREMENT 값 재설정
        cursor.execute("ALTER TABLE iosxr AUTO_INCREMENT = 1;")
        
        # 2단계: ID 컬럼 값 재정렬
        cursor.execute("SET @COUNT = 0;")
        cursor.execute("UPDATE iosxr SET id = @COUNT:= @COUNT + 1;")

        # 변경 사항 저장
        conn.commit()
        print("AUTO_INCREMENT values reset successfully.")
    else:
        pass


except pymysql.MySQLError as e:
    print(f"Error occurred: {e}")

finally:
    # 커서 및 연결 닫기
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
