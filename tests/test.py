import pandas as pd

from etls.reddit_etl import connect_reddit, extract_posts, data_transformation, load_data_to_csv
from etls.aws_etl import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import CLIENT_ID, SECRET, USER_AGENT,AWS_BUCKET_NAME, AWS_REGION


def reddit_pipeline(subreddit: str, limit=10):

    # connecting to reddit instance

    instance = connect_reddit(CLIENT_ID, SECRET, USER_AGENT)

    # extraction
    posts = extract_posts(instance, subreddit ="Python", limit = 10)
    print(posts)
    post_df = pd.DataFrame(posts)
    # print(post_df)
    post_df = data_transformation(post_df)

    file_path = f'/Reddittttttt_12345.csv'
    print(file_path)
    load_data_to_csv(post_df, file_path)

def s3_pipeline():
    s3 = connect_to_s3()

    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME, AWS_REGION)

    file_path = f'/Reddittttttt_12345.csv'
    print(file_path.split('/')[-1])
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, file_path.split('/')[-1])


if __name__ == "__main__":
    reddit_pipeline(subreddit ='Python', limit=10)
    s3_pipeline()
