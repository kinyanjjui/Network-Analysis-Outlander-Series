
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys inport Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import re
import warnings


# Creating The Driver
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
warnings.filterwarnings("ignore", category=DeprecationWarning)

#wiki url character list
wiki_url = 'https://outlander.fandom.com/wiki/Category:Characters'
driver.get(wiki_url)

#finding characters by book
Book_categories = driver.find_elements(By.CLASS_NAME,'category-page__member-link')
#get page link redirecting to page showing characters for each book
for i in range(len(Book_categories)):
    if re.search("^Category:Characters by book", Book_categories[i].text):
        book_link = Book_categories[i].get_attribute('href')
        
driver.get(book_link)

novels = driver.find_elements(By.CLASS_NAME,'category-page__member-link')
#contains other books by the author

Book_list = ['Outlander',
             'Dragonfly in Amber',
             'Voyager',
             'Drums of Autumn','The Fiery Cross',
             'A Breath of Snow and Ashes',
             'An Echo in the Bone',
             'Go Tell the Bees That I Am Gone',
            ] ##list of the  main books in the series


books =[]
for bk in Book_list: ##filtering for only books in main series
    for i in range(len(novels)):
        book_title = novels[i].text.lstrip('Category:Characters in ')
        if bk in book_title:
        #The final book wont show debugg later
            book_url = novels[i].get_attribute('href')
            books.append({'book_title': book_title, 'url':book_url})
            
print(books)


Character_list= []

for book in books:
    driver.get(book['url'])
    Char_elems = driver.find_elements(By.CLASS_NAME, 'category-page__member-link')
    
    for Char in Char_elems:
        Character_list.append({'Book':book['book_title'], 'Character': Char.text})


character_df =pd.DataFrame(Character_list)
pd.set_option('display.max_rows', None)


#removing character names containing '/'
filt = character_df["Character"].str.contains('/')
character_df = character_df[~filt]

#dropping duplicates
character_df.drop_duplicates(subset="Character", keep='first', inplace=True)

character_df.to_csv(f'{os.getcwd()}/characters_csv', index=False)

#Characters per book
character_df['Book'].value_counts().plot(kind='bar')
plt.show()

print(character_df)

