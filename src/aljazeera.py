from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import requests
from bs4 import BeautifulSoup
import re as re
import time
import pandas as pd
import numpy as np

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

from wordcloud import WordCloud
from langdetect import detect
from textblob import TextBlob


def get_aljazeera():
    """With this function we get into aljazeera news website,getting all the ukraine war news, download the first 200 links of the actual news
    ( filtering the links they don't match with news/2)"""
    
    driver = webdriver.Chrome()
    url= 'https://www.aljazeera.com/'
    driver.get(url)
    time.sleep(10)
    cookies_accept = driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    ukraine_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Ukraine war').click()
    time.sleep(10)
    lnks=driver.find_elements(By.TAG_NAME,"a")
    lst_aljazeera=[lnk.get_attribute('href') for lnk in lnks]
    lst_aj=[url for url in lst_aljazeera if '/news/2' in url ]
    while len(lst_aj)<200:
        show_more = driver.find_element(By.CLASS_NAME, "show-more-button")
        driver.execute_script("arguments[0].scrollIntoView();",show_more)
        show_more= driver.find_element(By.CLASS_NAME, "show-more-button").click()
        time.sleep(3)
        lnks=driver.find_elements(By.TAG_NAME,"a")
        lst_aljazeera=[lnk.get_attribute('href') for lnk in lnks]
        lst_aj=[url for url in lst_aljazeera if '/news/2' in url ]
        if len(lst_aj)<200:
            continue
    return lst_aj


def create_dict_aj(lst_aj):
    
    """This function creates a dictionary relating the link of the news and its content, 
    cleaning the outcome of the last one"""
    
    dict_aj={}
    for url in lst_aj:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        article= soup.getText()
        article = article[article.find('facebooktwitterwhatsapp'):]
        article = article[:article.find('Source: Al Jazeera')]
        article = article.replace('\n','').replace('\xa0',' ').replace('facebooktwitterwhatsapp','')
        dict_aj[url]= article
    return dict_aj


def descriptives(dict_aj):
    
    """This function extracts the data we want getting how many times the words 'ukraine','war','russia','putin','zelensky'
    is repeated; it also includes sentimental analysis of each new creating a new dataframe with all these descriptives"""
    
    lst_polarity = [round(TextBlob(article).sentiment.polarity,5) for article in dict_aj.values()]
    lst_subjectivity = [round(TextBlob(article).sentiment.subjectivity,5) for article in dict_aj.values()]
    length=[len(articles) for articles in dict_aj.values()]
    ukraine=[articles.lower().count('ukraine') for articles in dict_aj.values()]
    war=[articles.lower().count('war') for articles in dict_aj.values()]
    russia=[articles.lower().count('russia') for articles in dict_aj.values()]
    putin = [articles.lower().count('putin') for articles in dict_aj.values()]
    zelensky= [articles.lower().count('zelensky') for articles in dict_aj.values()]
    dict_length= {'polarity':lst_polarity, 'subjectivity':lst_subjectivity,'length':length,'ukraine':ukraine,'war':war, 'russia':russia,'putin':putin,'zelensky':zelensky}
    df_aj_descr= pd.DataFrame(dict_length)
    return df_aj_descr

def create_df_aj(dict_aj):
    
    """This function creates a DataFrame with the links and articles, tnasposing and creating a new index to be able to
    join witht their descriptives"""
    
    idx= {'article'}
    df_aj= pd.DataFrame(dict_aj,idx).transpose().reset_index()
    df_aj= df_aj.rename(columns={"index": "link"})
    return df_aj