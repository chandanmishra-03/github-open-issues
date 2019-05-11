from flask import Flask, render_template, request
from static.get_token_distribution import *
from flask_cors import CORS
import config
import json

app = Flask(__name__)
CORS(app)


# route to check application is live or not. Kind of health checking
@app.route('/_ah/health')
def default():
    return 'this is auto deploy, try  after 22'


# loading start page with hiding table and graphs.
@app.route("/")
def index():
    return render_template('welcome.html', table_visiblity="hidden", graph_visibility="hidden")


# after post request from user this is going to perform backend task
# This route is responsible for getting all query results from github apis and gathering required data for plots
@app.route("/git_query", methods=['POST', 'GET'])
def git_query():
    from static.get_git_query_result import get_git_issues_count
    if request.method == 'POST':
        git_repo_url = request.form['git_repo']

        temp_repo_name = '/'.join(
            git_repo_url.split('github.com/')[1].split('/')[0:2])  # extracting github userid/projectname
        total_issues, no_total_issues, no_open_issues_24, no_open_issues_24_to_7, no_open_issues_more_than_7, duration = get_git_issues_count(
            temp_repo_name)
        # get_git_issues_count function will call the github api with different filters to get counts of open issues
        # on different conditions.

        total_issues_token_distribution = token_distribution(total_issues)
        # token_distribution function will let you know the occurence of keywords in the list of error texts

        data_from_server = [no_total_issues, no_open_issues_24, no_open_issues_24_to_7, no_open_issues_more_than_7]
        # converting all counts to a list so that it can easily accessible by js for count distribution plotting

        # one failure step
        #     {
        #     "plot_data": [['open issues interval', 'no of issues'], ["no_total_issues", no_total_issues],
        #                   ["no_open_issues_24", no_open_issues_24],
        #                   ["no_open_issues_24_to_7", no_open_issues_24_to_7],
        #                   ["no_open_issues_more_than_7", no_open_issues_more_than_7]]}
        # data_from_server = json.dumps(data_from_server)

        return render_template('welcome.html', git_repo_url=git_repo_url, no_total_issues=no_total_issues,
                               no_open_issues_24=no_open_issues_24, no_open_issues_24_to_7=no_open_issues_24_to_7,
                               no_open_issues_more_than_7=no_open_issues_more_than_7, data_from_server=data_from_server,
                               total_issues_token_distribution=json.dumps(total_issues_token_distribution),
                               table_visiblity="visible", graph_visibility="visible", duration=duration)

    else:
        return render_template('welcome.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=config.DEBUG_MODE)
