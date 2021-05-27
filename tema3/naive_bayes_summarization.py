from functions import split_articles
from functions import split_fold
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from setup import load_stop_words
from collections import Counter
from math import log
from constants import TYPE, SUMMARY_TYPE, SUMMARY_MODE, alpha
import re
from rouge_score import rouge_scorer

"""
    Functie ce imparte textul si sumarul articolului in propozitii.
    Determina tokens din sumar, tokens fara stop words si tokens lematized.
"""


def get_sentences(data_set):
    lemmatizer = WordNetLemmatizer()
    stop_words = load_stop_words()
    for subset in data_set:
        for article in subset["articles"]:
            lemmatized_text = []
            # Scot propozitiile din text
            article["sentences"] = sent_tokenize(article["text"])
            # Adaug spatiu dupa punct
            article["summary"] = re.sub(
                r'\.(?=[^ \W\d])', '. ', article["summary"])
            # Scot toate tipurile de token uri cerute in enunt
            article["summary_tokens"] = word_tokenize(article["summary"])
            article["summary_no_stopwords"] = [
                word for word in article["summary_tokens"] if not word in stop_words]
            for word in article["summary_no_stopwords"]:
                word = lemmatizer.lemmatize(word)
                lemmatized_text.append(word)
            article["summary_lematized"] = lemmatized_text
            # Scot propozitiile din summary
            article["summary_sentences"] = sent_tokenize(article["summary"])
    return data_set


"""
    Functie ce intoarce vocabularul obtinut, tinand cont de varianta aleasa.
"""


def get_vocabulary(training):
    sizes = {}
    vocabulary = {}
    used_words = []
    relevant_words = []
    for subset in training:
        used_words += ([word for sublist in subset["articles"]
                        for word in sublist[TYPE]])
        relevant_words += ([word for sublist in subset["articles"]
                            for word in sublist[SUMMARY_TYPE]])
    c = Counter(used_words)
    counter = dict(c)
    sizes["total"] = sum(c.values())

    for word in counter.keys():
        vocabulary[word] = {}
        vocabulary[word]["total"] = counter[word]

    c2 = Counter(relevant_words)
    counter2 = dict(c2)
    sizes["relevant"] = sum(c2.values())

    for word in counter2.keys():
        if word not in vocabulary:
            vocabulary[word] = {}
            vocabulary[word]["relevant"] = counter2[word]
            vocabulary[word]["total"] = counter2[word]
        else:
            vocabulary[word]["relevant"] = counter2[word]

    for word in vocabulary:
        if "relevant" not in vocabulary[word].keys():
            vocabulary[word]["relevant"] = 0
    return vocabulary, sizes


"""
    Functie ce intoarce probabilitatea unei propozitii de a fi relevanta sau
    irelevanta
"""


def get_likelihood(training):
    # calculez prob ca o prop sa fie relevanta/ irelevanta
    likelihood = {}
    total = 0
    relevant = 0
    for subset in training:
        for article in subset["articles"]:
            total += len(article["sentences"])
            relevant += len(article["summary_sentences"])
    likelihood["relevant"] = relevant / total
    likelihood["irelevant"] = (total - relevant) / total
    return likelihood


"""
    Functie ce intoarce probabilitatile fiecarui cuvant din vocabular de a 
    fi relevant sau irelevant
"""


def get_probabilities(vocabulary, sizes):
    probabilities = {}
    for word in vocabulary:
        probabilities[word] = {}
        probabilities[word]["relevant"] = (
            vocabulary[word]["relevant"] + alpha) / (sizes["relevant"] + alpha + sizes["total"])
        irelevant = vocabulary[word]["total"] - vocabulary[word]["relevant"]
        if irelevant < 0:
            irelevant = 0
        probabilities[word]["irelevant"] = (
            irelevant + alpha) / (sizes["total"] - sizes["relevant"] + alpha + sizes["total"])
    return probabilities


"""
    Functie in care este implementat modelul naive bayes si care incearca
    sa sumarizeze articolul pe baza formulelor date si a valorilor calculate.
"""


