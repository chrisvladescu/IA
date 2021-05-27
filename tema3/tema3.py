from setup import load_setup
from naive_bayes_classification import naive_bayes as classification
from naive_bayes_classification import fold_classification
from naive_bayes_summarization import naive_bayes as summarization
from naive_bayes_summarization import fold_summarization
from articles import articles
from functions import print_classification, print_summarization, print_fold_c, print_fold_s

if __name__ == "__main__":
    """ Am comentat linia ce contine "load_setup" deoarece am incarcat deja 
    articolele in articles.py intr-o rulare anterioara.
        Pentru reincarcarea setului, se decomenteaza linia si se comenteaza / 
    sterge importul "from articles import articles"
        Pentru alegerea actiunii, se decomentează din optiunile de mai jos.
        Pentru alegerea tipului (tokens, tokens fara stop words, lematized),
    se alege din constants varianta dorita.
    """
    # articles = load_setup()

    # Classification
    precision, recall = classification(articles)
    print_classification(precision, recall)

    # Summarization
    # precision, recall = summarization(articles)
    # print_summarization(precision, recall)

    # 5 fold classification
    # precision, recall = fold_classification(articles)
    # print_fold_c(precision, recall)

    # 5 fold summarization
    # precision, recall = fold_summarization(articles)
    # print_fold_s(precision, recall)
