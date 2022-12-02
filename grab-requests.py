import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# https://stackoverflow.com/questions/19786525/how-to-list-loaded-resources-with-selenium-phantomjs
PROXY_PORT = 8889
PROXY_URL = 'localhost:%d' % PROXY_PORT
webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy":PROXY_URL,
        "ftpProxy":PROXY_URL,
        "sslProxy":PROXY_URL,
        "noProxy":None,
        "proxyType":"MANUAL"
}

# https://stackoverflow.com/questions/65156932/selenium-proxy-server-argument-unknown-error-neterr-tunnel-connection-faile
webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
print(webdriver.DesiredCapabilities.CHROME)

chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--proxy-server=%s' % PROXY_URL)
chrome_options.add_argument('ignore-certificate-errors')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
     options=chrome_options)

for url in sys.stdin:
    driver.get(url)

user_agent_check = driver.execute_script("return navigator.userAgent;")
print(user_agent_check)

driver.close()
del driver

# avoid warnings about selenium.Service not shutting down in time
time.sleep(3)