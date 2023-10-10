from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import os
import shutil
import openai

website = "https://arxiv.org/list/cs/new"

# A class to hold the attributed of a single arxiv paper
class Article:
    def __init__(self, title: str, link: str, abstract: str):
        self.title = title
        self.link = link
        self.abstract = abstract
    
    def get_abstract(self) -> str:
        return self.abstract
    
    def get_title(self) -> str:
        return self.title

    def __str__(self):
        return f"Title: {self.title}\nLink: {self.link}\nAbstract: {self.abstract}"


def main():
    print("Rah running...")
    # Create todays working directory - delete if already here
    create_directory()
    # load the keywords for filtering papers
    keywords = load_keywords()
    print("loaded {} keywords".format(len(keywords)))
    # get all the new papers for today
    articles = get_articles()
    print("{} total articles found today".format(len(articles)))
    #filter all the papers based on they current keywords
    filtered_articles = filter_articles_by_keyword(keywords, articles)
    print("{} filtered articles found today".format(len(filtered_articles)))
    print_top_ten(filtered_articles)


# Create a working directory based on today's date
def create_directory():
    current_date = datetime.date.today()
    directory_path = str(current_date)
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

    os.makedirs(directory_path)


# load the keywords for filtering papers
def load_keywords():
    keywords = []
    try:
        with open('keywords', 'r') as file:
            # Read all lines from the file and strip whitespace from each line
            lines = file.readlines()
            # Create the keywords array by removing any additional whitespace around each word
            keywords = [line.strip() for line in lines if line.strip() != ""]
    except Exception as e:
        print(str(e))

    return keywords

# get all the new papers for today
def get_articles():
    articles = []
    try:
        # arxiv uses <DL> tags to list the  entries - one <DL> tag for new entries, one for Cross-listing and one for Replacements.
        # we will ignore the replacements for now
        dl_tags = driver.find_elements(By.TAG_NAME, "dl")
        for x in range(0, len(dl_tags)-1):
            # article link is in the DT tag 
            dt_tags = dl_tags[x].find_elements(By.TAG_NAME, "dt")

            # article abstract is in the dd tag.
            dd_tags = dl_tags[x].find_elements(By.TAG_NAME, "dd")

            # number of dt_tags should match # of dd_tags
            # lets get the article link and pair it with the article abstract
            for a in range(0, len(dt_tags)):
                all_links = dt_tags[a].find_elements(By.TAG_NAME, "a")
                pdf_link = all_links[2].get_attribute("href")
                
                title_div_tags = dd_tags[a].find_elements(By.TAG_NAME, "div")
                title = title_div_tags[1].get_attribute("innerHTML").split('</span>')[1]
            
                ptags = dd_tags[a].find_elements(By.TAG_NAME, "p")#[-].get_attribute("innerHTML")
                abstract = ptags[0].get_attribute("innerHTML")

                article = Article(title, pdf_link, abstract)
                articles.append(article)
    except Exception as e:
        print(str(e))

    driver.close()

    return articles


def filter_articles_by_keyword(keywords, articles):
    filtered_articles = []
    try:
        for article in articles:
            for keyword in keywords:
                if keyword in article.get_title():
                    filtered_articles.append(article)
                    break
    except Exception as e:
        print(str(e))

    return filtered_articles
                

def print_top_ten(filtered_articles):
    for x in range(0, 9):
        print(filtered_articles[x].get_abstract())
        print("\n*********************\n")


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(website)
    main()
