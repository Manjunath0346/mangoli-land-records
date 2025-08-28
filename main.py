from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

def main():
    try:
        print("Starting the script...")

        website = "https://landrecords.karnataka.gov.in/Service2/"
        path = "C:/Windows/chromedriver.exe"
        service = Service(path)
        driver = webdriver.Chrome(service=service)

        print("Maximizing the browser window...")
        driver.maximize_window()

        print("Opening the website...")
        driver.get(website)

        print("Website opened. Waiting for the page to load...")
        time.sleep(1)  # Wait for the page to load

        print("\nSelecting the District dropdown...")
        wait = WebDriverWait(driver, 10)
        district_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCDistrict")))
        district_dropdown = Select(district_dropdown_element)
        district_dropdown.select_by_visible_text("VIJAYAPURA")

        print("District selected. Waiting for the Taluk dropdown to be populated...")
        time.sleep(1)  # Wait for the Taluk dropdown to be populated

        print("Selecting the Taluk dropdown...")
        taluk_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCTaluk")))
        taluk_dropdown = Select(taluk_dropdown_element)
        taluk_dropdown.select_by_visible_text("BASAVAN BAGEWADI")

        print("Taluk selected. Waiting for the Hobli dropdown to be populated...")
        time.sleep(1)  # Wait for the Hobli dropdown to be populated

        print("Selecting the Hobli dropdown...")
        hobli_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCHobli")))
        hobli_dropdown = Select(hobli_dropdown_element)
        hobli_dropdown.select_by_visible_text("MANAGULI")

        print("Hobli selected. Waiting for the Village dropdown to be populated...")
        time.sleep(1)  # Wait for the Village dropdown to be populated

        print("Selecting the Village dropdown...")
        village_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCVillage")))
        village_dropdown = Select(village_dropdown_element)
        village_dropdown.select_by_visible_text("MANAGULI")

        print("Village selected. Waiting for the Survey Number input to be enabled...")
        time.sleep(1)  # Wait for the Survey Number input to be enabled

        # Prepare to write to CSV file
        with open('owner_details.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Survey Number", "Hissa", "Owner", "Extent"])
            writer.writeheader()

            # Iterate over survey numbers from 1 to 2820
            for survey_number in range(2801, 2821):
                print(f"\nProcessing Survey Number: {survey_number}")

                print(f"{' ' * 2}Entering the Survey Number...")
                survey_number_input = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_MainContent_txtCSurveyNo")))
                survey_number_input.send_keys(Keys.CONTROL + "a")
                survey_number_input.send_keys(Keys.DELETE)
                survey_number_input.send_keys(str(survey_number))

                print(f"{' ' * 2}Survey Number entered. Clicking on the Go button...")
                go_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_MainContent_btnCGo")))
                driver.execute_script("arguments[0].click();", go_button)

                print(f"{' ' * 2}Go button clicked. Waiting for the Surnoc dropdown to be populated...")
                time.sleep(2)  # Wait for the Surnoc dropdown to be populated

                print(f"{' ' * 2}Selecting the Surnoc dropdown...")
                surnoc_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCSurnocNo")))
                surnoc_dropdown = Select(surnoc_dropdown_element)
                surnoc_dropdown.select_by_visible_text("*")

                print(f"{' ' * 2}Surnoc selected. Waiting for the Hissa dropdown to be populated...")
                time.sleep(2)  # Wait for the Hissa dropdown to be populated

                print(f"{' ' * 2}Selecting the Hissa dropdown...")
                hissa_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCHissaNo")))
                hissa_dropdown = Select(hissa_dropdown_element)
                hissa_values = [option.text for option in hissa_dropdown.options if option.text != "Select Hissa"]

                print(f"\n{' ' * 2}Hissa values: {hissa_values}")

                # Iterate over all Hissa options
                for index, hissa_value in enumerate(hissa_values):
                    print(f"\n  Selecting Hissa: {hissa_value} ({index+1}/{len(hissa_values)})")
                    hissa_dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlCHissaNo")))
                    hissa_dropdown = Select(hissa_dropdown_element)
                    hissa_dropdown.select_by_visible_text(hissa_value)

                    print(f"{' ' * 4}Hissa selected. Clicking on the Fetch details button...")
                    fetch_details_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_MainContent_btnCFetchDetails")))
                    fetch_details_button.click()

                    print(f"{' ' * 4}Fetch details button clicked. Waiting for the details to be displayed...")
                    time.sleep(5)  # Wait for the details to be displayed

                    print(f"{' ' * 4}Extracting Owner and Extent details...")
                    try:
                        # Locate the table rows containing owner details
                        rows = driver.find_elements(By.XPATH, "//div[@id='ctl00_MainContent_div1']//table//tr[position()>1]")

                        print(f"{' ' * 4}Owner details:")
                        print(f"{' ' * 6}Survey Number: {survey_number}, Hissa: {hissa_value}")

                        for row in rows:
                            owner_element = row.find_element(By.XPATH, "./td[1]")
                            extent_element = row.find_element(By.XPATH, "./td[2]")

                            owner = owner_element.text
                            extent = extent_element.text

                            details = {
                                "Survey Number": survey_number,
                                "Hissa": hissa_value,
                                "Owner": owner,
                                "Extent": extent
                            }

                            print(f"{' ' * 8}Owner: {details['Owner']}, Extent: {details['Extent']}")

                            # Write details to CSV file
                            writer.writerow(details)

                        print(f"{' ' * 4}Details for Hissa {hissa_value} written to owner_details.csv")

                    except Exception as e:
                        print(f"{' ' * 4}An error occurred while extracting details for Hissa {hissa_value}: {e}")

                time.sleep(2)

        print(f"\nClosing the browser...")
        driver.quit()

        print(f"Script finished.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()