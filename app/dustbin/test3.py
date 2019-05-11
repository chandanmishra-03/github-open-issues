# import requests
# import concurrent.futures
# import json
#
# url = "https://api.github.com/repos/moby/moby/issues"
# querystring = {"filter": "all", "per_page": 30, "access_token": "fa6c840106c750f0f636b75069944d16dd1c1cc9"}
# payload = ""
# headers = {
#     'cache-control': "no-cache",
#     'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
# }
#
# response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
# results = json.loads(response.text)
#
#
# def load_url(page_no):
#     querystring["page"] = page_no
#     response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
#     return response
#
# try:
#     maximum_number = int(response.headers["link"].split("page=")[-1].split(">")[0])
#     page_numbers = [i + 2 for i in range(maximum_number - 1)]
#     print("++++++++++++++++++++++")
#     print(page_numbers)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
#         future_to_url = {executor.submit(load_url, url): url for url in page_numbers}
#         for future in concurrent.futures.as_completed(future_to_url):
#             url = future_to_url[future]
#             try:
#                 data = future.result()
#                 print(len(json.loads(data.text)))
#             except Exception as exc:
#                 raise
#                 resp_err = resp_err + 1
#             else:
#                 resp_ok = resp_ok + 1
# except:raise
#
#
#
#
try:
    # for python3
    import queue
    from urllib.request import urlopen
except:
    # for python2
    import Queue as queue
    from urllib2 import urlopen

import threading
import requests
import json
# worker_data = [2, 3, 4, 5]
url = "https://api.github.com/repos/moby/moby/issues"
querystring = {"filter": "all", "per_page": 30, "access_token": "fa6c840106c750f0f636b75069944d16dd1c1cc9"}
payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
results = json.loads(response.text)
maximum_number = int(response.headers["link"].split("page=")[-1].split(">")[0])
page_numbers = [i + 2 for i in range(maximum_number - 1)][0:10]
# load up a queue with your data, this will handle locking
q = queue.Queue()
for url in page_numbers:
    q.put(url)
temp = [len(results)]


# define a worker function
def worker(url_queue):
    queue_full = True
    while queue_full:
        try:
            url = "https://api.github.com/repos/moby/moby/issues"
            querystring = {"filter": "all", "per_page": 30, "access_token": "fa6c840106c750f0f636b75069944d16dd1c1cc9"}
            payload = ""
            headers = {
                'cache-control': "no-cache",
                'Postman-Token': "3b82e2ee-fe4f-4c57-8ea7-901de83c62f3"
            }
            # get your data off the queue, and do some work
            querystring["page"] = url_queue.get(False)

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            temp.append(len(json.loads(response.text)))
            print(len(json.loads(response.text)))

        except queue.Empty:
            queue_full = False


# create as many threads as you want
thread_count = 15
for i in range(thread_count):
    t = threading.Thread(target=worker, args=(q,))
    t.start()
print(temp)



