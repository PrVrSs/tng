import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

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
page1 = br.open("https://www.hackthissite.org/missions/prog/1/")
soup = BeautifulSoup(page1)
movie = soup.findAll('li')
a = []
b = 0
for i in range(10):
    c = movie[len(movie) - 10 + i]
    a.append(str(c))
    a[b] = a[b][4:len(str(c)) - 5]
    b += 1
nn = []
nnn = dict()
wordlistFile = open('')
for line in wordlistFile.readlines():
    passw = line.strip('\r\n')
    passwLen = len(passw)
    countDict = 0
    for line1 in a:
        word_list = line1.strip('\n')
        word_list_len = len(word_list)
        count = 0
        if passwLen != word_list_len:
            countDict += 1
            continue
        for symbol in passw:
            ss = 0
            for symbol1 in word_list:
                if symbol1 == symbol:
                    word_list = word_list[:ss] + word_list[ss + 1:]
                    count += 1
                    break
                ss += 1
        countDict += 1
        if count >= passwLen:
            nnn[countDict - 1] = passw
            break
for i in range(10):
    nn.append(nnn[i])
br.select_form(nr=0)
br["solution"] = ','.join(nn)
br.submit(name="submitbutton")
