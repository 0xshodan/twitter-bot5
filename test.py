from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.common import exceptions
import pickle
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Chrome()
cookies = pickle.load(open("cookies.pkl", "rb"))
driver.get("https://twitter.com/")
for cookie in cookies:
    driver.add_cookie(cookie)
# driver.add_cookie({"name":"auth_token","value":"18a72d152b031b215d326cd52fdd33d626a2eeea"})
# driver.get("https://twitter.com/home")
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
driver.get("https://twitter.com/BitcoinMagazine/status/1677769222255169536")

wait = WebDriverWait(driver, 20)
time.sleep(5)
el = driver.find_element(By.CLASS_NAME, "public-DraftEditorPlaceholder-root")
el.click()
time.sleep(200)
driver.close()