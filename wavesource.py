from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os  # Fix for missing 'os' module

# Define the target URL
url = "https://odnature.naturalsciences.be/marine-forecasting-centre/nl/graphs/sea_surface_wave_significant_height/Oostende"

# Set up Selenium WebDriver with Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Load the webpage
    driver.delete_all_cookies()
    driver.get(url)

    # Wait for the table to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@id, 'timeSeriesTable')]"))
    )

    # Parse the webpage
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Find today's expected table ID
    today_tab_id = datetime.now().strftime("timeSeriesChartTable%d%m")
    today_tab = soup.find("div", {"id": today_tab_id})

    # Extract table ID
    table_id = today_tab_id.replace("timeSeriesChartTable", "timeSeriesTable") if today_tab else sorted(tab_ids)[-1].replace("timeSeriesChartTable", "timeSeriesTable")
    if not table_id:
        print("Today's tab not found. Using latest available tab.")
        all_tabs = soup.find_all("div", class_="timeseries-tab tab-pane fade")
        tab_ids = [tab["id"] for tab in all_tabs if "timeSeriesChartTable" in tab["id"] and "MaxMin" not in tab["id"]]
        table_id = sorted(tab_ids)[-1].replace("timeSeriesChartTable", "timeSeriesTable")  # Fallback


    # Locate the correct table
    table = soup.find("table", {"id": table_id})
    if not table:
        print(f"Table {table_id} not found.")
    else:
        rows = table.find_all("tr")[1:]
        wave_data = [(td.text.strip() for td in row.find_all("td")) for row in rows]

        # Add current date to each row for historical tracking
        current_date = datetime.now().strftime("%Y-%m-%d")
        wave_data_with_date = [(current_date,) + tuple(row) for row in wave_data]

        # Convert to DataFrame with Date column
        wave_df = pd.DataFrame(wave_data_with_date, columns=["Date", "Time", "Wave Height (m)", "Swell Percentage (%)"])

        # Append instead of overwrite
        csv_filename = "wave_height_data_full.csv"
        wave_df.to_csv(csv_filename, index=False, encoding="utf-8", mode="a", header=not os.path.exists(csv_filename))

        print(f"Data appended to {csv_filename}")

except Exception as e:
    print(f"Error retrieving data: {e}")
