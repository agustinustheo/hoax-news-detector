import re
from google import google
from nltk.tokenize import word_tokenize

def preproccess_text(text_messages):
	# change words to lower case - Hello, HELLO, hello are all the same word
	processed = text_messages.lower()

	# Remove punctuation
	processed = re.sub(r'[.,\/#!%\^&\*;:|+{}=\-\'"_`~()?]', ' ', processed)

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

news_title = "donald trump government shutdown"

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