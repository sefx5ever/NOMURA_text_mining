# import praw # 由於筆數限制最多1千筆
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time
import requests

# Create the columns name
reddit_save_column = ['date','score','title','content','comment']

# Customize setting
KEY_WORD = 'fund' # Searching keyword
LIMITATION = 10000 # Number of data to save
START_DATE = '2020-01-01' #FIX FORMAT YYYY-MM-DD (2020-01-02)
CURRENT_DATE = str(dt.date.today()) # To name csv follow by date

# Create a space for data collection
data_collection = []

# PushshiftAPI for submission and comments
reddit_api_submission = 'https://api.pushshift.io/reddit/search/submission/?limit={}&q={}&after={}'.format(str(LIMITATION),str(KEY_WORD),str(START_DATE))
reddit_api_comment = 'https://api.pushshift.io/reddit/search/comment/?limit={}&link_id={}&fields=body'

# To request data from API
res_data_title = requests.get(reddit_api_submission)
res_title = res_data_title.json()['data']

# To collect forum's title and comment
for each_res in res_title:
    # date = str(pd.to_datetime(each_res['retrieved_on'])).split(' ')[0]
    date = time.strftime("%Y-%m-%d",time.gmtime(each_res['retrieved_on']))
    print(date)
    score = each_res['score']
    title = each_res['title']
    self_text = each_res['selftext']
    link_id = each_res['id']
    num_comment = each_res['num_comments']
    comments = ""
    if num_comment > 0: # Collect comments if exist
        res_data_comment = requests.get(reddit_api_comment.format(num_comment,link_id))
        res_comment = res_data_comment.json()['data']
        for comment in res_comment:
            comments = comments + "{}".format(comment['body'] + '\n ')
    data_collection.append([date,score,title,self_text,comments]) # Append data to created dataframe

# Create a dataframe with data collection
df = pd.DataFrame(data_collection,columns = reddit_save_column)

# Export dataframe to csv
df.to_csv('reddit_fund_with_comments_' + CURRENT_DATE + '.csv')



# Start scraping with condition
# res_data_title = list(api.search_submissions(after = start_epoch,subreddit = KEY_WORD, \
#                                         filter = ['author', 'title', 'subreddit' ,'score', 'selftext'],limit = LIMITATION))

# res_data_comment = list(api.search_comments(after = start_epoch,subreddit = KEY_WORD, \
#                                         filter = ['author', 'title', 'subreddit' ,'score', 'selftext'],limit = LIMITATION))


#FIX
# subreddit = reddit.subreddit('{}'.format(KEY_WORD))
# raw_data = subreddit.hot(limit = LIMITATION)


# for submission in raw_data:
#     comments = submission.comments.list()
#     for comment in comments:
#         print(20 * '-')
#         print(comment.body)
#         print(20 * '-')
#         if len(comment.replies) > 0:
#             for reply in comment.replies:
#                 print(20 * '=')
#                 print(reply.body)
#                 print(20 * '=')
#     # if submission.stickied:
#     #     print(submission.author,submission.score,submission.title,submission.selftext)

