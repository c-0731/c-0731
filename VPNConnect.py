import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

__email__ = "c_blub@naver.com"
n = ToastNotifier()

command = input("1.연결, 2.종료: ")
url = requests.get("https://www.vpngate.net/en")
soup = BeautifulSoup(url.content, "lxml")

td1 = soup.find('span', attrs={'id': 'Label_Table'})  # 페이지 테이블 뽑아오기
td2 = td1.find_all('td', attrs={'class': 'vg_table_row_1'})  # 페이지 테이블 서버 정보 빼오기
count = 0

if command == "1":
    sec = int(input("VPN이용할 시간을 입력해주세요 1시간 = 3600초 (초단위): "))  # 초단위로 입력
    for td in td2:
        count = count + 1
        if count == 1:
            n.show_toast("- 알림 -", ">> " + td.text + " Server VPN에 연결중입니다!", duration=5)
            list = td.text
        if count == 2:
            os.system(str("PowerShell Add-VpnConnection NewVpn '" + td.text[0:25] + "' -RememberCredential"))
            print("Add to Complete")
            os.system(str("rasdial NewVpn vpn vpn"))  # VPN 연결 시도
            time.sleep(3)
            n.show_toast("- 알림 -", ">> " + list + " Server VPN 연결에 성공했습니다!", duration=5)
            print("Connect to Complete")
            time.sleep(sec/3)
            n.show_toast("- 알림 -", ">> VPN 사용시간 " + str(int(sec)-sec//3) + "초 남았습니다.", duration=5)
            time.sleep(sec/3)
            n.show_toast("- 알림 -", ">> VPN 사용시간 " + str(sec//3) + "초 남았습니다.", duration=5)
            time.sleep(sec/3)
            print("Disconnection Timeout")
            n.show_toast("- 알림 -", ">> " + str(sec) + "초 이용시간이 만료되어 " + list + " Server VPN연결을 종료합니다.", duration=5)
            os.system("rasdial /Disconnect")
            time.sleep(2)
            os.system("PowerShell Remove-VpnConnection NewVpn -Force")
            time.sleep(2)
            print("Disconnect to Complete")
            sys.exit()

if command == "2":
    os.system("rasdial /Disconnect")
    time.sleep(2)
    os.system("PowerShell Remove-VpnConnection NewVpn -Force")
    print("Disconnect to Complete")
    n.show_toast("- 알림 -", ">> 연결중인 VPN을 종료합니다.", duration=5)
    sys.exit()

if command == "":
    print("명령어 숫자를 입력해주세요")
    sys.exit()