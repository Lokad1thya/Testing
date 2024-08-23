from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def search_vegnonveg_products(search_query):
    base_url = 'https://www.vegnonveg.com/search?q='
    search_url = f"{base_url}{search_query.replace(' ', '+')}"

    print(f'Search URL: {search_url}')  # Debugging line to check the constructed URL

    results = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(search_url)
        
        # Wait for the page to load and check for the presence of product items
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.gt-product-click'))
            )
        except TimeoutException:
            print("TimeoutException: Product items not found within the specified time.")
            return results
        
        # Extract product information
        products = driver.find_elements(By.CSS_SELECTOR, 'a.gt-product-click')
        if not products:
            print("No products found or incorrect HTML structure.")
        else:
            for product in products:
                try:
                    # Extract product link
                    link = product.get_attribute('href') if product else '#'
                    
                    # Extract product title
                    title_element = product.find_element(By.CSS_SELECTOR, 'span.p-name')
                    title = title_element.text.strip() if title_element else 'No title available'
                    
                    # Extract product price
                    price_element = product.find_element(By.CSS_SELECTOR, 'div.info p span')
                    price = price_element.text.strip() if price_element else 'No price available'
                    
                    # Extract product image URL
                    image_element = product.find_element(By.CSS_SELECTOR, 'img.img-normal')
                    image_url = image_element.get_attribute('src') if image_element else 'No image available'
                    
                    print(f'Link: {link}')
                    print(f'Title: {title}')
                    print(f'Price: {price}')
                    print(f'Image URL: {image_url}')
                    print('-' * 40)
                    
                    results.append({
                        'link': link,
                        'title': title,
                        'price': price,
                        'image_url': image_url
                    })
                except Exception as e:
                    print(f'Error occurred while processing a product: {e}')
    finally:
        driver.quit()
    
    return results
