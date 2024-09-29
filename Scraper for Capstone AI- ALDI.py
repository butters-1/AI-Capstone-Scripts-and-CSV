# Import modules
import requests
import bs4
import csv
from datetime import datetime

# Specify the CSV file name
csv_file = 'aldi_products.csv'


# List of URLs to scrape
urls = [
    ("https://new.aldi.us/products/fresh-meat-seafood/fresh-beef/k/84", 1),  # Beef
    ("https://new.aldi.us/products/fresh-produce/fresh-fruit/k/89", 2),  # Fresh Fruit
    ("https://new.aldi.us/products/fresh-meat-seafood/fresh-poultry/k/86", 3),  # Poultry
    ("https://new.aldi.us/products/fresh-produce/fresh-vegetables/k/90", 4)  # Vegetables
]

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Store name
store_name = "ALDI"

# Open a CSV file for writing
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header row
    csvwriter.writerow(['Date', 'Store', 'Product Name', 'Price', 'Size', 'Category'])
    
    # Scrape each URL
    for url, category in urls:
        # Get the web page
        request_result = requests.get(url).text
        
        # Parse the HTML
        soup = bs4.BeautifulSoup(request_result, "html.parser")
        
        # Find product names, prices, and sizes
        products = soup.find_all("div", class_="product-tile__name")
        prices = soup.find_all("span", class_="base-price__regular")
        sizes = soup.find_all("div", class_="product-tile__unit-of-measurement")

        # Write product names, prices, sizes, date, store, and category to the CSV file
        for product, price, size in zip(products, prices, sizes):
            product_name = product.p.get_text(strip=True)
            price_value = price.span.get_text(strip=True)  # Get the price value
            size_value = size.p.get_text(strip=True)  # Get the size value
            csvwriter.writerow([current_date, store_name, product_name, price_value, size_value, category])  # Write to CSV

print("Data saved to aldi_products.csv")
