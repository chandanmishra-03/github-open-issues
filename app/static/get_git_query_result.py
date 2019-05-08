from github import Github
from datetime import datetime

# github auth key
g = Github("IIITian-Chandan", "bapunu123")  # I have hidden it for security issues


def get_git_issues_count(repo_name):
    repo = g.get_repo(repo_name)
    total_pull_number = [i.number for i in repo.get_pulls('all')]
    total_issues = [i for i in repo.get_issues(state='open') if
                    i.number not in total_pull_number]  # getting all open issues and converting into list
    no_total_issues = len(total_issues)

    open_issues_24 = [i for i in repo.get_issues(state='open',
                                                 since=datetime.fromtimestamp(
                                                     datetime.now().timestamp() - (24 * 60 * 60))) if
                      i.number not in total_pull_number]
    # getting list of open issues in last 24 hrs timestamp will convert time into seconds so that if we will do
    # subtraction of 24 hrs in secs we will get exact time of 24hrs back

    no_open_issues_24 = len(open_issues_24)

    open_issues_24_to_7 = [i for i in repo.get_issues(state='open',
                                                      since=datetime.fromtimestamp(
                                                          datetime.now().timestamp() - (7 * 24 * 60 * 60)))[
                                      no_open_issues_24:] if i.number not in total_pull_number]
    # issues in between last 7 days to 24 hrs

    no_open_issues_24_to_7 = len(open_issues_24_to_7)

    no_open_issues_more_than_7 = no_total_issues - (no_open_issues_24 + no_open_issues_24_to_7)

    # here we are also returning all total issues that will help us to extract word frequency distribution
    return total_issues, no_total_issues, no_open_issues_24, no_open_issues_24_to_7, no_open_issues_more_than_7
