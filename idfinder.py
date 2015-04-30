#!/home/julius/Projects/facebook/idfinder/bin/python
import requests
import warnings
import sys
import re
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



a = IDFinder()
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
        tmpline.append(profile['id'])
        tmpline.append(profile['keyword'])

    f1.write(','.join(tmpline)+'\n')
    line = f.readline()

f.close()
f1.close()
