import random
from constants import CATEGORIES

"""
    Functia imparte setul de date in setul de antrenare si setul de testare,
    in procentul dorit in enunt.
"""


def split_articles(articles):
    training = []
    testing = []

    for subset in articles:
        size = len(subset["articles"])
        testing_size = int(size * 0.25)
        random.shuffle(subset["articles"])

        testing_articles = subset["articles"][:testing_size]
        testing.append({"category": subset["category"],
                        "articles": testing_articles})

        training_articles = subset["articles"][testing_size:]
        training.append({"category": subset["category"],
                         "articles": training_articles})
    return training, testing


"""
    Helper pentru 5-fold cross validation
"""


def add_training(set_1, set_2, set_3, set_4):
    final_set = []
    final_set += set_1
    final_set += set_2
    final_set += set_3
    final_set += set_4
    return final_set


"""
    Functia imparte setul de date in modul cerut de 5-fold cross validation
"""


def split_fold(articles):
    training_split = []
    testing_split = []

    training_1 = []
    training_2 = []
    training_3 = []
    training_4 = []
    training_5 = []

    testing_1 = []
    testing_2 = []
    testing_3 = []
    testing_4 = []
    testing_5 = []

    for subset in articles:

        size = len(subset["articles"])
        testing_size = int(size * 0.2)
        random.shuffle(subset["articles"])
        margin_1 = testing_size
        margin_2 = testing_size * 2
        testing_1_s = subset["articles"][:margin_1]
        testing_2_s = subset["articles"][margin_1:margin_2]
        margin_1 = testing_size * 2
        margin_2 = testing_size * 3
        testing_3_s = subset["articles"][margin_1:margin_2]
        margin_1 = testing_size * 3
        margin_2 = testing_size * 4
        testing_4_s = subset["articles"][margin_1:margin_2]
        testing_5_s = subset["articles"][margin_2:]

        training_1_s = add_training(
            testing_2_s, testing_3_s, testing_4_s, testing_5_s)
        training_2_s = add_training(
            testing_1_s, testing_3_s, testing_4_s, testing_5_s)
        training_3_s = add_training(
            testing_1_s, testing_2_s, testing_4_s, testing_5_s)
        training_4_s = add_training(
            testing_1_s, testing_2_s, testing_3_s, testing_5_s)
        training_5_s = add_training(
            testing_1_s, testing_2_s, testing_3_s, testing_4_s)

        testing_1.append(
            {"category": subset["category"], "articles": testing_1_s})
        testing_2.append(
            {"category": subset["category"], "articles": testing_2_s})
        testing_3.append(
            {"category": subset["category"], "articles": testing_3_s})
        testing_4.append(
            {"category": subset["category"], "articles": testing_4_s})
        testing_5.append(
            {"category": subset["category"], "articles": testing_5_s})

        training_1.append(
            {"category": subset["category"], "articles": training_1_s})
        training_2.append(
            {"category": subset["category"], "articles": training_2_s})
        training_3.append(
            {"category": subset["category"], "articles": training_3_s})
        training_4.append(
            {"category": subset["category"], "articles": training_4_s})
        training_5.append(
            {"category": subset["category"], "articles": training_5_s})

    training_split = [training_1, training_2,
                      training_3, training_4, training_5]
    testing_split = [testing_1, testing_2, testing_3, testing_4, testing_5]

    return training_split, testing_split


"""
    Functii de afisaj pentru rezultatele finale
"""


def print_classification(precision, recall):
    print("Precision: " + str(precision))
    print("Recall: ")
    for category in CATEGORIES:
        print("For " + category + ": " + str(recall[category]))


def print_summarization(precision, recall):
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))


def print_fold_c(precision, recall):
    count = 1
    for p in precision:
        print("Precision for set " + str(count) + " :" + str(p))
        count += 1
    count = 1
    for r in recall:
        print("Recall for set " + str(count) + " :")
        for category in CATEGORIES:
            print("For " + category + ": " + str(r[category]))
        count += 1


def print_fold_s(precision, recall):
    count = 1
    for p in precision:
        print("Precision for set " + str(count) + " :" + str(p))
        count += 1
    count = 1
    for r in recall:
        print("Recall for set " + str(count) + " :" + str(r))
        count += 1
