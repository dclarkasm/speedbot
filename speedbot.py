#!/usr/bin/python
# speedbot.py
# Script to monitor internet speed and tweet it periodically
# Author: Devon Clark
# 2017
import time
import datetime
from pyspeedtest import SpeedTest
from twitter import *
from ConfigParser import SafeConfigParser

# * * * * * * * * * * INI Configs
Config = SafeConfigParser()
Config.read('config.ini')

tMin = Config.getfloat('Configs', 'tMin')   # time delay between speed tests in minutes
logFileFmt = Config.get('Configs', 'logFileFmt')
token = Config.get('Configs', 'token')
tokenSecret = Config.get('Configs', 'tokenSecret')
consumerKey = Config.get('Configs', 'consumerKey')
consumerSecret = Config.get('Configs', 'consumerSecret')
pingLThresh = Config.getfloat('Configs', 'pingLThresh')
downLThresh = Config.getfloat('Configs', 'downLThresh')
upLThresh = Config.getfloat('Configs', 'upLThresh')
pingHThresh = Config.getfloat('Configs', 'pingHThresh')
downHThresh = Config.getfloat('Configs', 'downHThresh')
upHThresh = Config.getfloat('Configs', 'upHThresh')
tweetEn = Config.getboolean('Configs', 'tweetEn')
locale = Config.get('Configs', 'locale')
ispTwitter = Config.get('Configs', 'ispTwitter')
plan = Config.get('Configs', 'plan')
tags = Config.get('Configs', 'tags')
tagISPEn = Config.getboolean('Configs', 'tagISPEn')

# file initialization
logFileNm = time.strftime(logFileFmt, time.localtime())
print('Speed test log file: ' + logFileNm)
logFile = open(logFileNm, 'w')

# twitter
t = Twitter(auth=OAuth(token, tokenSecret, consumerKey, consumerSecret))

# speed test
st = SpeedTest()   # the speed test object

if __name__ == '__main__':
    try:
        while 1:
            try:
                utime = time.time()
                ping = st.ping()
                down = st.download()/1000000.0
                up = st.upload()/1000000.0

                logFile.write('%f,%f,%f,%f\n' % (utime, ping, down, up))
                speedStr = 'ping: %f ms\ndown: %f Mbps\nup: %f Mbps\n' % (ping, down, up)
                print(speedStr)

                lowSpeed = 0x0
                if ping > pingLThresh:
                    lowSpeed = lowSpeed | 0x1
                elif ping < pingHThresh:
                    lowSpeed = lowSpeed & (0xF ^ 0x1)
                if down < downLThresh:
                    lowSpeed = lowSpeed | 0x2
                elif down > downHThresh:
                    lowSpeed = lowSpeed & (0xF ^ 0x2)
                if up < upLThresh:
                    lowSpeed = lowSpeed | 0x4
                elif up > upHThresh:
                    lowSpeed = lowSpeed & (0xF ^ 0x4)

                if tweetEn:
                    status = None
                    if lowSpeed > 0 and tagISPEn:
                        statsFmt = 'down: %.2f Mbps\nup: %.2f Mbps\nping: %.2f\nLocation: %s'
                        commentary = '@%s, why is my internet speed so slow when I pay for %s? Fix my internet! %s'
                        statusFmt = 'Current internet speed:\n\n' + statsFmt + '\n\n' + commentary
                        status = statusFmt % (down, up, ping, locale, ispTwitter, plan, tags)
                    else:
                        statsFmt = 'down: %.2f Mbps\nup: %.2f Mbps\nping: %.2f\nLocation: %s'
                        statusFmt = 'Current internet speed:\n\n' + statsFmt
                        status = statusFmt % (down, up, ping, locale)

                    if status:
                        t.statuses.update(status=status)
                        print('Tweet sent\n')

                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print('* * * Exception in main * * *')
                print(e)
                logFile.write('%f,-1,-1,-1,%s\n' % (utime, e))
            finally:
                time.sleep(tMin * 60)
    finally:
        print('Closing log file')
        logFile.close()
