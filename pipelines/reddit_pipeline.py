# Import necessary modules and functions for the Reddit data pipeline
import sys
from _datetime import datetime  # for working with dates and timestamps
import pandas as pd  # for handling data in DataFrame format
from etls.reddit_etl import connect_reddit, extract_posts, data_transformation, load_data_to_csv
from utils.constants import CLIENT_ID, SECRET, USER_AGENT, OUTPUT_PATH

# Define the main Reddit data pipeline function
def reddit_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):

    # Connect to Reddit instance using credentials
    instance = connect_reddit(CLIENT_ID, SECRET, USER_AGENT)

    # Extract posts from the specified subreddit
    posts = extract_posts(instance, subreddit, limit)

    # Check if posts were successfully extracted
    if posts:
        # Convert the list of posts to a pandas DataFrame for further processing
        post_df = pd.DataFrame(posts)
        # print(post_df)

        # Transform the data by cleaning and modifying as needed
        post_df = data_transformation(post_df)

        # Define the file path for saving the data to a CSV file
        file_path = f'{OUTPUT_PATH}/{file_name}.csv'

        # Load the transformed data to a CSV file
        load_data_to_csv(post_df, file_path)
    else:
        # Print a message if no posts were extracted
        print('No Posts were extracted!')

    # Return the file path for further use or reference
    return file_path
