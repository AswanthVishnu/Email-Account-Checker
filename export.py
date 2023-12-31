from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

def check_pinterest_account(email, result_dict):
    url = 'https://in.pinterest.com/'
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mweb-unauth-container"]/div/div/div[1]/div/div[2]/div[2]/button/div/div'))
        )
        login_button.click()

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )

        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        time.sleep(2)

        error_message = None
        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="email-error"]/div/div/div[2]'))
            )
        except:
            pass

        if error_message:
            result_dict[email].append("Pinterest")

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        result_dict[email].append("Error")

    finally:
        driver.quit()

def check_spotify_account(email, result_dict):
    url = 'https://www.spotify.com/in-en/signup'
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
        )

        email_input.send_keys(email)
        email_input.submit()

        try:
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="Wrapper-sc-62m9tu-0 POdTa encore-warning-set AlreadyInUseBanner__StyledBanner-sc-1j4rkgm-0 jMBpIH"]'))
            )
            result_dict[email].append("Spotify")
        
        except TimeoutException:
            next_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="submit"]'))
            )
            next_button.click()

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        result_dict[email].append("Error")
    
    finally:
        driver.quit()

def check_quora_account(email, result_dict):
    url = 'https://www.quora.com/'
    driver = webdriver.Chrome()

    try:
        driver.get(url)

        email_input = driver.find_element(By.ID, 'email')
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        time.sleep(2)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        error_message_div = soup.find('div', {'class': 'qu-color--red_error'})
        if error_message_div:
            result_dict[email].append("Quora")

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        result_dict[email].append("Error")

    finally:
        driver.quit()

if __name__ == "__main__":
    with open('emails.txt', 'r') as file:
        email_list = file.read().splitlines()

    # Dictionary to store results for each email
    results = {email: [] for email in email_list}

    # Check accounts for each email
    for email in email_list:
        print(f"\nChecking email: {email}")
        check_quora_account(email, results)
        check_pinterest_account(email, results)
        check_spotify_account(email, results)

    # Write results to output.txt
    with open('output.txt', 'w') as output_file:
        for email, platforms in results.items():
            if platforms:
                output_file.write(f"{email} is linked to: {', '.join(platforms)}\n")
            else:
                output_file.write(f"{email} has no accounts.\n")