def test_model(testing, probabilities, likelihood):
    lemmatizer = WordNetLemmatizer()
    stop_words = load_stop_words()
    for subset in testing:
        for article in subset["articles"]:
            article["new_summary"] = ""
            cmap = {"relevant": 0, "irelevant": 0}
            # Calculez pt fiecare articol in parte
            for sentence in article["sentences"]:
                if SUMMARY_TYPE == "summary_tokens":
                    for word in word_tokenize(sentence):
                        if word in probabilities.keys():
                            cmap["relevant"] += log(probabilities[word]
                                                    ["relevant"])
                            cmap["irelevant"] += log(probabilities[word]
                                                     ["irelevant"])
                if SUMMARY_TYPE == "summary_no_stopwords":
                    words = [word for word in word_tokenize(
                        sentence) if not word in stop_words]
                    for word in words:
                        if word in probabilities.keys():
                            cmap["relevant"] += log(probabilities[word]
                                                    ["relevant"])
                            cmap["irelevant"] += log(probabilities[word]
                                                     ["irelevant"])
                if SUMMARY_TYPE == "summary_lematized":
                    words = [lemmatizer.lemmatize(word) for word in word_tokenize(
                        sentence) if not word in stop_words]
                    for word in words:
                        if word in probabilities.keys():
                            cmap["relevant"] += log(probabilities[word]
                                                    ["relevant"])
                            cmap["irelevant"] += log(probabilities[word]
                                                     ["irelevant"])
                cmap["relevant"] += log(likelihood["relevant"])
                cmap["irelevant"] += log(likelihood["irelevant"])
                if cmap["relevant"] > cmap["irelevant"]:
                    article["new_summary"] += sentence
    return testing


"""
    Functie ce parseaza valoarea intoarsa de rouge scorer.
"""


def get_values(values):
    values = values.split("=")
    precision = values[1].split(",")[0]
    recall = values[2].split(",")[0]
    return float(precision), float(recall)


"""
    Functie ce calculeaza valorea medie a preciziei si a recall ului folosind
    rouge scorer pentru unigrame.
"""


def get_rouge_scores_unigrams(results):
    avg_precision = 0.0
    avg_recall = 0.0
    entries = 0
    scorer = rouge_scorer.RougeScorer(['rouge1'])
    for subset in results:
        for article in subset["articles"]:
            score = scorer.score(article["summary"], article["new_summary"])
            values = str(score["rouge1"])
            precision, recall = get_values(values)
            avg_precision += precision
            avg_recall += recall
            entries += 1
    avg_precision = avg_precision / entries
    avg_recall = avg_recall / entries
    return avg_precision, avg_recall


"""
    Functie ce calculeaza valorea medie a preciziei si a recall ului folosind
    rouge scorer pentru bigrame.
"""


def get_rouge_scores_bigrams(results):
    avg_precision = 0.0
    avg_recall = 0.0
    entries = 0
    scorer = rouge_scorer.RougeScorer(['rouge2'])
    for subset in results:
        for article in subset["articles"]:
            score = scorer.score(article["summary"], article["new_summary"])
            values = str(score["rouge2"])
            precision, recall = get_values(values)
            avg_precision += precision
            avg_recall += recall
            entries += 1
    avg_precision = avg_precision / entries
    avg_recall = avg_recall / entries
    return avg_precision, avg_recall


"""
    Functie ce transforma o lista de unigrame in lista de bigrame.
"""


def bigrams(old_list):
    bigrams = [old_list[i] + ' ' + old_list[i+1]
               for i in range(len(old_list) - 1)]
    return bigrams


"""
    Functie ce transforma datele deja calculate din unigrame in bigrame.
"""


def transform_to_bigrams(data_set):
    for subset in data_set:
        for article in subset["articles"]:
            article["tokens"] = bigrams(article["tokens"])
            article["no_stopwords"] = bigrams(article["no_stopwords"])
            article["lematized"] = bigrams(article["lematized"])
            article["summary_tokens"] = bigrams(article["summary_tokens"])
            article["summary_no_stopwords"] = bigrams(
                article["summary_no_stopwords"])
            article["summary_lematized"] = bigrams(
                article["summary_lematized"])
    return data_set


"""
    Functie ce combina toti pasii necesari sumarizarii.
"""


def naive_bayes(articles):
    training, testing = split_articles(articles)
    training = get_sentences(training)
    testing = get_sentences(testing)

    if SUMMARY_MODE == "bigrams":
        training = transform_to_bigrams(training)
        testing = transform_to_bigrams(testing)

    vocabulary, sizes = get_vocabulary(training)
    likelihood = get_likelihood(training)
    probabilities = get_probabilities(vocabulary, sizes)
    results = test_model(testing, probabilities, likelihood)
    if SUMMARY_MODE == "unigrams":
        precision, recall = get_rouge_scores_unigrams(results)
        return precision, recall
    if SUMMARY_MODE == "bigrams":
        precision, recall = get_rouge_scores_bigrams(results)
        return precision, recall


"""
    Functie ce combina toti pasii necesari 5-fold cross validation
"""


def fold_summarization(articles):
    training, testing = split_fold(articles)
    precision_fold = []
    recall_fold = []
    for i in range(5):
        training[i] = get_sentences(training[i])
        testing[i] = get_sentences(testing[i])
        vocabulary, sizes = get_vocabulary(training[i])
        likelihood = get_likelihood(training[i])
        probabilities = get_probabilities(vocabulary, sizes)
        results = test_model(testing[i], probabilities, likelihood)
        precision, recall = get_rouge_scores_unigrams(results)
        precision_fold.append(precision)
        recall_fold.append(recall)

    return precision_fold, recall_fold
