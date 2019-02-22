def find_similar_articles(news, similarity):
    news_title_tokenized = ""
    
    if(re.match(r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$', news)):
        news_article = Article(news)
        news_article.download()
        news_article.parse()
        news_title_tokenized = news_title_tokenization(preproccess_text(news_article.title))
    else:
        news_title_tokenized = news_title_tokenization(preproccess_text(news))

    search_title = ""
    for word in news_title_tokenized:
        search_title = search_title + word + " "

    num_page_searched = 1
    search_results = google.search(search_title, num_page_searched)

    similar_articles = []
    for result in search_results:
        similar_article = {}
        search_result_title = result.name.split('http')[0].split('...')[0]
        search_result_title = remove_unnecessary_noise(search_result_title)
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

        if dist < similarity:
            similar_article["article_title"] = result.name.split('http')[0].split('...')[0]
            similar_article["article_url"] = result.link
            similar_articles.append(similar_article)

    return similar_articles
