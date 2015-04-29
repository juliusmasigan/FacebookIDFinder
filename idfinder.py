#!/home/julius/Projects/facebook/idfinder/bin/python
import requests
import warnings
import sys
from prettyprint import pp


class IDFinder:

    API = 'https://graph.facebook.com/v2.3';
    APP_ID = '369253336592554'
    APP_SECRET = '142a28496a7f69457c993638ddc58e3e'
    ACCESS_TOKEN = 'CAAFP1X31sKoBABusvrvhMHtFTCLxGNreGwWwNZAC2VtZBItYHGfPdZATfqG33t3pXk34dB55' + \
    'jegb5Um80ZCBNth0jhop1VKEtEdtWY7uHYju7SYF2TSilATPLbC5ehpUfh1iMZCowVC9rB4K5qSDqJ7N7BOHC1Ty' + \
    'jANBR3UEhIsRhPPlujnPDZCQVENVkwLLIN4qat8hRanQZAPHvNoD8GVRiodda2q3A0ZD'

    #Constructor
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.checkToken()

    def checkToken(self):
        payload = {'access_token':self.ACCESS_TOKEN}
        request = requests.get(self.API+'/me', params=payload)
        response = request.json()

        if (response['error']):
            print response['error']['message']
            self.getToken()

    def getToken(self):
        IDFinder.ACCESS_TOKEN = raw_input('Please enter new token: \n')

    @staticmethod
    def printToken():
        print IDFinder.ACCESS_TOKEN

    def setSourceFile(self, filename):
        self.srcfilename = filename
        fhandle = open(self.srcfilename, 'r+')
        
        line = fhandle.readline()
        while line:
            print line
            line = fhandle.readline()
        fhandle.close()


a = IDFinder()
filename = raw_input('File: \n')
a.setSourceFile(filename)
