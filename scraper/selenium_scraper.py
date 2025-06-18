from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from models.book import Book

class BookScraper:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)

    def scrape_all_books(self, start_url: str) -> list[Book]:
        self.driver.get(start_url)
        all_books = []
        page_count = 0

        while page_count < 2:
            books = self.driver.find_elements(By.CLASS_NAME, "product_pod")

            for book in books:
                title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                price = book.find_element(By.CLASS_NAME, "price_color").text
                ref = book.find_element(By.XPATH, ".//img[@class='thumbnail']").get_attribute("src")
                all_books.append(Book(title=title, price=price, ref=ref))
            page_count += 1

            try:
                next_btn = self.driver.find_element(By.CLASS_NAME, "next")
                next_url = next_btn.find_element(By.TAG_NAME, "a").get_attribute("href")
                self.driver.get(next_url)
            except:
                break

        self.driver.quit()
        return all_books

