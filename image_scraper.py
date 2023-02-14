from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests

import shutil
import os

driver = webdriver.Chrome(executable_path="C:\\Program Files\\WebDriver\\bin\\chromedriver.exe")
driver.get("https://pokemondb.net/pokedex/all")

driver.find_element_by_xpath("//button[@class='btn btn-primary gdpr-accept']").click()

pokemon_links = [elem.get_attribute('href') for elem in driver.find_elements_by_xpath("//a[@class='ent-name']")]

for link in pokemon_links[800:]:
    driver.get(link)

    pokemon_name = driver.find_element_by_xpath("//h1").text

    if pokemon_name == "Type: Null":
        pokemon_name = "Type Null"

    if not os.path.exists(f"images/{pokemon_name}"):
        os.makedirs(f"images/{pokemon_name}")
    else:
        # We have already stored these pictures and can skip this Pokemon
        print(f"{pokemon_name}: Skipped")
        continue

    try:
        all_pics_link = driver.find_element_by_xpath("//a[text()='Additional artwork']").get_attribute('href')
        driver.get(all_pics_link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        picture_links = driver.find_elements_by_xpath("//img[contains(@src, 'https://img.pokemondb.net/artwork/')]")
        print(f"{pokemon_name}: {len(picture_links)} Images")

        for i in range(len(picture_links)):
            src = picture_links[i].get_attribute('src')
            response = requests.get(src, stream=True)
            with open(f"images/{pokemon_name}/{i}.{src[-3:]}", "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)

        driver.back()
    except NoSuchElementException:
        picture_links = driver.find_elements_by_xpath("//img[contains(@src, 'https://img.pokemondb.net/artwork/')]")
        print(f"{pokemon_name}: {len(picture_links)} Images")

        for i in range(len(picture_links)):
            src = picture_links[i].get_attribute('src')
            response = requests.get(src, stream=True)
            with open(f"images/{pokemon_name}/{i}.{src[-3:]}", "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)

    driver.back()

print("DONE!")
driver.close()
