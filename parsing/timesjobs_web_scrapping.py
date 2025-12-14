from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as Bs4
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from timesjobs_utils import all_elements_located, get_href_of_div, conditions

# Иногда сайт может зависать и парсинг прерывается. В этом случае лучше просто его перезапустить.
# Парсинг можно прервать CTRL + C в любой момент 

options = Options()
options.page_load_strategy = 'none'
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


driver.get('https://www.timesjobs.com/job-search?keywords="Data+Science"%2C&location=&experience=&refreshed=true')

counter = 0

with open("result.csv", "w") as file:
    while True:
        try: 
            WebDriverWait(driver, 30).until(lambda x: len(x.find_elements(By.CSS_SELECTOR, "[class*='srp-card']")) >= 10)
            
            locators = [
                f"(//*[contains(@class, 'srp-card')])[{i+1}]"
                for i in range(10)
            ]

            for locator in locators:
                counter += 1
                general_result = dict()
                href = get_href_of_div(driver, locator)

                if not href: continue
                
                driver.execute_script(f"window.open('{href}', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])

                try:
                    WebDriverWait(driver, 100).until(all_elements_located)
                
                    resulted_string = ""
                    soup = Bs4(driver.page_source, "html.parser")

                    h1 = soup.find("h1", class_="text-lg font-bold mb-2").get_text()
                    print("Название", h1)

                    general_result[0] = h1

                    required_classname = conditions[1][1].replace(".", " ").replace("\\", "")[1:]

                    base_info = soup.find("div", class_=required_classname).find_all("span", recursive=False)
                    general_result[1] = base_info[0].span.get_text()
                    general_result[2] = base_info[1].get_text()
                    print("Локация", general_result[1])
                    print("Рабочий опыт", general_result[2])


                    required_classname = conditions[2][1].replace(".", " ").replace("\\", "")[1:]
                    stack = soup.find_all("span", class_=required_classname)

                    result_stack = []

                    for span in stack: result_stack.append(span.get_text())

                    stack = "/".join(result_stack)

                    print("Навыки", stack)
                    general_result[3] = stack

                    required_classname = conditions[3][1].replace(".", " ")[1:]
                    list_els = soup.find("ul", class_=required_classname).find_all("li")

                    for li in list_els:
                        if "Graduate Courses" in li.span.get_text():
                            general_result[4] = li.get_text().split(": ")[1]
                            print("Образование", general_result[4]) 
                        elif "Industry" in li.span.get_text():
                            general_result[5] = li.get_text().split(": ")[1]
                            print("Индустрия", general_result[5]) 
                        elif "Employment Type" in li.span.get_text():
                            general_result[6] = li.get_text().split(": ")[1]
                            print("Тип занятости", general_result[6])

                    for index in general_result: 
                        general_result[index] = str(general_result[index]).replace(";", ",")

                    general_result = map(lambda x: x[1], sorted(general_result.items(), key=lambda x: x[0]))


                    append_result = ";".join(general_result) + "\n"
                    file.writelines([append_result])

                    print("*" * 50)
                    print("Собрано к этому моменту:", counter)
                    print("*" * 50)



                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                except: continue
        
        except TimeoutException: break
        except: break
        
        button = driver.find_element(By.CSS_SELECTOR, "button.pagination-next")
        driver.execute_script("arguments[0].click();", button)


print("Сбор данных закончен!")




