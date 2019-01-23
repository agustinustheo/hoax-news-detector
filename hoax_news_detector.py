import re
import bs4
import lxml
import nltk
import pickle
import urllib.request
from google import google
from googlesearch import search 
from newspaper import Article
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer

stopwords = nltk.corpus.stopwords.words('english')

def preproccess_text(text_messages):
	# change words to lower case - Hello, HELLO, hello are all the same word
	processed = text_messages.lower()

	# Remove remove unnecessary noise
	processed = re.sub(r'\[[0-9]+\]|\[[a-z]+\]|\[[A-Z]+\]|\\\\|\\r|\\t|\\n|\\', ' ', processed)

	# Remove punctuation
	processed = re.sub(r'[.,\/#!%\^&\*;\[\]:|+{}=\-\'"_”“`~(’)?]', ' ', processed)

	# Replace whitespace between terms with a single space
	processed = re.sub(r'\s+', ' ', processed)

	# Remove leading and trailing whitespace
	processed = re.sub(r'^\s+|\s+?$', '', processed)
	return processed

def remove_unnecessary_noise(text_messages):
	text_messages = re.sub(r'\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])', ' ', text_messages)
	text_messages = re.sub(r'\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])', ' ', text_messages)
	text_messages = re.sub(r'\[[0-9]+\]|\[[a-z]+\]|\[[A-Z]+\]|\\\\|\\r|\\t|\\n|\\', ' ', text_messages)

	return text_messages

def clean_article(html):
    soup = BeautifulSoup(html, features="lxml") # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def news_title_tokenization(message):
	tokenized_news_title = []
	ps = PorterStemmer()
	for word in word_tokenize(message):
		if word not in stopwords:
			tokenized_news_title.append(ps.stem(word))

	return tokenized_news_title

def news_text_tokenization(message):
	tokenized_news_text = []
	for word in word_tokenize(message):
		tokenized_news_text.append(word)

	return tokenized_news_text

def find_similar_articles(news):
	news_article = Article(news)
	news_article.download()
	news_article.parse()
	news_title_tokenized = news_title_tokenization(preproccess_text(news_article.title))

	search_title = ""
	for word in news_title_tokenized:
		search_title = search_title + word + " "


	num_page_searched = 4
	search_results = google.search(search_title, num_page_searched)

	found_similar_article = 0
	for result in search_results:
		flag = 0
		search_result_title = result.name.split('http')[0]
		search_result_title = remove_unnecessary_noise(search_result_title.split('...')[0])
		search_result_title = preproccess_text(search_result_title)
		search_result_title = news_title_tokenization(search_result_title)

		result_string = ""
		for w in search_result_title:
			result_string = result_string + w + " "
		
		corpus = []
		corpus.append(search_title)
		corpus.append(result_string)
		
		vectorizer = CountVectorizer()
		features = vectorizer.fit_transform(corpus).todense()

		for f in features:
			dist = euclidean_distances(features[0], f)

		if dist < 2.5:
			found_similar_article = found_similar_article + 1

	if found_similar_article > 1:
		print('Found similar article titles!')
	elif found_similar_article == 1:
		print('Found a similar article title!')
	else:
		print('No similar article titles found!')

find_similar_articles("https://www.washingtonpost.com/powerpost/no-cave-trump-pelosi-vow-not-to-yield-in-government-shutdown-standoff/2019/01/22/1b6258bc-1e4b-11e9-8e21-59a09ff1e2a1_story.html?noredirect=on&utm_term=.deb595387de7")