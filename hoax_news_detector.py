from google import google
num_page = 3
search_results = google.search("vanessa angel sedang disidang", num_page)

for result in search_results:
	print(result.name.split('http')[0])