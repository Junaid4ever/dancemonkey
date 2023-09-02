import asyncio
import nest_asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import random
import getindianname as name

nest_asyncio.apply()

async def start(name, user, wait_time, meetingcode, passcode)::
    print(f"{name} started!")

    browser = await launch(
        headless=True,
        executablePath='/usr/bin/brave-browser',  # Specify the browser executable path
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    page = await browser.newPage()

    # Apply pyppeteer-stealth to mimic a real browser
    await stealth(page)

    await page.goto(f'https://zoom.us/wc/join/{meetingcode}')

    try:
        await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
    except Exception as e:
        pass

    try:
        await page.click('//button[@id="wc_agree1"]', timeout=5000)
    except Exception as e:
        pass

    try:
        await page.waitForSelector('input[type="text"]', timeout=200000)
        await page.type('input[type="text"]', user)
        await page.type('input[type="password"]', passcode)
        join_button = await page.waitForSelector('button.preview-join-button', timeout=200000)
        await join_button.click()
    except Exception as e:
        pass

    try:
        qry = '//button[text()="Join Audio by Computer"]'
        mic_btn_loc = await page.waitForXPath(qry, timeout=400000)
        await mic_btn_loc.click()
        print(f"{name} mic aayenge.")
    except Exception as e:
        print(f"{name} mic nahe aayenge.")

    # ... (other code)

    print(f"{name} sleep for {wait_time} seconds ...")
    await asyncio.sleep(wait_time)
    print(f"{name} ended!")

    await browser.close()
... 
async def main():
    # Accept input for the number of users directly in Colab
    number = int(input("Enter number of Users: "))
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    tasks = []

    for i in range(number):
        user = name.randname()  # Generate a random Indian name
        task = asyncio.create_task(start(f'[Thread{i}]', user, wait_time, meetingcode, passcode))
        tasks.append(task)

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        # Wait for tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
