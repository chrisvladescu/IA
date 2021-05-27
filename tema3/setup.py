import os
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from constants import PATH, SUMMARY_PATH

"""
    Functie pentru construirea setului de date.
    Incarc datele din fisiere, avand grija sa salvez toate campurile necesare.
    Fiecarui articol ii asociez si summary ul existent.
"""


def collect_data():
    articles = []
    entries = os.listdir(PATH)
    count = 0
    for entry in entries:
        subdirectory_path = PATH + '/' + entry
        summary_path = SUMMARY_PATH + '/' + entry
        raw_files = os.listdir(subdirectory_path)
        files = []
        for raw_file in raw_files:
            file_path = subdirectory_path + '/' + raw_file
            article = {}
            file_summary_path = summary_path + '/' + raw_file

            with open(file_path, 'r') as current_file:
                article["text"] = current_file.read()
                article["id"] = count
                article["name"] = raw_file

            with open(file_summary_path, 'r') as summary_file:
                article["summary"] = summary_file.read()
            files.append(article)
            count += 1
        cat = {"category": entry,
               "articles": files}
        articles.append(cat)
    return articles


"""
    Functie pentru incarcare stop words din fisierul dat.
"""


def load_stop_words():
    stop_words = []
    raw_words = []
    with open('stop_words', 'r') as f:
        raw_words = f.readlines()

    for word in raw_words:
        word = word.rstrip()
        stop_words.append(word)

    return stop_words


"""
    Functie pentru procesarea textului.
    Se determina token urile textului, sunt extrase stop words si se lematizeaza
    termenii ramasi.
    Aceste date sunt salvate in dictionarul articol, sub forma de liste.
"""


def process_text(articles, stop_words):
    lemmatizer = WordNetLemmatizer()
    for subset in articles:
        for article in subset["articles"]:
            lemmatized_text = []
            tokens = word_tokenize(article["text"])
            article["tokens"] = tokens
            article["no_stopwords"] = [
                word for word in tokens if not word in stop_words]
            for word in article["no_stopwords"]:
                word = lemmatizer.lemmatize(word)
                lemmatized_text.append(word)
            article['lematized'] = lemmatized_text

    return articles


"""
    Functie care returneaza setul de date sub forma unei liste.
"""


def load_setup():
    articles = collect_data()
    stop_words = load_stop_words()
    articles = process_text(articles, stop_words)
    return articles
