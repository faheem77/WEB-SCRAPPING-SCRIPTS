# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
driver= webdriver.Chrome(ChromeDriverManager().install(), options=option)
driver.maximize_window()
driver.get('https://www.adamchoi.co.uk/overs/detailed')
driver.find_element(By.XPATH,'//label[@analytics-event="All matches"]').click()

matches = driver.find_elements(By.TAG_NAME,'tr')
date= []
home_team= []
score =[]
away_team= []
for match in matches:
    date.append(match.find_element(By.XPATH,'./td[1]').text)
    home_team.append(match.find_element(By.XPATH,'./td[2]').text)
    score.append(match.find_element(By.XPATH,'./td[3]').text)
    away_team.append(match.find_element(By.XPATH,'./td[4]').text)


df = pd.DataFrame({"Date":date,"HOME_TEAM":home_team, "SCORE":score, "AWAY_TEAM":away_team})
df.to_csv("data.csv", index=True)

driver.quit()
