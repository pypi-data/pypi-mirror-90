from licensing import methods
from licensing.methods import Helpers
import hashlib
import base64
import os, sys, requests
        
class slab:
    @staticmethod
    def auth(auth_id):
        global r
        r=requests.get('https://pastebin.com/'+auth_id)
    @staticmethod
    def user_id():
        print('USER ID:'+Helpers.GetMachineCode())
    @staticmethod
    def verify(username, password, key):
        try:
            #r=requests.get('https://pastebin.com/'+auth_id)
            ke=Helpers.GetMachineCode()
            co=ke.encode('utf-8')
            k=hashlib.md5(co)
            e=k.hexdigest()
            KEY=e.upper()
            info=username+'\n'+password
            ok=info.encode('utf-8')
            say=hashlib.md5(ok)
            h=say.hexdigest()
            if h in r.text:
                if key==KEY:
                    if e in r.text:
                        os.system('cls' if os.name=='nt' else 'clear')
                    else:
                        print('Invalid Account')
                        sys.exit()
                else:
                    print('Please Use Your Device Or Key!')
                    sys.exit()
            else:
                print('Invalid Username Or Password!')
                sys.exit()
        except requests.ConnectionError:
            print('Please Turn On NetWork Connection!')
            sys.exit() 
    
