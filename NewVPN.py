import os
import sys
import time
import requests
from bs4 import BeautifulSoup

__email__ = "c_blub@naver.com"

url = requests.get("https://www.vpngate.net/en")
soup = BeautifulSoup(url.content, "lxml")

td1 = soup.find('span', attrs={'id': 'Label_Table'})  # 페이지 테이블 뽑아오기
td2 = td1.find_all('td', attrs={'class': 'vg_table_row_1'})  # 페이지 테이블 서버 정보 빼오기
count = 0

for td in td2:
    count = count + 1
    if count == 1:
        a = open("VPN연결정보.txt", "w")  # VPN 연결정보 작성
        a.write(str(sys.argv[0]) + "\n\nCountry : " + td.text + "\n")
        a.close()
    if count == 2:
        a = open("VPN연결정보.txt", "a")
        a.write("Server : " + td.text[0:25] + "\n")
        a.close()
        os.system(str("PowerShell Add-VpnConnection 'NewVPN' '" + td.text[0:25] + "' -RememberCredential"))
        time.sleep(2)
        print("Add to Complete")
        os.system(str("rasdial NewVPN vpn vpn"))  # VPN 연결 시도
        print("Connect to Complete")
    if count == 4:
        a = open("VPN연결정보.txt", "a")
        a.write("Speed : " + str(td.text).split("Ping")[0] + "\n")
        a.close()
    if count == 10:
        print("Disconnect.bat in th Folder : "+str(sys.argv[0].rsplit('\\', 1)[0]))
        a = open("VPN Disconnect.bat", "w")  # 연결 끊는 .bat 스크립트가 저장된 경로에 생성
        a.write("rasdial /Disconnect\nPowerShell Remove-VpnConnection 'NewVpn'")
        a.close()
        print("Finish")
        break
