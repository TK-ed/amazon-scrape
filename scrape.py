import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}
dta = {"customer-action": "pagination"}
base = "https://www.amazon.in/s?k=gpu&page=1&crid=1BPASLKAZJMY9&qid=1720417227&sprefix=gpu%2Caps%2C465&ref=sr_pg_2"
url_domain = "https://www.amazon.in"

rsp = requests.get(base, headers=headers)
soup = BeautifulSoup(rsp.content, "html.parser")
products = soup.select("div", class_="sg-col-inner")
processed_names = set()
processed_prices = set()
processed_urls = set()
processed_ratings = set()
processed_reviews = set()

with open("products.csv", "a", newline="") as f:
    writer = csv.writer(f)

    for product in products:

        try:
            # Name Extraction
            name_elements = product.select(
                "span.a-size-medium.a-color-base.a-text-normal"
            )
            if name_elements:
                name = name_elements[0].text
                if name not in processed_names:
                    processed_names.add(name)
                    writer.writerow(["Product Name", name])

            # Price Extraction
            price_elements = product.select("span.a-price-whole, span.a-offscreen")
            if price_elements:
                price = price_elements[0].text
                if price not in processed_prices:
                    processed_prices.add(price)
                    writer.writerow(["Product Price", price])  # Write directly

            # URL Extraction
            url_element = product.find_all(
                "a",
                class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
                href=True,
            )
            if url_element:
                url = url_element[0].get("href")
                if url not in processed_urls:
                    main_url = url_domain + url
                    processed_urls.add(main_url)
                    writer.writerow(["Product URL", main_url])

            # Rating Extraction (assuming rating is within span.rating-value)
            rating_element = product.find_all("span", class_="a-icon-alt")
            if rating_element:
                rating = rating_element[0].text
                if rating not in processed_ratings:
                    processed_ratings.add(rating)
                    writer.writerow(["Rating", rating])

            # Review Extraction (assuming reviews are within span.a-size-base.s-underline-text)
            reviews_element = product.find_all(
                "span", class_="a-size-base s-underline-text"
            )
            if reviews_element:
                reviews = reviews_element[0].text
                if reviews not in processed_reviews:
                    processed_reviews.add(reviews)
                    writer.writerow(["Reviews", reviews])

        except AttributeError:
            pass

print(processed_names, end="\n\n")
print(processed_prices, end="\n\n")
print(processed_ratings, end="\n\n")
print(processed_reviews, end="\n\n")
print(processed_urls, end="\n\n")
