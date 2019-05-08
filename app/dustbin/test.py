from github import Github
from datetime import datetime
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# nltk.download('stopwords')

# from nltk import FreqDist

text = "This is your custom text . You can replace it with anything you want . Feel free to modify it and test ."

text_list = text.split(" ")

g = Github("IIITian-Chandan", "bapunu123")
repo = g.get_repo("spotify/annoy")
total_pull_number = [i.number for i in repo.get_pulls('all')]
total_issues = [i for i in repo.get_issues(state='open') if i.number not in total_pull_number]

for i in total_issues:
    print(i)
no_total_issues = len(total_issues)

open_issues_24 = [i for i in repo.get_issues(state='open',
                                             since=datetime.fromtimestamp(datetime.now().timestamp() - (24 * 60 * 60))) if i.number not in total_pull_number]
no_open_issues_24 = len(open_issues_24)

open_issues_24_to_7 = [i for i in repo.get_issues(state='open',
                                                  since=datetime.fromtimestamp(
                                                      datetime.now().timestamp() - (7 * 24 * 60 * 60)))[
                                  no_open_issues_24:]if i.number not in total_pull_number]
no_open_issues_24_to_7 = len(open_issues_24_to_7)

no_open_issues_more_than_7 = no_total_issues - (no_open_issues_24 + no_open_issues_24_to_7)

print(no_total_issues)
print(no_open_issues_24)
print(no_open_issues_24_to_7)
print(no_open_issues_more_than_7)
#
# total_issues_titles = ' . '.join([i.title for i in total_issues])
# stop_words = set(stopwords.words('english'))
# from nltk.tokenize import RegexpTokenizer
#
# tokenizer = RegexpTokenizer(r'\w+')
#
# word_tokens = tokenizer.tokenize(total_issues_titles)
#
# filtered_sentence = [w for w in word_tokens if not w in stop_words]
#
# temp = [['word', 'count', 'area']]
# freqDist = FreqDist(filtered_sentence)
# for i, j in freqDist.items():
#     temp.append([i, j, j])
# print(temp)
#
# # import datetime
#
# # print(datetime.now().timestamp())
# # print(datetime.fromtimestamp(datetime.now().timestamp()-(24*60*60)))
# # print(datetime.fromordinal(datetime.now()))
