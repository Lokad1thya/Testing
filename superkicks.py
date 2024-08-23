from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

def search_superkicks_products(search_query):
    # URL encode the search query
    encoded_query = urllib.parse.quote(search_query)
    base_url = 'https://www.superkicks.in/search?q='
    search_url = f"{base_url}{encoded_query}"
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    results = []
    
    try:
        print(f'Navigating to {search_url}')
        driver.get(search_url)
        
        # Use explicit waits to wait for product cards to load
        print('Waiting for product cards')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.st-product'))
        )

        # Scroll to the bottom and wait for more content to load
        print('Scrolling to the bottom to load more content')
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.st-product'))
            )
            time.sleep(2)  # Short wait to ensure content loads
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Find and process product cards
        products = driver.find_elements(By.CSS_SELECTOR, 'div.st-product')
        if not products:
            print("No products found. Printing page content for debugging:")
            print(driver.page_source)
        else:
            for product in products:
                try:
                    link_element = product.find_element(By.CSS_SELECTOR, 'figure.st-product-media a')
                    link = link_element.get_attribute('href') if link_element else '#'
                    absolute_link = link if link.startswith('http') else f"https://superkicks.in{link}"
                    
                    title_element = product.find_element(By.CSS_SELECTOR, 'div.st-product-name a')
                    title = title_element.text.strip() if title_element else 'No title available'
                    
                    subtitle_element = product.find_element(By.CSS_SELECTOR, 'div.st-secondary-title')
                    subtitle = subtitle_element.text.strip() if subtitle_element else 'No subtitle available'
                    
                    price_element = product.find_element(By.CSS_SELECTOR, 'div.st-product-price span.new-price')
                    price = price_element.text.strip() if price_element else 'No price available'
                    
                    image_element = product.find_element(By.CSS_SELECTOR, 'figure.st-product-media img')
                    image_url = image_element.get_attribute('src') if image_element else 'No image available'
                    
                    print(f'Link: {absolute_link}')
                    print(f'Title: {title}')
                    print(f'Subtitle: {subtitle}')
                    print(f'Price: {price}')
                    print(f'Image URL: {image_url}')
                    print('-' * 40)
                    
                    results.append({
                        'link': absolute_link,
                        'title': title,
                        'subtitle': subtitle,
                        'price': price,
                        'image_url': image_url
                    })
                except Exception as e:
                    print(f'Error occurred while processing a product: {e}')
    
    except Exception as e:
        print(f'Error: {e}')
        print(driver.page_source)
    
    finally:
        driver.quit()
    
    return results
