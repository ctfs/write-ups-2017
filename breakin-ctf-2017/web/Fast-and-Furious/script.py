import mechanize

URL = 'https://felicity.iiit.ac.in/contest/extra/fastandfurious/'

br = mechanize.Browser()
br.open(URL)

count = 1
while True:
    res = br.response().read()
    if count > 200:
        print res
        break
    print res.split(':')[0].split('>')[1].split('<')[0],
    ans = eval(res.split(':')[1].split('<')[0].strip(' '))
    print ans
    br.select_form(nr=0)
    br.form['ques_ans'] = str(ans)
    br.submit()
    count += 1
