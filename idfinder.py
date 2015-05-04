#!/home/julius/Projects/facebook/idfinder/bin/python
import requests
import warnings
import sys
import re
import mechanize
import StringIO
from lxml import etree
from prettyprint import pp


class IDFinder:

    API = 'https://graph.facebook.com/v2.3'
    APP_ID = '369253336592554'
    APP_SECRET = '142a28496a7f69457c993638ddc58e3e'
    ACCESS_TOKEN = 'CAAFP1X31sKoBABusvrvhMHtFTCLxGNreGwWwNZAC2VtZBItYHGfPdZATfqG33t3pXk34dB55' + \
    'jegb5Um80ZCBNth0jhop1VKEtEdtWY7uHYju7SYF2TSilATPLbC5ehpUfh1iMZCowVC9rB4K5qSDqJ7N7BOHC1Ty' + \
    'jANBR3UEhIsRhPPlujnPDZCQVENVkwLLIN4qat8hRanQZAPHvNoD8GVRiodda2q3A0ZD'

    #Constructor
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.login()
        #self.checkToken()

    def checkToken(self):
        payload = {'access_token':self.ACCESS_TOKEN}
        request = requests.get(self.API+'/me', params=payload)
        response = request.json()
        if ('error' in response):
            print response['error']['message']
            self.getToken()

    def getToken(self):
        IDFinder.ACCESS_TOKEN = raw_input('Please enter new token: \n')

    def setSourceFile(self, filename):
        self.srcfilename = filename
		
    def getProfileID(self, args):
        # Hijack code. Only allow ON province.
        # There aren't much else to do for now.
        if(args['province'] != 'ON'):
            return

        args['province'] = 'ONTARIO'
        keywords = [args['name'], args['city'], args['province']]
        while(len(keywords) > 1):
            profiles = self.doRequest(keywords)
            if(len(profiles) == 0):
                keywords.pop()
            else:
                profile = profiles[0]
                profile['keyword'] = ' '.join(keywords)
                return profile
        else:
            profiles = self.doRequest(keywords)
            if(len(profiles)):
                profile = profiles[0]
                profile['keyword'] = ' '.join(keywords)
                return profile
        return

    def doRequest(self, args):
        keyword = ' '.join(args)
        payload = {'access_token':IDFinder.ACCESS_TOKEN, 'q':keyword, 'type':'user', 'limit':10}
        request = requests.get(self.API+'/search', params=payload)
        response = request.json()
        if('error' in response):
            print response['error']['message']
            self.getToken()
            return self.doRequest(args)
        else:
            return response['data']

    @staticmethod
    def printToken():
        print IDFinder.ACCESS_TOKEN

    def login(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.cookies = mechanize.CookieJar()

        #self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US)     AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36')]
        self.browser.open("http://m.facebook.com/")
        self.browser.select_form(nr=0)

        #self.browser.form['email'] = 'juliusmasigan@yahoo.com'
        self.browser.form['email'] = 'hack_julius@yahoo.com'
        self.browser.form['pass'] = 'jl.masigan'
        self.browser.submit()

    def getPicID(self, profile_id):
        url = "https://m.facebook.com/app_scoped_user_id/"+profile_id
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36')]
        html = self.browser.open(url).read()
        #pp(html)
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(html), parser)
        ids = tree.xpath("//div[@class='bl bm']/a/@href")
        if(not ids):
            ids = tree.xpath("//div[@class='bk bl']/a/@href")
            if(not ids):
                ids = tree.xpath("//div[@class='de']/a/@href")
                if(not ids):
                    ids = tree.xpath("//div[@class='bi cv']/a/@href")

        isID = re.search(r'id=[0-9]*', ids[0], re.M|re.I)
        if(isID):
            pid = isID.group()
            pp(pid)
            return pid.split('=')[1]
        else:
            isID = re.search(r'profile_id=[0-9]*', ids[0], re.M|re.I)
            pid = isID.group()
            return pid.split('=')[1]
        


a = IDFinder()
#a.getPicID('892795510777751')
a.setSourceFile(sys.argv[1])

f = open(a.srcfilename, 'r+')
f1 = open(re.sub(r'.csv$', '.tmp', a.srcfilename), 'w+')
line = f.readline()
while line:
    lsplit = line.split(',')
    name = ' '.join([lsplit[0].strip(' '), lsplit[1].strip(' ')])
    print name

    params = {
        'name':name.strip(' '), 
        'street':lsplit[2].strip(' '), 
        'city':lsplit[3].strip(' '), 
        'province':lsplit[4].strip(' '),
        'postal':lsplit[5].strip(' '), 
        'age':lsplit[6].strip(' '), 
        'gender':re.sub(r'^[\r\n]+|[\r\n]+$', '', lsplit[7]),
    }

    tmpline = [params['name'],params['street'],params['city'],params['province'],params['postal'],params['age'],params['gender']]

    profile = a.getProfileID(params)
    print str(profile)

    if(profile):
        #tmpline.append(profile['id'])
        tmpline.append(a.getPicID(profile['id']))
        tmpline.append(profile['keyword'])

    f1.write(','.join(tmpline)+'\n')
    line = f.readline()

f.close()
f1.close()
