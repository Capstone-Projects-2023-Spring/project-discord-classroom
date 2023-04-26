from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
import json


config_path = os.path.abspath("../config.json")

if os.path.exists(config_path):
    with open(config_path) as f:
        configData = json.load(f)
else:
    configTemp = {"DISCORD_EMAIL": "", "DISCORD_PASSWORD": "", "LOUNGE_CHANNEL_URL": "", "PRIVATE_QUESTION_CHANNEL_URL":"",
                  "BOT_DM":"", "DISCORD_EMAIL_TEACHER": "", "DISCORD_PASSWORD_TEACHER": "", "ATTENDANCE_CHANNEL_URL" : "",
                  "BOT_DM_TEACHER":""}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemp, f)

DISCORD_EMAIL = configData["DISCORD_EMAIL"]
DISCORD_PASSWORD = configData["DISCORD_PASSWORD"]
LOUNGE_CHANNEL_URL = configData["LOUNGE_CHANNEL_URL"]
ATTENDANCE_CHANNEL_URL = configData["ATTENDANCE_CHANNEL_URL"]
PRIVATE_QUESTION_CHANNEL_URL = configData["PRIVATE_QUESTION_CHANNEL_URL"]
BOT_DM = configData["BOT_DM"]
DISCORD_EMAIL_TEACHER = configData["DISCORD_EMAIL_TEACHER"]
DISCORD_PASSWORD_TEACHER = configData["DISCORD_PASSWORD_TEACHER"]
BOT_DM_TEACHER = configData["BOT_DM_TEACHER"]

# student account
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.get("https://discord.com/login")
time.sleep(5) # Wait for the page to load

# Enter email and password
login_form = driver.find_element(By.XPATH, "//input[@type='text' and @name='email']")
login_form.send_keys(DISCORD_EMAIL)
password_field =  driver.find_element(By.XPATH, "//input[@type='password']")
password_field.send_keys(DISCORD_PASSWORD)
login_form.submit() # Submit the form to login
time.sleep(5) 

# Navigate to lounge channel
driver.get(LOUNGE_CHANNEL_URL)
time.sleep(5)
message_field = driver.find_element(By.XPATH, "//div[@aria-label='Message #lounge']")
message_field.click()

#create a poll
message_field.send_keys("/poll topic:favorite color option1:black option2:orange")
time.sleep(5)
message_field.send_keys(Keys.ENTER)
time.sleep(5) 
message_field.send_keys(Keys.ENTER)
time.sleep(5) 

# send a private question
message_field.click()
message_field.send_keys("/private question:office hour?")
time.sleep(5)
message_field.send_keys(Keys.ENTER)
time.sleep(5) 
message_field.send_keys(Keys.ENTER)
time.sleep(5) 

# ask tutor gpt to create a practice quiz
message_field.click()
message_field.send_keys("/tutor quiz number_of_questions:1 subject:Math grade:7")
time.sleep(5)
message_field.send_keys(Keys.ENTER)
time.sleep(5) 
message_field.send_keys(Keys.ENTER)
time.sleep(5)

# navigate to dm to check/answer quiz and receive feedback
driver.get(BOT_DM)
time.sleep(5)
message_field = driver.find_element(By.XPATH, "//div[@role='textbox']")
time.sleep(5) 
message_field.send_keys("1)0")
time.sleep(5) 
message_field.send_keys(Keys.ENTER)
time.sleep(5) 

# check if private question was created
driver.get(PRIVATE_QUESTION_CHANNEL_URL)
time.sleep(5)

#close student expierence
driver.quit()


# educator account
driver = webdriver.Chrome(options=options)

driver.get("https://discord.com/login")
time.sleep(5) 

# Enter email and password
login_form = driver.find_element(By.XPATH, "//input[@type='text' and @name='email']")
login_form.send_keys(DISCORD_EMAIL_TEACHER)
password_field =  driver.find_element(By.XPATH, "//input[@type='password']")
password_field.send_keys(DISCORD_PASSWORD_TEACHER)
login_form.submit() # Submit the form to login
time.sleep(5) 

# Navigate to attendance channel
driver.get(ATTENDANCE_CHANNEL_URL)
time.sleep(5) 

message_field = driver.find_element(By.XPATH, "//div[@aria-label='Message #attendance']")
message_field.click()
time.sleep(5)

message_field.send_keys("/lecture attendance time:0.1")
time.sleep(5)
message_field.send_keys(Keys.ENTER)
time.sleep(5) 
message_field.send_keys(Keys.ENTER)
time.sleep(6) 
driver.get(BOT_DM_TEACHER)
time.sleep(5)

driver.quit()
