"""! This file is just a template and is currently not functional."""

import sys

import pandas as pd

sys.path.append("..")
from classes.DB import DB

web_data_db = DB()
web_data_db.connect()
web_data_db.create_table_company_profiles()
web_data_db.create_table_company_posts()

profile_metadata_df = pd.read_csv("../data/Slalom_profile_metadata.csv")
company_posts_df = pd.read_csv("../data/Slalom_company_posts.csv")

for index, row in profile_metadata_df.iterrows():
    name = row["name"]
    followers = row["followers"]
    employees_on_linkedin = row["employees_on_linkedin"]
    web_data_db.into_company_profiles(name, followers, employees_on_linkedin, url)

for index, row in company_posts_df.iterrows():
    content = row["content"]
    like_count = row["like_count"]
    comment_count = row["comment_count"]
    date = row["date"]
    web_data_db.into_company_posts(content, like_count, comment_count, date, index + 1)

web_data_db.select()
