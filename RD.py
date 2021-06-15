from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from article_outline import ArticleOutline
from firebase_service import FirebaseService


def crawl():
    # webdriver settings
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    # go to website
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ncu.edu.tw/rd/tw/news/index.php")
    
    howpage = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/select')))
    howpage_list = list(howpage.text.strip().split())
    for i in range(len(howpage_list)):
        for j in range(1,11):
            fetchArticleOutline(driver, j)
        if i != len(howpage_list):
            # next page
            next_page = driver.find_element_by_link_text('下一頁')
            next_page.click()
    driver.quit()


def fetchArticleOutline(driver, index):
    global firebaseService

    try:
        # information of block
        article = WebDriverWait(driver, 1).until(EC.presence_of_element_located(
            (By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/table/tbody/tr[{index}]')))
    except:
        return

    try:
        # individual information
        category = WebDriverWait(article, 1).until(
            EC.presence_of_element_located((By.XPATH, './td[1]/a')))
        # print(category.text)

        news = WebDriverWait(article, 1).until(
            EC.presence_of_element_located((By.XPATH, './td[3]/span/a')))
        # print(news.text)

        link = WebDriverWait(article, 1).until(
            EC.presence_of_element_located((By.XPATH, './td[3]/span/a')))
        # print(link.get_attribute("href"))

        articleOutline = ArticleOutline(category.text, news.text, link.get_attribute("href"))

        # articleOutline.printJson()

        firebaseService.addArticleOutline(articleOutline)
    except:
        return

if __name__ == "__main__":
    firebaseService = FirebaseService()

    crawl()