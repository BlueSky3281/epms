from multiprocessing import Pool
#from selenium import webdriver
import itertools
import requests
import time
import logging

#driver = webdriver.PhantomJS('/home/shinhan/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#driver.implicitly_wait(3)

logging.basicConfig(filename='./crawler.log', level=logging.INFO,format='%(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)

#logger.debug('Welcome SDII %s', 'Lab')

def crawler(args):
    url = args[0]
    checkTime = args[1]
    limitTime = args[2]
    print("URL : ",url," MortorTime : ",checkTime," LimitTime : ",limitTime)

    while(1):
      rst = 0
      now = time.localtime()
      s_time = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec)
      start_time=time.time()

      try:
        response = requests.get(url)
        #driver.get(url);
        rst = response.status_code
        #print(response.status_code)
      except requests.exceptions.RequestException as e:
        print('exception caught', e)
        rst = 1

      end_time=time.time()
      a_load_time=round(float(end_time-start_time),3)

      if rst == 200:
        if limitTime > a_load_time:
          logdata = "%s %s %.3f %d" %(url, s_time, a_load_time, rst)
        else:
          logdata = "%s %s %.3f %d ERROR" %(url, s_time, a_load_time, rst)
      else:
        logdata = "%s %s %.3f %d ERROR" %(url, s_time, a_load_time, rst)

      logger.info(logdata)
      time.sleep(checkTime)

if __name__ == '__main__':

    sites = [["http://www.naver.com",20,10,"#EX"],
             ["http://www.google.com",10,10,"#EX"],
             ["http://www.shinhan.com",30,3,"#IN"],
             ["http://m.shinhan.com",30,3,"#IN"],
             ["http://www.daum.com",7,7,"#EX"]]

    print("Mornitor count is ",len(sites))

    pool = Pool(processes=len(sites))

    print(pool.map(crawler, sites))
    pool.close()
