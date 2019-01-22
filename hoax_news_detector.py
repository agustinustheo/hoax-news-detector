import re
import bs4
import lxml
import nltk
import pickle
import urllib.request
from google import google
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

def preproccess_text(text_messages):
	# change words to lower case - Hello, HELLO, hello are all the same word
	processed = text_messages.lower()

	# Remove remove unnecessary noise
	processed = re.sub(r'\[[0-9]+\]|\[[a-z]+\]|\[[A-Z]+\]|\\\\|\\r|\\t|\\n|\\', ' ', processed)

	# Remove punctuation
	processed = re.sub(r'[.,\/#!%\^&\*;\[\]:|+{}=\-\'"_`~()?]', ' ', processed)

	# Replace whitespace between terms with a single space
	processed = re.sub(r'\s+', ' ', processed)

	# Remove leading and trailing whitespace
	processed = re.sub(r'^\s+|\s+?$', '', processed)
	return processed

def remove_unnecessary_noise(text_messages):
	processed = text_messages.replace(' di ', ' ')
	processed = processed.replace(' ke ', ' ')
	processed = processed.replace(' yang ', ' ')
	processed = processed.replace(' dan ', ' ')

	return processed

def news_title_tokenization(message):
	tokenized_news_title = word_tokenize(message)

	return tokenized_news_title

news_title = "ahok bebas penjara"

news_title_tokenized = news_title_tokenization(news_title)

search_title = ""

for word in news_title_tokenized:
	search_title = search_title + word + " "

def find_features(message):
	words = word_tokenize(message)
	features = {}
	for word in news_title_tokenized:
		features[word] = (word in words)

	return features

num_page = 4
search_results = google.search(search_title, num_page)

is_news_hoax = 0
for result in search_results:
	flag = 0
	search_result_title = result.name.split('http')[0]
	search_result_title = remove_unnecessary_noise(search_result_title.split('...')[0])
	search_result_title = preproccess_text(search_result_title)

	conclusion = find_features(preproccess_text(search_result_title))

	for word in news_title_tokenized:
		if conclusion[word] == True:
			flag = flag + 1

	if flag == len(news_title_tokenized):
			is_news_hoax = is_news_hoax + 1

if is_news_hoax > 4:
	print('Not Fake News!')
else:
	print('Fake News!')

def cleanMe(html):
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

webpage = str(urllib.request.urlopen('https://www.washingtonpost.com/powerpost/no-cave-trump-pelosi-vow-not-to-yield-in-government-shutdown-standoff/2019/01/22/1b6258bc-1e4b-11e9-8e21-59a09ff1e2a1_story.html?noredirect=on&utm_term=.2e3bfa71c3d5').read())
cleantext = cleanMe(webpage)
cleantext = re.sub(r'\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])', '', cleantext)
cleantext = re.sub(r'\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])\\([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])([a-z]|[A-Z]|[0-9])', '', cleantext)
cleantext = preproccess_text(cleantext)

# indonesian_sent_tokenizer_f = open("indonesian_sent_tokenizer.pickle", "rb")
# indonesian_sent_tokenizer = pickle.load(indonesian_sent_tokenizer_f)
# indonesian_sent_tokenizer_f.close()

print(cleantext)