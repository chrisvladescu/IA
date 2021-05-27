import random
from collections import Counter
from constants import CATEGORIES
from constants import alpha
from constants import TYPE
from math import log
from functions import split_articles
from functions import split_fold

"""
    Functie ce intoarce vocabularul obtinut, tinand cont de varianta aleasa.
"""


def get_vocabulary(training):
    size = 0
    sizes = {}
    vocabulary = {}
    for subset in training:
        used_words = [word for sublist in subset["articles"]
                      for word in sublist[TYPE]]
        c = Counter(used_words)
        counter = dict(c)
        sizes[subset["category"]] = sum(c.values())
        size += sum(c.values())
        for word in counter.keys():
            if word in vocabulary:
                vocabulary[word][subset["category"]] = counter[word]
            else:
                vocabulary[word] = {}
                vocabulary[word][subset["category"]] = counter[word]
    sizes["total"] = size
    sizes["vocabulary"] = get_unique_words(training)
    return vocabulary, sizes


"""
    Functie ce intoarce numarul unic de cuvinte dintr-o listă de articole.
"""


def get_unique_words(training):
    used_words = []
    for subset in training:
        used_words += [word for sublist in subset["articles"]
                       for word in sublist[TYPE]]
    used_words = list(set(used_words))
    return len(used_words)


"""
    Functie ce intoarce probabilitatile fiecarui cuvant din vocabular de a 
    apartine uneia dintre cele 5 categorii.
"""


def get_probabilities(vocabulary, sizes):
    probabilities = {}
    for word in vocabulary:
        probabilities[word] = {}
        for category in CATEGORIES:
            count_appereances = 0
            if category in vocabulary[word].keys():
                probabilities[word][category] = (vocabulary[word][category] + alpha) / \
                    (sizes[category] + alpha + sizes["total"])
                count_appereances += vocabulary[word][category]
            else:
                probabilities[word][category] = alpha / \
                    (sizes[category] + alpha + sizes["total"])
    return probabilities


"""
    Functie ce intoarce probabilitatea unui articol de a apartine uneia dintre
    cele 5 categorii.
"""


def get_likelihood(training):
    likelihood = {}
    total = 0
    for subset in training:
        total += len(subset["articles"])

    for subset in training:
        likelihood[subset["category"]] = len(subset["articles"]) / total

    return likelihood


"""
    Functie in care este implementat modelul naive bayes si care incearca
    sa clasifice articolul pe baza formulelor date si a valorilor calculate.
"""


def test_model(testing, probabilities, likelihood):
    results = {}
    articles_number = {}

    for category in CATEGORIES:
        results[category] = {}
        results[category]["ok"] = 0
        results[category]["wrong"] = {}
        for category2 in CATEGORIES:
            results[category]["wrong"][category2] = 0
        articles_number[category] = 0

    for subset in testing:
        articles_number[subset["category"]] = len(subset["articles"])
        for article in subset["articles"]:
            cmap = {}
            max_cmap = -99999999999999999999
            chosen_category = ""
            for category in CATEGORIES:
                cmap[category] = 0
            for word in article[TYPE]:
                for category in CATEGORIES:
                    if word in probabilities.keys():
                        cmap[category] += log(probabilities[word][category])
                    else:
                        cmap[category] += 0

            for category in CATEGORIES:
                cmap[category] += log(likelihood[category])
                if cmap[category] > max_cmap:
                    max_cmap = cmap[category]
                    chosen_category = category

            if chosen_category == subset["category"]:
                results[chosen_category]["ok"] += 1
            else:
                results[subset["category"]]["wrong"][chosen_category] += 1
    return results, articles_number


"""
    Functie ce calculeaza valoarea preciziei si a recall ului.
"""


def get_test_results(results, articles_number):
    all_articles = 0
    all_correct = 0
    recall = {}
    for category in CATEGORIES:
        all_articles += articles_number[category]
        all_correct += results[category]["ok"]
        recall[category] = results[category]["ok"] / articles_number[category]

    precision = all_correct / all_articles
    return precision, recall


"""
    Functie ce combina toti pasii necesari clasificarii.
"""


def naive_bayes(articles):
    training, testing = split_articles(articles)
    vocabulary, sizes = get_vocabulary(training)
    likelihood = get_likelihood(training)
    probabilities = get_probabilities(vocabulary, sizes)
    results, articles_number = test_model(testing, probabilities, likelihood)
    precision, recall = get_test_results(results, articles_number)
    return precision, recall


"""
    Functie ce combina toti pasii necesari 5-fold cross validation
"""


def fold_classification(articles):
    training, testing = split_fold(articles)
    precision_fold = []
    recall_fold = []
    for i in range(5):
        vocabulary, sizes = get_vocabulary(training[i])
        likelihood = get_likelihood(training[i])
        probabilities = get_probabilities(vocabulary, sizes)
        results, articles_number = test_model(
            testing[i], probabilities, likelihood)
        precision, recall = get_test_results(results, articles_number)
        precision_fold.append(precision)
        recall_fold.append(recall)
    return precision_fold, recall_fold
