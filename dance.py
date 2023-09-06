import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import getindianname as name

# Define the MUTEX variable
MUTEX = threading.Lock()

# Flag to indicate whether the script is running
running = True

def sync_print(text):
    with MUTEX:
        print(text)

def get_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1
    })
    driver = webdriver.Chrome("chromedriver", options=options)
    return driver

def driver_wait(driver, locator, by, secs=10, condition=EC.element_to_be_clickable):
    wait = WebDriverWait(driver=driver, timeout=secs)
    element = wait.until(condition((by, locator)))
    return element

def start(name, user, wait_time, meetingcode, passcode):
    sync_print(f"{name} started!")
    driver = get_driver()
    driver.get(f'https://zoom.us/wc/join/{meetingcode}')

    try:
        accept_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        accept_btn.click()
    except Exception as e:
        pass

    try:
        agree_btn = driver.find_element(By.ID, 'wc_agree1')
        agree_btn.click()
    except Exception as e:
        pass

    try:
        input_box = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        input_box.send_keys(user)
        password_box = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_box.send_keys(passcode)
        join_button = driver.find_element(By.CSS_SELECTOR, 'button.preview-join-button')
        join_button.click()
    except Exception as e:
        pass

    try:
        audio_button = driver.find_element(By.XPATH, '//button[text()="Join Audio by Computer"]')
        time.sleep(13)
        audio_button.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge. ", e)

    sync_print(f"{name} sleep for {wait_time} seconds ...")
    while running and wait_time > 0:
        time.sleep(1)
        wait_time -= 1
    sync_print(f"{name} ended!")

    driver.quit()

def main():
    global running
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    with ThreadPoolExecutor(max_workers=number) as executor:
        tasks = []
        for i in range(number):
            try:
                # Generate a random Indian name using getindianname
                user = name.randname()
            except IndexError:
                break
            task = executor.submit(start, f'[Thread{i}]', user, wait_time, meetingcode, passcode)
            tasks.append(task)
        try:
            for task in tasks:
                task.result()
        except KeyboardInterrupt:
            running = False
            # Wait for tasks to complete

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
