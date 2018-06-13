import base64
import json
import os
import time
from xml.dom import minidom

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_current_date(driver):
    attempts = 0
    while True:
        try:
            current_date = driver.find_element(By.NAME, "PlanZajecRadScheduler_SelectedDateCalendar_SD") \
                .get_attribute('value')
            return current_date
        except StaleElementReferenceException:
            time.sleep(0.5)
            attempts += 1
            if attempts == 3:
                raise
            else:
                pass


def click_next_date_button(driver):
    attempts = 0
    while True:
        try:
            driver.find_element(By.CLASS_NAME, "rsNextDay").click()
            break
        except StaleElementReferenceException:
            time.sleep(0.5)
            attempts += 1
            if attempts == 3:
                raise
            else:
                pass


def go_to_next_day(driver):
    current_day = get_current_date(driver)
    click_next_date_button(driver)
    while get_current_date(driver) == current_day:
        time.sleep(0.5)


# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
# and set path to binary file
chrome_driver = '/usr/bin/chromedriver'

chrome_options = Options()
# comment line below to run windowed version, moving mouse cursor over window breaks script (chrome bug)!
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get("https://planzajec.pjwstk.edu.pl/PlanOgolny.aspx")

required_fields = ["Data zajęć:", "Godz. rozpoczęcia:", "Godz. zakończenia:", "Budynek:", "Sala:"]
extra_fields = ["Kody przedmiotów:", "Nazwy przedmiotów:", "Typ zajęć:", "Liczba studentów:", "Grupy:"]

all_subjects = []

# for next 30 days
for day in range(0, 30):
    timetable_elements = []
    try:
        timetable_elements = WebDriverWait(driver, 15).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(@class,'rsAptSubject')]"))
        )
    except TimeoutException:
        break

    # scan timetable
    for timetableElement in timetable_elements[:]:
        action = ActionChains(driver)
        action.move_to_element(timetableElement).perform()
        visible_tooltips = WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located((By.ID, "RadToolTipManager1RTMPanel")))

        for visible_tooltip in visible_tooltips[:]:
            tooltip_xmldoc = minidom.parseString(visible_tooltip.get_attribute('innerHTML').encode())
            subject_information_list = tooltip_xmldoc.getElementsByTagName('tr')
            tooltip_data = {}

            for subject_information in subject_information_list[:]:
                row_columns = subject_information.getElementsByTagName('td')
                tooltip_data[row_columns[0].getElementsByTagName('b')[0].firstChild.nodeValue] = \
                    row_columns[1].getElementsByTagName('span')[0].firstChild.nodeValue

            all_required_fields = True
            output_data = []

            for field in required_fields:
                if field in tooltip_data:
                    value = tooltip_data[field].strip()
                    if field == "Data zajęć:":
                        value = "-".join(value.split('.')[::-1])

                    output_data.append(value)
                else:
                    all_required_fields = False
                    break

            if "Dydaktycy:" in tooltip_data:
                output_data.append(tooltip_data["Dydaktycy:"].strip())
            elif "Osoba rezerwująca:" in tooltip_data:
                output_data.append(tooltip_data["Osoba rezerwująca:"].strip())
            else:
                all_required_fields = False

            for field in extra_fields:
                if field in tooltip_data:
                    output_data.append(tooltip_data[field].strip())
                else:
                    output_data.append("")

            if all_required_fields:
                all_subjects.append(output_data)

    go_to_next_day(driver)

print(json.dumps(all_subjects, ensure_ascii=False))
driver.quit()
