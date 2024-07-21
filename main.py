from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scraper import Scraper
from ai_generator import Generator

class BlogCommenter:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        # Create a Service object
        
        # Initialize the WebDriver with the Service object
        self.driver = webdriver.Chrome()
        
        # Maximize the browser window
        self.driver.maximize_window()

    def post_comment(self, name, email, content):
        def perform_actions(driver, wait):
            try:
                # Open the URL
                print("Navigating to the URL...")
                driver.get("https://www.backblaze.com/blog/announcing-b2-live-read/")

                # Wait until the iframe is visible
                print("Waiting for the iframe to load...")
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/main/div/div[2]/div/iframe[1]')))
                
                # Switch to the iframe
                print("Switching to the iframe...")
                driver.switch_to.frame(iframe)
                
                # Wait until the comment box is visible using a CSS selector
                print("Waiting for the comment box to be visible...")
                comment_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"][aria-multiline="true"][contenteditable="true"]')))
                
                # Scroll to the comment box
                print("Scrolling to the comment box...")
                actions = ActionChains(driver)
                actions.move_to_element(comment_box).perform()

                # Type in a few words
                print("Typing in the comment box...")
                comment_box.send_keys(content)

                # Wait a bit to observe the result
                time.sleep(2)

                # Navigate to the name input field and type the name
                print(f"Entering the name '{name}'...")
                name_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/section/div/div[1]/form/div/div[4]/div/div/section/div[2]/p/input')))
                name_input.send_keys(name)
                time.sleep(2)

                # Navigate to the email input field and type the email
                print(f"Entering the email '{email}'...")
                email_input = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/section/div/div[1]/form/div/div[4]/div/div/section/div[2]/div[2]/p[1]/input')))
                email_input.send_keys(email)
                time.sleep(2)

                # Check the checkbox
                print("Checking the checkbox...")
                checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div/div/section/div/div[1]/form/div/div[4]/div/div/section/div[2]/div[2]/div[1]/label/input')))
                checkbox.click()
                time.sleep(2)

                # Click the comment button again
                print("Clicking the comment button ...")
                comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[1]/div/div/section/div/div[1]/form/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/button')))
                comment_button.click()

                # Wait a bit to observe the result
                time.sleep(5)

                return True
            except Exception as e:
                print(f"Error encountered: {e}")
                return False

        retry_limit = 3
        wait = WebDriverWait(self.driver, 20)
        for attempt in range(retry_limit):
            success = perform_actions(self.driver, wait)
            if success:
                break
            print(f"Retrying... ({attempt + 1}/{retry_limit})")
            time.sleep(2)  # Wait before retrying

        if not success:
            print("Failed after multiple attempts.")

    def close_driver(self):
        print("Script finished. The browser will remain open for a while.")
        time.sleep(5)
        self.driver.quit()




def main():
    scraper = Scraper()
    generator = Generator()
    
    commenter = BlogCommenter()
    blog_urls = ["https://www.backblaze.com/blog/ai-video-understanding-in-your-apps-with-twelve-labs-and-backblaze/", "https://www.backblaze.com/blog/announcing-event-notifications/"]
    subreddits = ['backblaze']
    scraped_content = scraper.scrape_and_merge_content(blog_urls, subreddits)
    
    comment = generator.generate_content(scraped_content["blog_content"], scraped_content["subreddit_content"])
    commenter.start_driver()
    commenter.post_comment("Parley", "parley@gmail.com", comment)
    commenter.close_driver()
    

if __name__ == "__main__":
    main()
