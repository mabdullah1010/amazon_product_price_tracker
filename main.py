import requests
import os
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Not A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
}


URL = ("https://www.amazon.com/MATEIN-Backpack-Business-Approved-Rucksack/dp/B07QN9NPKN/"
       "ref=sr_1_3?crid=1F0OZHJYGHFDH&dib=eyJ2IjoiMSJ9.muYQp3WuFnSiPvrb8GnOoOFAP_"
       "1e_5o8Bgu7v7IFvyxGxSlBWh6vtrOgbz8jrvwLGuBNRJu1VljCOh7ThDOfVzEUWmnSOx0foZF6pBZUp_"
       "Fo3EgI2NL4z8gRlVQ5fwmyocVpxYlyepe4u5RGTGW4Ly7wNhySsCCVvTPEAroHFi96GeU_a-BvZxGOLSbLwh_"
       "ojUDxzWBT1FQpwUHH3pJsdB_XJWka_rtofnyeHOgn8L8.y2x4obrbtXsYA21V_sg-sF7qUxpUJsDjtEmIQfX"
       "1FwM&dib_tag=se&keywords=laptop%2Bbackpack&qid=1722679069&sprefix=lapt%2Caps%2C318&sr="
       "8-3&th=1")

response = requests.get(url=URL, headers=headers)
page = response.text
soup = BeautifulSoup(page, "html.parser")
target_price = 26.99
price = soup.find(name="span", class_="a-offscreen")
final_price = float(str(price.text)[1: len(str(price.text))])
title = (soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break")).text.strip()

if final_price <= target_price:
    my_email = MY_EMAIL
    my_password = MY_PASSWORD
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=RECEIVER_EMAIL,
                            msg=f"Subject:Amazon Price Alert \n\nThe price of your product {title} is ${final_price},"
                                f"which is below your target price of ${target_price}. \nBuy it now! \n {URL}")
    print("EMAIL SENT")
else:
    print(f"The price of your product {title} is ${final_price} which is above your target price of ${target_price}. "
          f"\nEmail not sent  "
          f"\n{URL}")
