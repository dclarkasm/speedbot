#!/usr/bin/python
# speedbot.py
# Script to monitor internet speed and tweet it periodically
# Author: Devon Clark
# 2017
import time
import datetime
from pyspeedtest import SpeedTest

tMin = 0.1   # time delay between speed tests in minutes
st = SpeedTest()   # the speed test object
logFileNm = time.strftime('logs/SpeedLog-%d%m%Y-%H%M%S.csv', time.localtime())
print('Speed test log file: ' + logFileNm)
logFile = open(logFileNm, 'w')

if __name__ == '__main__':
    try:
        while 1:
            utime = time.time()
            ping = st.ping()
            down = st.download()/1000000
            up = st.upload()/1000000

            logFile.write('%f,%d,%d,%d\n' % (utime, ping, down, up))
            print(('ping: %d ms\ndown: %d Mbps\nup: %d Mbps') % (ping, down, up))
            time.sleep(tMin * 60)
    except Exception as e:
        print('* * * Exception in main * * *')
        print(e)
    finally:
        print('Closing log file')
        logFile.close()