from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import random
import os
import pickle
import pyautogui
import sys

def main():
    ser = Service('chromedriver')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ser, options=options)
    driver.set_window_size(1920, 1080*12)
    driver.get("https://www.twitch.tv/team/staff")
    time.sleep(random.uniform(0.5, 1.5))
    staff_list = []
    
    for i in range(1, 250):
        try:
            element = driver.find_element(By.XPATH, f"//button[{i}]/div/div/p")
            print("Found staff name:", element.text)
            staff_list.append(element.text)
            # if i % 50 == 0:
            #     time.sleep(0.1)
            #     print(f"Scrolling down on {i}")
            #     try:
            #         scroll_button = driver.find_element(By.XPATH, f"//div[2]/div[2]/div/div/div")
            #         actions = ActionChains(driver)
            #         actions.move_to_element(scroll_button).perform()
            #         actions.click_and_hold(scroll_button).perform()
            #         actions.move_by_offset(0, 400).perform()
            #         actions.release().perform()
            #         actions.drag_and_drop_by_offset(scroll_button, 0, 400).perform()
            #     except Exception as e:
            #         print(e) 
            #     time.sleep(random.uniform(0.5, 1))
        except:
            break
    if os.path.exists("twitch_staff.pickle"):
        with open("twitch_staff.pickle", "rb") as f:
            staff_set = pickle.load(f)
    else:
        staff_set = set()
    
    for staff in sys.argv[1:]:
        staff_set.add(staff)
    for staff in staff_list:
        if staff != "":
            staff_set.add(staff)
    staff_set.add('jbulava')
    
    with open("twitch_staff.pickle", "wb") as f:
        pickle.dump(staff_set, f)

    print(staff_set)

    print(f"Length of staff_set is {len(staff_set)}")

if __name__ == "__main__":
    main()