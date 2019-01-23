import sys
import os
import time
from base import MiBand2
from bluepy.btle import BTLEException

MAC = sys.argv[1]
filepath = sys.argv[2]
if os.path.exists(sys.argv[2]):
    os.remove(sys.argv[2])
fp = open(filepath, 'a')
fp.write('time, heartrate\n')

def log(rate):
    print rate
    data = "%s, %d\n" % (int(time.time()), rate)
    fp.write(data)
    print data

while True:
    try:
        band = MiBand2(MAC, debug=True)
        band.setSecurityLevel(level="medium")
        band.authenticate()
        if sys.argv[3] == "seperated":
            start = time.time()
            log(band.get_heart_rate_one_time())
            while True:
                sleep(10)
                if time.time()-start >= 60*3:
                    start = time.time()
                    try:
                        log(band.get_heart_rate_one_time())
                        #time.sleep(55)
                    except KeyboardInterrupt:
                        print 'Manual break by user'
                        pass
        else:
            band.start_heart_rate_realtime(heart_measure_callback=log)

        band.disconnect()
    except BTLEException:
        pass
