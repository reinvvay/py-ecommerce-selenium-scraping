import csv
from dataclasses import dataclass
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def get_single_page():
    driver = webdriver.Chrome()
    driver.get("https://webscraper.io/test-sites/e-commerce/more/")
    products = []
    for single in driver.find_elements(By.CLASS_NAME, "caption"):
        products.append(Product(
            title=single.find_element(By.CLASS_NAME, "title"),
            description=single.find_element(By.CLASS_NAME, "description"),
            price=single.find_element(By.CSS_SELECTOR, "[itemprop='price']"),
            rating=single.find_element(By.CSS_SELECTOR, "[itemprop='data-rating]'").get_attribute("data-rating"),
            num_of_reviews=single.find_element(By.CSS_SELECTOR, "[itemprop='reviewCount']"),
        ))

    return products


def write_to_csv(output_file):
    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        products = get_single_page()
        writer = csv.writer(csv_file)
        for product in products:
            writer.writerow(
                [product.title, product.description, product.price, product.rating, product.num_of_reviews]
            )


def get_all_products() -> None:
    write_to_csv("test.csv")


if __name__ == "__main__":
    get_all_products()
