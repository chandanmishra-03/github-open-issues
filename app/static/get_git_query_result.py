from github import Github
from datetime import datetime
import itertools
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

global temp_results
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

querystring = {"filter": "all", "access_token": "fa6c840106c750f0f636b75069944d16dd1c1cc9"}
payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
}

# github auth key
g = Github("IIITian-Chandan", "bapunu123")  # I have hidden it for security issues


def multi_request(url_page):


    # querystring["page"] = page_no
    response = requests.request("GET", url_page, data=payload, headers=headers, params=querystring)
    temp_results.append(json.loads(response.text))


def calculate(item):
    try:
        if "pull_request" not in item.keys():
            total_issues.append(item)

            total_issues_titles.append(item["title"].lower())

            created_time = datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

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
        pass


def clear_buffer():
    del temp_results[:]
    del total_issues[:]
    del open_issues_24[:]
    del open_issues_24_to_7[:]
    del open_issues_more_than_7[:]
    del total_issues_titles[:]


def get_git_issues_count(repo_name):
    start_time = datetime.now().timestamp()
    url = "https://api.github.com/repos/" + repo_name + "/issues"
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    results = json.loads(response.text)

    try:
        if 'link' in response.headers:
            pages_url = []
            pages = {i[6:-1]: j[j.index('<') + 1:-1] for j, i in
                     (link.split(';') for link in
                      response.headers['link'].split(','))}
        maximum_number = int(response.headers["link"].split("page=")[-1].split(">")[0])
        t_url = "=".join(pages["last"].split("=")[:-1]) + "="
        page_numbers = [t_url + str(i + 2) for i in range(maximum_number)]
        thread = min(int(len(page_numbers) / 2) + 1, 30)
        for batch in range(0, len(page_numbers), 30 * 10):
            pool = ThreadPool(thread)
            items = (json.loads(response.text))[batch:batch + (30 * 10)]
            p_results = pool.map(multi_request, page_numbers)

            pool.close()
            pool.join()

        results = list(itertools.chain.from_iterable(temp_results)) + results

    except:
        pass

    for batch in range(0, len(results), 20 * 10):
        pool = ThreadPool(10)
        items = results[batch:batch + (10 * 20)]
        results1 = pool.map(calculate, items)
        pool.close()
        pool.join()

    no_total_issues = len(total_issues)
    no_open_issues_24 = len(open_issues_24)
    no_open_issues_24_to_7 = len(open_issues_24_to_7)
    no_open_issues_more_than_7 = no_total_issues - (no_open_issues_24 + no_open_issues_24_to_7)

    output_1, output_2, output_3, output_4, output_5 = total_issues_titles.copy(), no_total_issues, no_open_issues_24, no_open_issues_24_to_7, no_open_issues_more_than_7
    # url = "https://api.github.com/repos/moby/moby/issues"
    # # querystring = {"state": "open"}
    # # payload = ""
    # # headers = {
    # #     'cache-control': "no-cache",
    # #     'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
    # # }
    # #
    # # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    # #
    # # print(response.text)
    #
    # repo = g.get_repo(repo_name)
    # total_pull_number = [i.number for i in repo.get_pulls('all')]
    # total_issues = [i for i in repo.get_issues(state='open') if
    #                 i.number not in total_pull_number]  # getting all open issues and converting into list
    # no_total_issues = len(total_issues)
    # print(no_total_issues)
    #
    # open_issues_24 = [i for i in repo.get_issues(state='open',
    #                                              since=datetime.fromtimestamp(
    #                                                  datetime.now().timestamp() - (24 * 60 * 60))) if
    #                   i.number not in total_pull_number]
    # # getting list of open issues in last 24 hrs timestamp will convert time into seconds so that if we will do
    # # subtraction of 24 hrs in secs we will get exact time of 24hrs back
    #
    # no_open_issues_24 = len(open_issues_24)
    #
    # open_issues_24_to_7 = [i for i in repo.get_issues(state='open',
    #                                                   since=datetime.fromtimestamp(
    #                                                       datetime.now().timestamp() - (7 * 24 * 60 * 60)))[
    #                                   no_open_issues_24:] if i.number not in total_pull_number]
    # # issues in between last 7 days to 24 hrs
    #
    # no_open_issues_24_to_7 = len(open_issues_24_to_7)
    #
    # no_open_issues_more_than_7 = no_total_issues - (no_open_issues_24 + no_open_issues_24_to_7)

    # here we are also returning all total issues that will help us to extract word frequency distribution
    end_time = datetime.now().timestamp()
    duration = str(end_time-start_time)
    clear_buffer()
    return output_1, output_2, output_3, output_4, output_5,duration
