import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 호텔 검색 URL
HOTEL_URLS = {
    "신토신": "https://www.toyoko-inn.com/korea/search/result?"
              "lcl_id=ko&chck_in=2025/03/29&inn_date=1&rsrv_num=1&sel_ldgngPpl=1"
              "&sel_area=18&sel_area_txt=%EC%82%AC%EC%9D%B4%ED%83%80%EB%A7%88"
              "&sel_htl=00121&rd_smk=0&sel_room_clss_Id=10&sel_prkng=&sel_cnfrnc="
              "&sel_hrtfll_room=&srch_key_word=&lttd=&lngtd=&pgn=1&sel_dtl_cndtn=&prcssng_dvsn=dtl&",
    "오미야": "https://www.toyoko-inn.com/korea/search/result?"
              "lcl_id=ko&chck_in=2025/03/29&inn_date=1&rsrv_num=1&sel_ldgngPpl=1"
              "&sel_area=18&sel_area_txt=%EC%82%AC%EC%9D%B4%ED%83%80%EB%A7%88"
              "&sel_htl=00334&rd_smk=0&sel_room_clss_Id=10&sel_prkng=&sel_cnfrnc="
              "&sel_hrtfll_room=&srch_key_word=&lttd=&lngtd=&pgn=1&sel_dtl_cndtn=&prcssng_dvsn=dtl&"
}

# Gmail 계정 정보
EMAIL_ADDRESS = "shpark199@gmail.com"  # 발신자 Gmail 주소
EMAIL_PASSWORD = "nmvc wsma qqqv wnco"   # Gmail 앱 비밀번호
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USER_EMAIL = "skpark196@naver.com"  # 수신자 이메일 주소

def check_discount_availability(hotel_name, url):
    """
    특정 호텔 URL에서 "할인가격"이라는 문구를 확인하여 빈 방 여부를 반환합니다.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if "할인가격" in response.text:
                return True  # 빈 방 있음
            return False  # 빈 방 없음
        else:
            raise Exception(f"Failed to fetch page for {hotel_name}: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while checking {hotel_name}: {e}")
        return False

def send_email(subject, body):
    """
    Gmail을 사용해 이메일 알림을 보내는 함수.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = USER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # TLS 연결 시작
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # 로그인
            server.send_message(msg)
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    start_time = datetime.now()  # 시작 시간 기록
    max_duration = timedelta(hours=6)  # 최대 실행 시간: 6시간

    while True:  # 무한 루프 시작
        try:
            # 실행 시간 확인
            elapsed_time = datetime.now() - start_time
            if elapsed_time > max_duration:
                print("6시간이 경과하여 스크립트를 종료합니다.")
                break  # 루프 종료

            # 두 호텔의 예약 가능 여부 확인
            availability = {hotel_name: check_discount_availability(hotel_name, url)
                            for hotel_name, url in HOTEL_URLS.items()}
            
            # 이메일 제목 및 메시지 작성
            body = ""
            if availability["신토신"] and availability["오미야"]:
                subject = "신토신, 오미야 둘 다 빈 방 있음"
                body = (
                    "토요코인 사이타마 신토신과 토요코인 오미야 에키 히가시구치 둘 다 빈 방이 있습니다!\n\n"
                    "신토신 예약 확인: {신토신}\n"
                    "오미야 예약 확인: {오미야}"
                ).format(신토신=HOTEL_URLS["신토신"], 오미야=HOTEL_URLS["오미야"])
            elif availability["신토신"]:
                subject = "토요코인 사이타마 신토신 빈 방 있음"
                body = (
                    "토요코인 사이타마 신토신에 빈 방이 있습니다!\n\n"
                    "신토신 예약 확인: {신토신}"
                ).format(신토신=HOTEL_URLS["신토신"])
            elif availability["오미야"]:
                subject = "토요코인 오미야 에키 히가시구치 빈 방 있음"
                body = (
                    "토요코인 오미야 에키 히가시구치에 빈 방이 있습니다!\n\n"
                    "오미야 예약 확인: {오미야}"
                ).format(오미야=HOTEL_URLS["오미야"])
            else:
                print("두 호텔 모두 빈 방이 없습니다.")
                time.sleep(60)  # 1분 대기 후 다시 확인
                continue  # 다음 반복으로 이동
            
            # 이메일 보내기
            send_email(subject, body)
        except Exception as e:
            print(f"Error: {e}")
        
        # 1분 대기 후 다시 실행
        print("Waiting for 1 minute before checking again...")
        time.sleep(60)