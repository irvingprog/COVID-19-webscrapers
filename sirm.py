''' 
Webscrapper for COVID-19 database
https://www.sirm.org/
'''
import requests
from bs4 import BeautifulSoup
import wget


BASE_URL = 'https://www.sirm.org'
DB_NAME = 'category/senza-categoria/covid-19'

def download_db_page(page_number):
    url = '{}/{}/page/{}'.format(BASE_URL, DB_NAME, page_number)
    print(url)
    page = requests.get(url)
    return page.text

def download_case_page(url):
    print(' ', url)
    page = requests.get(url)
    return page.text

def get_images_url_from_page(page_as_text):
    soup = BeautifulSoup(page_as_text, 'html.parser')
    figures = soup.find_all('figure', class_='wp-block-image')

    images_urls = []
    for figure in figures:
        images_urls.append(figure.find_all('img')[0]['src'])

    return images_urls

def download_images(images_urls):
    for url in images_urls:
        name = url.split('/')[-1]
        wget.download(url, out='{}'.format(name))

def main():

    page_found = True
    page_number = 1
    while page_found:

        downloaded_page = download_db_page(page_number)

        soup = BeautifulSoup(downloaded_page, 'html.parser')
        error404 = soup.find_all('div', class_='td-404-sub-title')

        if error404:
            page_found = False
        else:
            readMoreButtons = soup.find_all('div', class_='td-read-more')

            for readMoreButton in readMoreButtons:
                anchor = readMoreButton.find_all('a')[0]
                case_page = download_case_page(anchor['href'])
                images_urls = get_images_url_from_page(case_page);
                download_images(images_urls)
        
        page_number += 1


if __name__ == '__main__':
    main()
