from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from typing import List, Dict
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_next_page(driver, i):
    """
    Clicks the 'Next' button for pagination in LinkedIn search results, handling dynamic content loading.
    """
    try:
        # Scroll to the bottom to trigger LinkedIn to load more elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        
        # Wait until the next button is visible and clickable
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='Page {i}']")) 
        )

        # Scroll the button into view and click it
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        time.sleep(1)  # Let the browser adjust
        driver.execute_script("arguments[0].click();", next_button)
        
        print(f"Next {i} button clicked.")
        time.sleep(3)  # Wait for new results to load

        return True  # Indicate successful click

    except Exception as e:
        print(f"No next button found or error: {e}")
        return False  # Stop pagination if button isn't found

def login_linkedin(username, password, driver):
    """
    Logs into LinkedIn using provided credentials.
    """
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    if "login" in driver.current_url:
        email_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        email_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(5)  # Wait for login to complete

def search_linkedin_profiles(driver, search_query, max_results=20):
    """
    Searches LinkedIn for profiles based on the search query, storing URLs in a queue.
    """
    driver.get(f"https://www.linkedin.com/search/results/people/?keywords={search_query}")
    time.sleep(3)
    
    profile_links = []
    i = 1
    while len(profile_links) < max_results:
        profile_elements = driver.find_elements(By.XPATH, "//ul[@role='list']/li//div[@class='mb1']//a[contains(@href, '/in/')]")
        
        for profile in profile_elements:
            profile_url = profile.get_attribute("href")
            if profile_url not in profile_links:
                profile_links.append(profile_url)
            if len(profile_links) >= max_results:
                break
        
        if not click_next_page(driver, i):
                break  # Stop if no more pages exist

        i += 1  
    return profile_links


def get_profile_details(driver, profile_url):
    """
    Retrieves details of a specific LinkedIn profile.
    """
    driver.get(profile_url)
    time.sleep(3)
    
    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
        headline = driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium')]" ).text
    except:
        name, headline = "Unknown", "Not available"
    
    return {"name": name, "headline": headline, "url": profile_url}

def linkedin_search_tool(search_query: str, max_results: int = 20) -> List[Dict[str, str]]:
    """
    Searches LinkedIn for profiles matching the search query and retrieves details.
    
    Args:
        search_query (str): The name or keywords to search for on LinkedIn.
        max_results (int): The maximum number of profiles to retrieve.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing profile details.
    """

    options = webdriver.ChromeOptions()
    
    # Set the Brave browser binary
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # Use the same user profile to maintain session
    # options.add_argument("--user-data-dir=/Users/kush/Library/Application Support/BraveSoftware/Brave-Browser")
    options.add_argument("--user-data-dir=/Users/kush/Library/Application Support/Google/Chrome")
    
    options.add_argument("--profile-directory=Default")  # Change if using a different profile
    
    # Launch Selenium with the existing profile
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    
    try:
        username = os.getenv("LINKEDIN_USERNAME", "khush.grandhi@gmail.com")
        password = os.getenv("LINKEDIN_PASSWORD", "Ksm2612pl,")
        
        login_linkedin(username, password, driver)
        profiles = search_linkedin_profiles(driver, search_query, max_results)
        
        profile_details = [get_profile_details(driver, profile) for profile in profiles]
        
        return profile_details
    
    finally:
        driver.close()
if __name__ == "__main__":
    search_query = "Rivian AND Recruiter"
    max_results = 2
    results = linkedin_search_tool(search_query, max_results)
    print(results)
    for result in results:
        print(result)