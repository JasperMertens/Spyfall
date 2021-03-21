from fbchat.models import *
import fbchat

from common import loadConfig
from getpass import getpass
from traceback import print_exception
import logging
import re
import json

SESSION_FILE = "session.json"

class FbChatter:
    # When pretend==True, do not send any messages
    def __init__ (self, pretend=False):
        self.pretend = pretend;
        self.client = None
        self.username = loadConfig()['Facebook']['username']
        self.userAgent = loadConfig()['Facebook']['user agent']
        self.client = self.startClientSession()

    def __enter__ (self):
        return self

    def __exit__ (self, exc_type, exc_value, traceback):
        self.saveSession()
        if exc_type is not None:
            # There was an exception
            print_exception(exc_type, exc_value, traceback)


    def startClientSession (self):
        # Hack: see https://github.com/fbchat-dev/fbchat/issues/638#issuecomment-800518857
        fbchat._state.FB_DTSG_REGEX = re.compile(r'"token":"(.*?)"')
    
        cookies = {}
        try:
            # Load the session cookies
             with open(SESSION_FILE, 'r') as f:
                 cookies = json.load(f)
             # Try loggin in with the cookies
             client = fbchat.Client(self.username, password="", user_agent=self.userAgent,
                                    session_cookies=cookies, max_tries=1)
             
        except:
            # If it fails, never mind, we'll just login again
            client = fbchat.Client(self.username, password=getpass(), user_agent=self.userAgent, max_tries=1)
            pass
    
        print("Session started with id: {}".format(client.uid))
        return client

    def saveSession (self):
        if not self.client.isLoggedIn():
            return # No valid session
        # Save the session again
        with open(SESSION_FILE, 'w') as f:
            json.dump(self.client.getSession(), f)

    def sendMessage (self, message, name):
        user = self.getFriend(name)
        print("Sending message to {} {}".format(user.first_name, user.last_name))
        if self.pretend:
            print("Message: {}".format(message))
        else:
            self.client.send(fbchat.Message(text=message),
                             thread_id=user.uid, thread_type=ThreadType.USER)
               
    def getFriend (self, name):
        user = self.client.searchForUsers(name)[0]
        if (not user.is_friend and user.uid != self.client.uid):
            raise Exception("""
            {} {} is not your friend on Facebook.
            Only messaging friends is allowed!
            Check that config.ini is set up correctly.
            """.format(user.first_name, user.last_name))

        return user
