import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Open kolesa.kz and after open advertisement
driver = webdriver.Firefox()
driver.get("https://kolesa.kz/")
driver.find_element_by_xpath('//*[@title="Легковые"]').click()
wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
button.click()
page_counter = 2
cars = []

# Counter of page for upload only one hundred advertisements
while page_counter <= 6:
    models = driver.find_elements_by_xpath('//*[@class="a-el-info-title"]')
    prices = driver.find_elements_by_xpath('//*[@class="price"]')
    descriptions = driver.find_elements_by_xpath('//div[@class="a-search-description"]')
    regions = driver.find_elements_by_xpath('//div[@class="list-region"]')
    created_at = driver.find_elements_by_xpath('//*[@class="date"]')
    views = driver.find_elements_by_xpath('//*[@class="nb-views-int"]')

    # Append data about one car to list
    for i in range(len(models)):
        cars.append({
            'model': models[i].text,
            'price': prices[i].text,
            'description': descriptions[i].text,
            'region': regions[i].text,
            'created_at': created_at[i].text,
            'viewed': views[i].text
        })
    page_counter += 1
    driver.find_element_by_xpath("//a[@href='/cars/?page=" + str(page_counter) + "']").click()

# Open json file and upload data about cars
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(cars, json_file, ensure_ascii=False, indent=4)
driver.close()
print("Data successfully saved")
