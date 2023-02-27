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


def get_bbc():
    """With this function we get into bbc news website,getting all the ukraine war news, download the first 200 links of the actual news
    ( filtering the links they don't match with news like live content or help content)"""
    driver = webdriver.Chrome()
    url= 'https://www.bbc.com/news'
    driver.get(url)
    time.sleep(5)
    cookies_accept = driver.find_element(By.CLASS_NAME, 'fc-button').click()
    search_bar     = driver.find_element(By.CLASS_NAME, 'ux-v5').click()
    search_bar     = driver.find_element(By.ID, 'search-input')
    search_bar.send_keys('Ukraine war')
    search_bar.send_keys(Keys.RETURN)
    
    lst_bbc_ukr=[]
    while len(lst_bbc_ukr)<200:
        lnks           = driver.find_elements(By.TAG_NAME,"a")
        lst_bbc        = [lnk.get_attribute('href') for lnk in lnks]
        lst_bbc_       = [url for url in lst_bbc if '/news/' in url and '/help' not in url and '/live/' not in url]
        search_bar = driver.find_element(By.LINK_TEXT, 'next page').click()
        for i in lst_bbc_:
            lst_bbc_ukr.append(i)
    return lst_bbc_ukr

def bbc_list(lst_bbc_ukr):
    """This function creates a dictionary relating the link of the news and its content, 
    cleaning the outcome of the last one"""
    dict_article_bbc={}
    for url in lst_bbc_ukr:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        article=soup.getText().replace('\'', "´").strip()
        dict_article_bbc[url]=article
    return dict_article_bbc

def descriptives(dict_article_bbc):
    
    """This function extracts the data we want getting how many times the words 'ukraine','war','russia','putin','zelensky'
    is repeated; it also includes sentimental analysis of each new creating a new dataframe with all these descriptives"""
    
    length=[len(articles) for articles in dict_article_bbc.values()]
    lst_polarity = [round(TextBlob(article).sentiment.polarity,5) for article in dict_article_bbc.values()]
    lst_subjectivity = [round(TextBlob(article).sentiment.subjectivity,5) for article in dict_article_bbc.values()]
    ukraine=[articles.lower().count('ukraine') for articles in dict_article_bbc.values()]
    war=[articles.lower().count('war') for articles in dict_article_bbc.values()]
    russia=[articles.lower().count('russia') for articles in dict_article_bbc.values()]
    putin = [articles.lower().count('putin') for articles in dict_article_bbc.values()]
    zelensky= [articles.lower().count('zelensky') for articles in dict_article_bbc.values()]
    dict_length= {'polarity':lst_polarity,'subjetivity':lst_subjectivity,'length':length,'ukraine':ukraine,'war':war, 'russia':russia,'putin':putin,'zelensky':zelensky}
    df_descriptive= pd.DataFrame(dict_length)
    return df_descriptive

def create_df_bbc(dict_article_bbc):
    
    """This function creates a DataFrame with the links and articles, tnasposing and creating a new index to be able to
    join witht their descriptives"""
    
    
    idx= {'article'}
    df_bbc= pd.DataFrame(dict_article_bbc,idx).transpose().reset_index()
    df_bbc= df_bbc.rename(columns={"index": "link"})
    return df_bbc

