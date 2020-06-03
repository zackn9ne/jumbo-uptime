#!/usr/bin/python
# finds computers that have uptime issues and warns them

import os.path
from os import path
import subprocess
import re

LOGOPATH = '/System/Library/PreferencePanes/DateAndTime.prefPane/Contents/Resources/DateAndTime.icns'
limit  = 20
instructs = 'email support@awesomecompany.nyc'

class popupWindow:
    # build class
    def __init__(self, name):
        self.name = name
        
    def buildWindow(self, windowStyle, heading, title, message, *args):
        icon = "{}".format(LOGOPATH)    
        if not os.path.exists(icon):
            icon = "/System/Library/CoreServices/Problem Reporter.app/Contents/Resources/ProblemReporter.icns"
        window = [
            "/Library/Application Support/JAMF/bin/jamfHelper.app/Contents/MacOS/jamfHelper",
            "-windowType",
            windowStyle, #hud #utility #fullscreen
            "-heading",
            heading,
            "-title",
            title,
            "-description",
            message, #what do you wanna say
            "-icon",
            icon,
        ]
        for ar in args:
            window.append(ar)
        return window

    #feed me the popupWindow.buldWindow as an arg
    def fireWindow(self, popup_type):
        self.proc = subprocess.Popen(popup_type, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.out, self.err = self.proc.communicate()

        print "User clicks:", self.out
        if self.proc.returncode == 0:
            return True
        if self.proc.returncode == 2:
            return False
        else:
            return False
            print("Error: %s" % self.proc.returncode)

def uptimeNotAcceptable():
    global days


    raw = subprocess.check_output('uptime').replace(',','')
    days = int(raw.split()[2])
    if 'min' in raw:
    	days = 0

    print 'uptime is: ', days
    
    if days >= limit:
        return True



def main():
    uptimeNotAcceptable()
    
    print 'checking uptime please wait...', days
    
    if uptimeNotAcceptable():  
        p = popupWindow('restartNeeded')
        p = p.fireWindow(p.buildWindow('hud', 'Restart Needed', 'Current Uptime {} days'.format(days), '''It is our IT policy that your computer needs to be restarted every {} days. 

Please save your work and select Apple Menu >> Restart... as soon as possible...

If you feel you have reached this message in error {}'''.format(limit, instructs), '-button1', 'AGREE', '-defaultbutton', '1',))

if __name__ == "__main__":
#    buildPromptVars(typeOneWindow)
    main()
