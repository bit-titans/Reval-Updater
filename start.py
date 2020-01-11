import requests
from lxml import html
import ocr
from bs4 import BeautifulSoup
import mysql.connector 
import xlrd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
i = 1
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="admin123",
auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor()
mycursor.execute("use MyDB")
loc = ("USN.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
while i<=199:
    try:
        USN = "1BI18CS"+str(format(i, '03d'))
        batch = USN[3:5]
    except:
        break
    s = requests.Session()
    headers = {'Referer': 'https://results.vtu.ac.in/vitavicbcsrevaljj19/index.php',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
                     'Cookie': 'PHPSESSID=u7l9ighsavqvqs9ecd4ltu6t81'
            , 'Connection': 'keep-alive',
            'Origin': 'https://results.vtu.ac.in',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'results.vtu.ac.in'}
   
    image = s.get("https://results.vtu.ac.in/vitavicbcsrevaljj19/captcha_new.php", headers=headers, verify=False)
    with open("snap.png", 'wb') as file:
        file.write(image.content)
    cap = ocr.get_ocr("snap.png")
    #USN = "1BI17CS"+str(format(i, '03d'))
    url = "https://results.vtu.ac.in/vitavicbcsrevaljj19/resultpage.php"
    page = s.get('https://results.vtu.ac.in/vitavicbcsrevaljj19/index.php',verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    token = soup.find('input',attrs = {'id':'tokenid'})
    token = token['value']
    payload = {'MIME Type': 'application/x-www-form-urlencoded',
                'lns': USN, 'captchacode': str(cap),
                   'token': token,
                   'current_url': 'https://results.vtu.ac.in/vitavicbcsrevaljj19/index.php'}
    page = s.post(url, data=payload, headers=headers, verify=False)
    soup = BeautifulSoup(page.content,'html.parser')
    if "Invalid captcha code !!!" in page.text:
        continue
    if "Redirecting to VTU Results Site" in page.text:
        continue
    if "University Seat Number is not available or Invalid..!" in page.text:
        i += 1
        continue
    table = soup.find('div',attrs={'class':'divTable'})
    rows = table.find_all('div',attrs={'class','divTableRow'})
    rows = rows[1:]
    for j in rows:
       cols =  j.find_all('div', attrs={'class':'divTableCell'})
       print(USN + ":"+ cols[0].text + ":" + cols[2].text)
       sql = 'INSERT INTO reval(USN,subcode,new_marks) VALUES (%s, %s, %s)'
       val = (USN,cols[0].text,int(cols[2].text))
       mycursor = mydb.cursor()
       mycursor.execute(sql, val)
       mydb.commit()
       print(mycursor.rowcount, "record inserted.")
    i += 1
    