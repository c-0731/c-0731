import os
import time
from win10toast import ToastNotifier
import requests
from bs4 import BeautifulSoup

__email__ = "c_blub@naver.com"

url = requests.get("https://www.vpngate.net/en")
soup = BeautifulSoup(url.content, "lxml")

td1 = soup.find('span', attrs={'id': 'Label_Table'})  # 페이지 테이블 뽑아오기
td2 = td1.find_all('td', attrs={'class': 'vg_table_row_1'})  # 페이지 테이블 서버 정보 빼오기
count = 0

sec = input("VPN이용할 시간을 입력해주세요 1시간 = 3600초 (초단위): ")

for td in td2:
    count = count + 1
    if count == 1:
        n = ToastNotifier()
        n.show_toast("- 알림 -", ">> " + td.text + " Server VPN에 연결중입니다!", duration=5)
        list = td.text
    if count == 2:
        os.system(str("PowerShell Add-VpnConnection 'NewVpn' '" + td.text[0:25] + "' -RememberCredential"))
        print("Add to Complete")
        os.system(str("rasdial NewVpn vpn vpn"))  # VPN 연결 시도
        n = ToastNotifier()
        n.show_toast("- 알림 -", ">> " + list + " Server VPN 연결에 성공했습니다!", duration=5)
        print("Connect to Complete")
        time.sleep(int(sec))
        os.system("rasdial /Disconnect\nPowerShell Remove-VpnConnection 'NewVpn'")
        n = ToastNotifier()
        n.show_toast("- 알림 -", ">> "+sec+"초 이용시간이 만료되어 " + list + " Server VPN연결을 종료합니다.", duration=5)
        print("Disconnect to Complete")
        break
