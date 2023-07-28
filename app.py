from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import *
from pynput.keyboard import Controller, Key
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import pytesseract
import seleniumwire
import json
import time

import json


class EasyApplyLinkedin:

    def __init__(self, data):
        """Parameter initialization"""
        SCRAPEOPS_API_KEY = '10a926a3-f858-4c02-ad9c-b468eb3e4df1'

        # Define ScrapeOps Proxy Port Endpoint
        proxy_server_url = f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353'
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        options = webdriver.ChromeOptions()
        options.add_argument(f'--proxy-server={proxy_server_url}')
        self.driver = webdriver.Chrome( options=options)
        
    def login_linkedin(self):
        """This function logs into your personal linkedin account"""

        # Go to linkedin login page
        self.driver.get("https://www.linkedin.com/login") 

        # Wait until the email input field is visible
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'session_key'))
        )

        # Introduce password
        email_input.clear()
        email_input.send_keys(self.email)

        # Wait until the password input field is visible
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'session_password'))
        )

        # Introduce password
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.submit()

        time.sleep(5)


    
    def job_search(self):
        """This function goest to the 'Jobs' section and looks for jobs matching the keywords and location"""

        self.driver.maximize_window()

        time.sleep(5)

        # Find the search keywords input field
        search_keywords = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-global-typeahead__input[aria-label='Search']"))
        )

        # Clear the search keywords input field and enter the keywords
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_keywords.send_keys(Keys.RETURN)

        time.sleep(5)

        # Wait for the "Easy apply" link to be clickable
        easy_apply_link = WebDriverWait(self.driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Easy apply'))
        )

        # Click on the "Easy apply" link
        easy_apply_link.click()

        time.sleep(10)

        results_header = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list__subtitle"))
        )

        time.sleep(5)

        
        # Retrieve the text within the <small> element
        results_text = results_header.text

        # Extract the number of results
        num_results = results_text.split()[0].replace(',', '')

        print(num_results)
 

       
        # Wait to load page
        time.sleep(2)


        easy_apply_links = WebDriverWait(self.driver, 10).until(

            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search-results__list-item"))

        )

        current_page_number = 1

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        try:
            page_number_elements = self.driver.find_elements(By.CSS_SELECTOR, "li[data-test-pagination-page-btn] button[aria-label^='Page']")
            last_page_number = max(int(button.get_attribute('aria-label').split()[-1]) for button in page_number_elements)
        except NoSuchElementException:
            last_page_number = current_page_number

        print(last_page_number)  

        # Find the div
        div_element = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list")

        job_titles = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container__link"))
        )   

        easy_apply_links = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search-results__list-item"))
        ) 
                
        # Scroll within the div until no more new content is loaded
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", div_element)
        while True:
            # Scroll down to bottom
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", div_element)

            # Wait to load page
            time.sleep(2) #adjust this sleep as needed

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", div_element)
            if new_height == last_height:
                break
            last_height = new_height

            job_titles = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container__link"))
            ) 

            easy_apply_links = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search-results__list-item"))
            )  

        # get the total number of job titles
        num_job_titles = len(job_titles)

        # get the total number of job titles
        num_easy_apply_links = len(easy_apply_links)

        jobs_per_page = 25 

        print(num_easy_apply_links)  


        print(easy_apply_links) 

        for i in range(3, last_page_number): # page numbers start from 1
        # The rest of your job search logic, such as scrolling and extracting job titles
             # Start by navigating to the page first:
            self.driver.get(f"https://www.linkedin.com/jobs/search/?f_AL=true&keywords=intern%20web&start={i*25}")

            time.sleep(5)

            easy_apply_links = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search-results__list-item"))
            ) 

            time.sleep(5)
            

            for index, easy_apply_link in enumerate(easy_apply_links):

                # Find the div
                div_element = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list")
                
                # Scroll within the div until no more new content is loaded
                last_height = self.driver.execute_script("return arguments[0].scrollHeight", div_element)
                while True:
                # Scroll down to bottom
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", div_element)

                # Wait to load page
                    time.sleep(2) #adjust this sleep as needed

                # Calculate new scroll height and compare with last scroll height
                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", div_element)
                    if new_height == last_height:
                        break
                    last_height = new_height

                job_title = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-list__title"))
                )  

                time.sleep(5)

                

                easy_apply_link_text = easy_apply_link.text
                print(easy_apply_link_text)
                # Click on the job title
                easy_apply_link.click()
                time.sleep(5)

                # Switch to the new tab
                self.driver.switch_to.window(self.driver.window_handles[0])
                
                try:
                    # Find the "jobs_apply_button" element
                    jobs_apply_button = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-apply-button"))
                    )
                    # Check if the button is enabled
                    if jobs_apply_button.is_enabled():
                        # Check if the button redirects to another page by inspecting its text
                        button_text = jobs_apply_button.text.strip().lower()  # Get the button text, remove extra spaces and convert to lowercase
                        if button_text == "apply":
                            print("Button redirects to another page. Skipping to the next job.")
                            continue  # Skip to the next job
                        else:
                            print("Button is enabled")
                            jobs_apply_button.click()
                    # rest of your code to handle the case when the job is applied successfully...
                    else:
                        print("Button is disabled. Skipping to the next job.")
                        continue  # Skip to the next job
                    
                except TimeoutException:
                    print('You already applied to this job, go to next...')
                    continue
                    time.sleep(5)
                    # Find the "jobs_apply_button" element
                    jobs_apply_button = WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-apply-button"))
                    )
                    # Click on the "Easy apply" button
                    jobs_apply_button.click()


                    time.sleep(5)
                submit_application_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary"))
                )

                submit_application_button_text = submit_application_button.text

                if submit_application_button_text == "Submit Application":
                    # Click on the submit application button
                    submit_application_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary"))
                    )
                    submit_application_button.click()

                    # Close the tab
                    time.sleep(5)

                   
                        

                else:
                    # Close the tab
                    time.sleep(5)

                    # Click on the "next button"
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary"))
                    )
                    next_button.click()

                    time.sleep(5)

                    # Click on the "next button"
                    review_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary"))
                    )
                    review_button_text = review_button.text

            # If the text of the review button is not "Review", close the job application form
                if review_button_text == "Review":
                    # Click on the review button
                    review_button.click()
                    submit_application_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-button--primary"))
                    )
                    submit_application_button.click()
                            
                    time.sleep(5)

                    close_job_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-modal__dismiss "))
                    )
                    close_job_button.click()

                    time.sleep(5)
                else:
                    close_job_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-modal__dismiss "))
                    )
                    close_job_button.click()
                    time.sleep(5)
                    
                    discard_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".artdeco-modal__confirm-dialog-btn")
                    if discard_buttons:  # if the list is not empty, i.e., the button exists
                        # discard button found, click it
                        discard_button = discard_buttons[0]  # get the first (and likely only) button from the list
                        discard_button.click()
                        time.sleep(5)
                    else:
                        # discard button not found, skip it
                        print('You already closed this job, go to next...')
                        continue
                    
                        

            

        

        

        

               

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.login_linkedin()
    bot.job_search()
    
