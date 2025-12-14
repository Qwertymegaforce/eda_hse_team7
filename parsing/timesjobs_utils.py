from selenium.webdriver.common.by import By
from selenium import webdriver


conditions = [
    [By.CSS_SELECTOR, ".text-lg.font-bold.mb-2"],
    [By.CSS_SELECTOR, ".mt-1.flex.flex-wrap.items-center.font-semibold.text-sm.leading-\\[24px\\].md\\:leading-normal"],
    [By.CSS_SELECTOR, ".border.mr-1.rounded-full.px-3.py-1.text-xs.mb-2.inline-block"],
    [By.CSS_SELECTOR, ".text-sm"],
]

def all_elements_located(driver : webdriver.Chrome):
    for by, classname in conditions:
        if not driver.find_elements(by, classname):
            return False
    return True


def get_href_of_div(driver : webdriver.Chrome, locator: str):
    return driver.find_element(By.XPATH, locator).find_element(By.TAG_NAME, "a").get_attribute("href")