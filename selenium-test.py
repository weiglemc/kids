import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import sys
import time
import socketserver
import http.server
import urllib.request
from http.server import SimpleHTTPRequestHandler
from multiprocessing import Process, freeze_support

def initial_test():
    # https://chromedriver.chromium.org/getting-started
    # https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python
    # https://stackoverflow.com/questions/44629970/error-name-by-is-not-defined-using-python-selenium-webdriver/44630066#44630066
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.google.com")
    time.sleep(5) # Let the user actually see something!
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5) # Let the user actually see something!
    driver.quit()

# https://stackoverflow.com/questions/19786525/how-to-list-loaded-resources-with-selenium-phantomjs
PROXY_PORT = 8889
PROXY_URL = 'localhost:%d' % PROXY_PORT

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print ("do_GET> ")
        sys.stdout.write('%s → %s\n' % (self.headers.get('Referer', 'NO_REFERER'), self.path))
        self.copyfile(urllib.request.urlopen(self.path), self.wfile)
        sys.stdout.flush()

    @classmethod
    def target(cls):
        httpd = socketserver.ThreadingTCPServer(('', PROXY_PORT), cls)
        httpd.serve_forever()

if __name__ == '__main__':
    freeze_support()

    p_proxy = Process(target=Proxy.target)
    p_proxy.start()

    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy":PROXY_URL,
#        "ftpProxy":PROXY_URL,
        "sslProxy":PROXY_URL,
        "noProxy":None,
        "proxyType":"MANUAL"#,
#        "class":"org.openqa.selenium.Proxy",
#        "autodetect":False
    }
# https://stackoverflow.com/questions/65156932/selenium-proxy-server-argument-unknown-error-neterr-tunnel-connection-faile
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    print(webdriver.DesiredCapabilities.CHROME)

    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--proxy-server=%s' % PROXY_URL)
    chrome_options.add_argument('ignore-certificate-errors')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
        options=chrome_options)
    for url in sys.stdin:
        driver.get(url)
        print (driver.title)

    user_agent_check = driver.execute_script("return navigator.userAgent;")
    print(user_agent_check)

    driver.close()
    del driver
    p_proxy.terminate()
    p_proxy.join()
    # avoid warnings about selenium.Service not shutting down in time
    time.sleep(3)