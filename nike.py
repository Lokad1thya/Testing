import urllib.parse  # Add this import statement at the top of your script
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def search_nike_products(search_query):
    encoded_query = urllib.parse.quote_plus(search_query)
    base_url = 'https://www.nike.com/in/w?q='
    search_url = f"{base_url}{encoded_query}"
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    results = []
    
    try:
        print(f'Navigating to {search_url}')
        driver.get(search_url)
        
        # Wait for the product cards to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card'))
        )
        
        # Scroll to the bottom to load more content
        print('Scrolling to the bottom to load more content')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        
        # Wait for more content to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card'))
        )
        
        products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')
        if not products:
            print("No products found. Printing page content for debugging:")
            print(driver.page_source)
        else:
            for product in products:
                try:
                    link = product.find_element(By.CSS_SELECTOR, 'a.product-card__link-overlay')
                    link = link.get_attribute('href') if link else '#'
                    absolute_link = link if link.startswith('http') else f"https://www.nike.com{link}"
                    
                    title = product.find_element(By.CSS_SELECTOR, 'div.product-card__title')
                    title = title.text.strip() if title else 'No title available'
                    
                    subtitle = product.find_element(By.CSS_SELECTOR, 'div.product-card__subtitle')
                    subtitle = subtitle.text.strip() if subtitle else 'No subtitle available'
                    
                    price = product.find_element(By.CSS_SELECTOR, 'div.product-card__price-wrapper')
                    price = price.text.strip() if price else 'No price available'
                    
                    image = product.find_element(By.CSS_SELECTOR, 'img.product-card__hero-image')
                    image_url = image.get_attribute('src') if image else 'No image available'

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
    
    finally:
        driver.quit()
    
    return results
