# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Importing credentials from a separate file (credentials.py)
from credentials import username, pswd

# Setting the URL for Bitcoin historical data
url = "https://www.investing.com/crypto/bitcoin/historical-data"

# Defining a class to grab cryptocurrency historical data


class CryptoValueGrabber():
    def __init__(self, url):
        # Initializing a WebDriver instance for the Edge browser
        self.driver = webdriver.Edge()
        self.driver.get(url)
        time.sleep(5)

        # Scrolling to a certain position on the webpage
        self.driver.execute_script("window.scrollTo(0,280)")
        time.sleep(2)

        # Clicking on a link to open a login form
        self.driver.find_element(
            By.XPATH, '//*[@id="column-content"]/div[4]/div/a').click()
        time.sleep(5)

        # Filling in login credentials
        self.driver.find_element(
            By.ID, "loginFormUser_email").send_keys(username)
        self.driver.find_element(
            By.ID, "loginForm_password").send_keys(pswd)
        time.sleep(3)
        # Clicking the login button
        self.driver.find_element(By.XPATH, '//*[@id="signup"]/a').click()
        time.sleep(10)

        # Clicking on a widget field
        self.driver.find_element(By.ID, 'widgetField').click()
        time.sleep(2)

        # Setting start date for data
        self.driver.find_element(By.ID, 'startDate').clear()
        self.driver.find_element(By.ID, 'startDate').send_keys("01/01/2008")
        time.sleep(2)

        # Setting end date for data
        self.driver.find_element(By.ID, 'endDate').clear()
        self.driver.find_element(By.ID, 'endDate').send_keys("01/01/2030")
        time.sleep(2)

        # Applying date range
        self.driver.find_element(By.XPATH, '//*[@id="applyBtn"]').click()
        time.sleep(3)
        # Clicking again on the widget field
        self.driver.find_element(
            By.XPATH, '//*[@id="column-content"]/div[4]/div/a').click()
        time.sleep(5)


# Creating an instance of the CryptoValueGrabber class
CryptoValueGrabber(url, username, pswd)


# Reading cryptocurrency historical data from a CSV file
data = pd.read_csv(
    r"C:\Users\bansa\Downloads\Bitcoin Historical Data - Investing.com.csv")

# Converting 'Date' column to datetime format and setting it as the index
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Renaming columns and replacing characters in the data
data = data.rename(
    columns={"Price": "Close", "Vol.": "Volume"}, errors="raise")
data.replace(",", "", regex=True, inplace=True)
data.replace("-", "0", regex=True, inplace=True)

# Converting 'Volume' values to numeric format
for i in data['Volume'].index:
    if 'K' in data.loc[i, 'Volume']:
        data.loc[i, 'Volume'] = float(
            data.loc[i, 'Volume'].replace("K", ""))*1000
    elif 'M' in data.loc[i, 'Volume']:
        data.loc[i, 'Volume'] = float(
            data.loc[i, 'Volume'].replace("M", ""))*1000000

# Converting selected columns to numeric format
data[['Close', 'Open', 'High', 'Low', 'Volume']] = data[[
    'Close', 'Open', 'High', 'Low', 'Volume']].apply(pd.to_numeric)

# Printing the processed data
print(data)
