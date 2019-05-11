from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk

nltk.download('stopwords')


# we have list of sentences. need to clean using nltk
# we will remove stopwords and punctuation marks

def token_distribution(total_issues):
    # each item in total_issues is a class item. by item.key we can access the particular key value
    # here I am extracting only titles of all issues & joining them as a single sentences
    total_issues_titles = ' . '.join(total_issues)
    # dictionary of english stopwords
    stop_words = set(stopwords.words('english'))
    # removing punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = tokenizer.tokenize(total_issues_titles)
    # filtering words those are not in stopwords
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    # I have fixed these 3 values as column headers why 3 values? when we have 2 dimension data ans: as here I am
    # using google plotting for bubble plot its better to assign 2 integer dimensions for a good visualization than
    # only it will able to plot circles in 2 dim
    #here count = area
    temp = [['word', 'count', 'area']]
    frequencyDist = FreqDist(filtered_sentence)
    for i, j in frequencyDist.items():
        temp.append([i, j, j])
    return temp
