import mechanize
import cookielib
from bs4 import BeautifulSoup

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
page1 = br.open("https://www.hackthissite.org/missions/prog/11/")
soup = BeautifulSoup(page1, "lxml")
movie = soup.findAll('td')
a = str(movie).index("Generated String:")
data = ""
for index in str(movie)[a+18:]:
    if index == "<":
        break
    data += index
b = str(movie).index("Shift: ")
shift = ''
for index in str(movie)[b+7:]:
    if index == "<":
        break
    shift += index
for index in data:
    if ord(index) < 48 or ord(index) > 57:
        razd = index
        break
answer = ''
for index in data.split(razd)[:-1]:
    answer += chr(int(index) - int(shift))
br.select_form(nr=0)
br["solution"] = answer
br.submit(name="submitbutton")
