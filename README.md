# github-open-issues

#### **About App**: This is a containerized flask app which will take any public git repo URL and will show distribution of different issues applying several condition.

#### **Endpoint of App**: http://104.197.43.20:8080/
#### **Docker Image**: gcr.io/greendeck-project/github-testing:latest

Input-page: 
![#](screenshot_images/g_input.png "welcome page")

Output-page: 
![#](screenshot_images/g_output.png "result page")

## Folder Structure:
parent-folder
└── app
|    └── dustbin (# for personal use #debugging & testing)
|    └── static
|           └── get_git_query_result.py (# function to perform git query and return resuls)
|           └── get_token_distribution.py (# function to return frequency distribution of words in request)
|
|    └── templates
|            └──welcome.html (# html page for frontend)
|
|    └── app.py (# flask app #starting)
|    └── config.py (# gunicorn config)
|    └── requirements.txt (# required packages)
|    └── uwsgi.ini (# initialization of uwsgi # ini service file)
|
|
└── screenshot-images (# contains screenshot images)
└── Dockerfile (# dockerfile to build a docker app)
└── kubernetes-config.yml (# kubernetes config file)
└── Readme.md
