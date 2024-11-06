import os
import sys
import numpy as np
import pandas as pd
import time
import praw
from praw import Reddit

from utils.constants import POST_FIELDS


# Defining Reddit Instance Below
def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent)
        print("connected to reddit!")
        print(reddit)
        return reddit
    except Exception as e:
        print(f'Failed to connect to Reddit: {e}')
        sys.exit(1)


#Defining how to extract posts from subreddit
def extract_posts(reddit_instance: Reddit, subreddit: str, limit=None, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Extracting posts from {subreddit}, attempt {attempt + 1}")
            subreddit = reddit_instance.subreddit(subreddit)
            posts = subreddit.top(limit=limit)
            # print(posts)
            post_lists = []
            for post in posts:
                post_data = {field: getattr(post, field, None) for field in POST_FIELDS}
                post_lists.append(post_data)
                print(f"Posts extracted: {len(post_lists)}")
            return post_lists
        except praw.exceptions.PRAWException as e:
            print(f"Error extracting posts: {e}")
            attempt += 1
            time.sleep(delay)
    print("Failed to extract posts after several attempts.")
    return None

#transforming Data
def data_transformation(post_df: pd.DataFrame):
    post_df['id'] = post_df['id'].astype(str)
    post_df['title'] = post_df['title'].astype(str)
    post_df['score'] = post_df['score'].fillna(0).astype(int)
    post_df['upvote_ratio'] = post_df['upvote_ratio'].fillna(0).astype(float)
    post_df['num_comments'] = post_df['num_comments'].fillna(0).astype(int)
    post_df['author'] = post_df['author'].astype(str)
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['url'] = post_df['url'].astype(str)
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)

    #Handling data in edited columns which contains either none or Boolean value
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)

    return post_df

def load_data_to_csv(data: pd.DataFrame, path: str):
    # Check if the directory exists, if not, create it
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the data to the specified path
    data.to_csv(path, index=False)