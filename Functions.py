from selenium.common.exceptions import NoSuchElementException
import telegram_send
import undetected_chromedriver as uc
from telethon import TelegramClient
import configparser
import time

def word_in_file(filename, name):
    with open(filename, 'r') as f:
        for line in f:
            if name in line:
                return True
        return False

def GetMessages():
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    api_hash = str(api_hash)
    phone = config['Telegram']['phone']
    username = config['Telegram']['username']
    MessageURLs=[]
    chat = 'https://t.me/coursemetry'
    with TelegramClient(username, api_id, api_hash) as client:
        for message in client.iter_messages(chat, limit=100):
            MessageURLs.append(message.buttons[0][0].url)
    return MessageURLs


def GetCourse(url):
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    udemyuser = config['Udemy']['udemyuser']
    udemypass = config['Udemy']['udemypass']

    options = uc.ChromeOptions()
    options.add_argument('--user-data-dir=C:\\Users\\Ouael\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    #options.add_argument("--window-size=1920,1080")
    options.add_argument('--headless')
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.get(url)
    

    if 'couponCode=' in driver.find_element_by_class_name('wp-block-button__link').get_attribute('href'):
        try:
            driver.get(driver.find_element_by_class_name('wp-block-button__link').get_attribute('href'))
            Course = driver.current_url
            time.sleep(5)
            try:
                if driver.find_element_by_css_selector("[data-purpose='header-login']").text == 'Log in':
                    try:
                        driver.find_element_by_css_selector("[data-purpose='header-login']").click()
                        time.sleep(5)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[1]/div/input').send_keys(udemyuser)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[2]/div/input').send_keys(udemypass)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/input').click()
                    except NoSuchElementException:
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input').send_keys(udemypass)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/input').click()
            except NoSuchElementException:
                print('Logged in already!')
            driver.get(Course)
            print(Course)
            time.sleep(5)
            driver.find_element_by_css_selector("[data-purpose='buy-this-course-button']").click()
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button').click()
            time.sleep(5)
            checkstatus = 'udemy.com/cart/success/' in driver.current_url
            if checkstatus:
                telegram_send.send(messages=['Subscribed to ' + Course])
                driver.close()
            else:
                print('Subscribing Failed')
                driver.close()
        except NoSuchElementException:
            print('Subscribing Failed')
            driver.close()
    else:
        try:
            driver.get(driver.find_element_by_class_name('wp-block-button__link').get_attribute('href'))
            Course = driver.current_url
            time.sleep(5)
            try:
                if driver.find_element_by_css_selector("[data-purpose='header-login']").text == 'Log in':
                    try:
                        driver.find_element_by_css_selector("[data-purpose='header-login']").click()
                        time.sleep(5)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[1]/div/input').send_keys(udemyuser)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div[2]/div/input').send_keys(udemypass)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/input').click()
                    except NoSuchElementException:
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[1]/div/div/input').send_keys(udemypass)
                        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/div[2]/div/input').click()
            except NoSuchElementException:
                print('Logged in already!')
            driver.get(Course)
            print(Course)
            time.sleep(5)
            driver.find_element_by_css_selector("[data-purpose='buy-this-course-button']").click()
            time.sleep(5)
            SubSuccess = 'udemy.com/cart/subscribe/'
            if SubSuccess in driver.current_url:
                telegram_send.send(messages=['Subscribed to ' + Course])
                driver.close()
            else:
                print('Subscribing Failed')
                driver.close()  
        except NoSuchElementException:
            print('Subscribing Failed')
            driver.close()