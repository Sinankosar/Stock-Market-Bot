from selenium import webdriver
from pushbullet import Pushbullet 
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.maximize_window()
pb = Pushbullet("o.xBUpUCxuP5eEDoUg8iJbRKzg68F1cOWO")
try:
    def check():
        driver.get("https://tr.tradingview.com/symbols/LKIUSDT/ideas/?exchange=GATEIO")
        time.sleep(3) 
        tekniker = driver.find_element(By.CLASS_NAME,"tv-tabs__scroll-box")
        _teknikler = tekniker.find_elements(By.TAG_NAME,"a")
        _teknikler[2].click()    
        time.sleep(3)

        container_div = driver.find_element(By.CSS_SELECTOR, ".speedometersContainer-kg4MJrFB.laptop-kg4MJrFB")
        inner_divs = container_div.find_elements(By.TAG_NAME,"div")
        özet_div = inner_divs[1]
        
        fifteen_min = driver.find_element(By.ID, "15m")
        fifteen_min.click()
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 600);")   
        time.sleep(3)
        özet_ibre = driver.find_elements(By.XPATH, "/html/body/div[3]/div[4]/div[3]/div[2]/div/section/div/div[4]/div[2]/div[2]")
        liste =[]
      
        for i in özet_ibre:
            liste.append(i.text)
            
        a = [item.replace("\n", " ").split() for item in liste]
        print(a)
        sat = int(a[0][1])
        al = int(a[0][-1])        
        return sat,al
        
    previous_sat, previous_al = check()
    
    is_on = True
    while is_on:
        time.sleep(300)
        current_sat, current_al = check()
        
        if current_sat != previous_sat :
            current_time = datetime.now().strftime("%H:%M")
            pb.push_note("Satma vakti geldi ", f"Sat: {current_sat}, Al: {current_al}. Zaman : {current_time}")
            previous_sat, previous_al = current_sat, current_al  
        elif current_al != previous_al:
            current_time = datetime.now().strftime("%H:%M")
            pb.push_note("Alma vakti geldi ", f"Sat: {current_sat}, Al: {current_al}. Zaman : {current_time}")
            previous_sat, previous_al = current_sat, current_al  
    
finally:
    driver.quit()
