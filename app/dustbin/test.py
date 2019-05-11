from github import Github
from datetime import datetime
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import dateutil.parser
import itertools
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool
from datetime import date

# nltk.download('stopwords')

# from nltk import FreqDist

text = "This is your custom text . You can replace it with anything you want . Feel free to modify it and test ."

text_list = text.split(" ")

# url = "https://api.github.com/repos/moby/moby/issues"
url = "https://api.github.com/repos/moby/moby/issues"
querystring = {"filter": "all", "access_token": "fa6c840106c750f0f636b75069944d16dd1c1cc9"}
payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(len(json.loads(response.text)))
results = json.loads(response.text)

temp_results = []
no_total_issues = 0
no_open_issues_24 = 0
no_open_issues_24_to_7 = 0
no_open_issues_more_than_7 = 0
total_issues = []
open_issues_24 = []
open_issues_24_to_7 = []
open_issues_more_than_7 = []
total_issues_titles = []

def multi_request(url_page):
    # querystring["page"] = page_no
    response = requests.request("GET", url_page, data=payload, headers=headers, params=querystring)
    temp_results.append(json.loads(response.text))


def calculate(item):
    try:
        if "pull_request" not in item.keys():
            total_issues.append(item)
            t_no.append(item["number"])
            total_issues_titles.append(item["title"].lower())

            created_time = datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            print(datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ"))

            print(datetime.fromtimestamp(datetime.utcnow().timestamp() - (24 * 60 * 60)))

            print("||")
            # print(datetime.fromtimestamp(datetime.utcnow().timestamp() - (24 * 60 * 60)))

            if created_time >= datetime.fromtimestamp(datetime.utcnow().timestamp() - (24 * 60 * 60)):
                open_issues_24.append(item)
            elif datetime.fromtimestamp(
                    datetime.now().timestamp() - (
                            7 * 24 * 60 * 60)) <= created_time < datetime.fromtimestamp(
                datetime.now().timestamp() - (24 * 60 * 60)):
                open_issues_24_to_7.append(item)
            else:
                open_issues_more_than_7.append(item)




    except:
        raise


try:
    if 'link' in response.headers:
        pages_url = []
        pages = {i[6:-1]: j[j.index('<') + 1:-1] for j, i in
                 (link.split(';') for link in
                  response.headers['link'].split(','))}
    print(response.headers["link"])
    maximum_number = int(response.headers["link"].split("page=")[-1].split(">")[0])
    t_url = "=".join(pages["last"].split("=")[:-1]) + "="
    page_numbers = [t_url + str(i + 2) for i in range(maximum_number)]
    thread = min(int(len(page_numbers) / 2) + 1, 20)
    for batch in range(0, len(page_numbers), thread * 20):
        pool = ThreadPool(thread)
        items = (json.loads(response.text))[batch:batch + (thread * 20)]
        p_results = pool.map(multi_request, page_numbers)

        pool.close()
        pool.join()
    print(len(temp_results))
    results = list(itertools.chain.from_iterable(temp_results)) + results

except:
    pass

# print(results)


print("=================")

# print(json.loads(response.text))
print(type(json.loads(response.text)))
print()



t_no = []

for batch in range(0, len(results), 20 * 10):
    pool = ThreadPool(10)
    items = results[batch:batch + (10 * 20)]
    results1 = pool.map(calculate, items)
    pool.close()
    pool.join()

print("======================================")
print(len(open_issues_24))
print(len(total_issues))
print(len(results))
print(len(open_issues_24_to_7))
print(len(open_issues_more_than_7))
print(len(total_issues_titles))
print(len(set(t_no)))
# g = Github("IIITian-Chandan", "bapunu123")
# repo = g.get_repo("moby/moby")
# total_pull_number = [i.number for i in repo.get_pulls('all')]
# total_issues = [i for i in repo.get_issues(state='open') if i.number not in total_pull_number]
#
# for i in total_issues:
#     print(i)
# no_total_issues = len(total_issues)
#
# open_issues_24 = [i for i in repo.get_issues(state='open',
#                                              since=datetime.fromtimestamp(datetime.now().timestamp() - (24 * 60 * 60))) if i.number not in total_pull_number]
# no_open_issues_24 = len(open_issues_24)
#
# open_issues_24_to_7 = [i for i in repo.get_issues(state='open',
#                                                   since=datetime.fromtimestamp(
#                                                       datetime.now().timestamp() - (7 * 24 * 60 * 60)))[
#                                   no_open_issues_24:]if i.number not in total_pull_number]
# no_open_issues_24_to_7 = len(open_issues_24_to_7)
#
# no_open_issues_more_than_7 = no_total_issues - (no_open_issues_24 + no_open_issues_24_to_7)
#
# print(no_total_issues)
# print(no_open_issues_24)
# print(no_open_issues_24_to_7)
# print(no_open_issues_more_than_7)
# #
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
