import os
import optparse
from PIL import Image, ImageDraw
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

from mechanize import ParseResponse, urlopen

br = mechanize.Browser()
br.set_handle_robots(False)
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

page = br.open("https://www.hackthissite.org/")

br.select_form(nr=0)
br["username"] = ""
br["password"] = ""
br.submit(name="btn_submit")
if 'Redirecting' in br.title():
    resp = br.follow_link(text_regex='click here')

page1 = br.open("https://www.hackthissite.org/missions/prog/2/")
soup = BeautifulSoup(page1)
movie = soup.find('img', {'src':'/missions/prog/2/PNG'})

print(movie['src'])
filename = os.path.join("/hackthissite/4.png")
print('[+] Saving ' + str(filename))
data = br.open(movie['src']).read()
br.back()
save = open(filename, 'wb')
save.write(data)
save.close()

Morze = dict(zip([".-", "-...", "-.-.",
                  "-..", ".", "..-.",  # DEF
                  "--.", "....", "..",  # GHI
                  ".---", "-.-", ".-..",  # JKL
                  "--", "-.", "---",  # MNO
                  ".--.", "--.-", ".-.",  # PQR
                  "...", "-", "..-",  # STU
                  "...-", ".--", "-..-",  # VWX
                  "-.--", "--..", ".----",  # YZ1
                  "..---", "...--", "....-",  # 234
                  ".....", "-....", "--...",   # 567
                  "---..", "----.", "-----", ".-."], ['A', 'B', 'C',
                                                      'D', 'E', 'F',
                                                      'G', 'H', 'I',
                                                      'J', 'K', 'L',
                                                      'M', 'N', 'O',
                                                      'P', 'Q', 'R',
                                                      'S', 'T', 'U',
                                                      'V', 'W', 'X',
                                                      'Y', 'Z', '1',
                                                      '2', '3', '4',
                                                      '5', '6', '7',
                                                      '8', '9', '0']))

image = Image.open("/hackthissite/4.png")
draw = ImageDraw.Draw(image)
width = image.size[0]
height = image.size[1]
pix = image.load()
count1 = 0
a = 0
str = ''
str2 = ''
for i in range(height):
    for j in range(width):
        if pix[j, i] == 0:
            count1 += 1
        else:
            if count1-a != 32:
                if count1-a == 46:
                    str += '.'
                else:
                    str += '-'
            else:
                str2 +=Morze[str]
                str = ''
            a = count1
            count1 += 1
print(str2)

br.select_form(nr=0)
br["solution"] = str2
br.submit(name="submitbutton")
