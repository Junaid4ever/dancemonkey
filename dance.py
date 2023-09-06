import time
import warnings
import threading

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec



proxylist = [
    "192.99.101.142:7497",
    "198.50.198.93:3128",
    "52.188.106.163:3128",
    "20.84.57.125:3128",
    "172.104.13.32:7497",
    "172.104.14.65:7497",
    "165.225.220.241:10605",
    "165.225.208.84:10605",
    "165.225.39.90:10605",
    "165.225.208.243:10012",
    "172.104.20.199:7497",
    "165.225.220.251:80",
    "34.110.251.255:80",
    "159.89.49.172:7497",
    "165.225.208.178:80",
    "205.251.66.56:7497",
    "139.177.203.215:3128",
    "64.235.204.107:3128",
    "165.225.38.68:10605",
    "165.225.56.49:10605",
    "136.226.75.13:10605",
    "136.226.75.35:10605",
    "165.225.56.50:10605",
    "165.225.56.127:10605",
    "208.52.166.96:5555",
    "104.129.194.159:443",
    "104.129.194.161:443",
    "165.225.8.78:10458",
    "5.161.93.53:1080",
    "165.225.8.100:10605",
]

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()

def sync_print(text):
    with MUTEX:
        print(text)


def start(name, proxy, user, wait_time, meetingcode, passcode):
    sync_print(f"{name} started!")
    driver = get_driver(proxy)
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
    wait_time = sec * 60
    workers = []
    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = fake.name()
        except IndexError:
            break
        wk = threading.Thread(target=start, args=(
            f'[Thread{i}]', proxy, user, wait_time, meetingcode, passcode))
        workers.append(wk)
    for wk in workers:
        wk.start()
    for wk in workers:
        wk.join()

if __name__ == '__main__':
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")
    sec = 5
    main()
