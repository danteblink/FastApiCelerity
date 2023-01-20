import os 
import random 
import time
from pyzbar.pyzbar import decode
#selenium libraries 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
#Other libraries 
import speech_recognition as sr 
import urllib 
import pydub
import undetected_chromedriver.v2 as uc
from unidecode import unidecode

def delay():
    time.sleep(random.randint(2,3))

def audio_to_text(audio_source):
    urllib.request.urlretrieve(audio_source, os.getcwd()+"\\uploads\sample.mp3")
    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\uploads\sample.mp3") 
    sound.export(os.getcwd()+"\\uploads\sample.wav", format="wav") 
    AUDIO_FILE = os.getcwd()+"\\uploads\sample.wav"

    #translate audio to text  
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  
    phrase=r.recognize_sphinx(audio)
    print("[INFO] Recaptcha Passcode: %s"%phrase)

    return phrase

def jump_captcha(url):
    options = uc.ChromeOptions()
    options.headless=True
    options.add_argument('--headless')
    options.add_argument("--lang=es")
    # Docker fix for chrome
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    data_ssalud = None
    is_captcha_solved = False
    succcesText = 'You are verified'

    delay()
    driver.get(url)
    
    try:
        frame_captcha=driver.find_elements_by_tag_name("iframe") 
        driver.switch_to.frame(frame_captcha[0]) 
    except Exception as e:
        print(e)
        driver.close()
        print('[WARNING] Bot Caught. Need to change ip')
        return data_ssalud
    delay()

    #click on checkbox to activate recaptcha 
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    delay()
    #checkbox_recaptcha = driver.find_element_by_id("recaptcha-anchor")
    recaptchaStatus = driver.find_element_by_id("recaptcha-accessible-status").get_attribute('innerText')
    print(recaptchaStatus)
    if  unidecode(recaptchaStatus) == unidecode(succcesText):
        print('[INFO] No advance captcha. Very unlikely')
        is_captcha_solved = True
    else:
    #switch to recaptcha audio control frame 
        driver.switch_to.default_content() 
        frames=driver.find_element_by_xpath("/html/body/div[3]/div[4]").find_elements_by_tag_name("iframe") 
        driver.switch_to.frame(frames[0]) 
        delay()

        #click on audio challenge 
        driver.find_element_by_id("recaptcha-audio-button").click()
        
        while not is_captcha_solved:
        #switch to recaptcha audio challenge frame 
            driver.switch_to.default_content() 
            frames= driver.find_elements_by_tag_name("iframe") 
            driver.switch_to.frame(frames[-1]) 
            delay()
            
            try:
                #click on the play button
                driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
            except Exception as e:
                print(e)
                driver.close()
                print('[WARNING] Bot Caught. Need to change ip')
                return data_ssalud

            #get the mp3 audio file 
            src = driver.find_element_by_id("audio-source").get_attribute("src") 
            print("[INFO] Audio src: %s"%src)

            passcode = audio_to_text(src)
            #download the mp3 audio file from the source 
            
            #key in results and submit 
            driver.find_element_by_id("audio-response").send_keys(passcode.lower()) 
            driver.find_element_by_id("audio-response").send_keys(Keys.ENTER) 
            driver.switch_to.default_content()
            delay()
            driver.switch_to.default_content()
            frame_captcha=driver.find_elements_by_tag_name("iframe")  
            driver.switch_to.frame(frame_captcha[0])
            recaptchaStatus = driver.find_element_by_id("recaptcha-accessible-status").get_attribute('innerText')
            print(recaptchaStatus)
            if unidecode(recaptchaStatus) == unidecode(succcesText) :
                print('[INFO] Congratulations!. Captcha Solved')
                is_captcha_solved = True
            
    driver.switch_to.default_content()
    driver.find_element_by_id("buscar").click() 
    delay()

    #Get data from modal
    try:
        data = driver.find_element_by_class_name('swal-text')
    except Exception as e:
                print(e)
                driver.close()
                print('[WARNING] No data was found')
                return data_ssalud
                
    data_vaccination = data.get_attribute('innerHTML')
    driver.close()

    data_vaccination = data_vaccination.split('<br><br>')
    data_ssalud = {'CURP': data_vaccination[1].split(':')[1].strip()}
    
    return data_ssalud