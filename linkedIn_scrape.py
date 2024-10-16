# Native
import re
import time

# Third party
import pandas as pd
from splinter import Browser

from notebooks.linkedIn_cred import linkedIn_email, linkedIn_password
from scripts.company_objects import daugherty, slalom, _1904labs, worldWideTechnology

companies = [daugherty, slalom, _1904labs, worldWideTechnology]

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=True)
browser.driver.set_window_size(
    1600, 900
)  # Has to be wide enough to prevent messenger from covering filter buttons


def log_on_to_linkedIn():
    browser.visit(companies[0].linkedin)
    button = browser.links.find_by_partial_href("https://www.linkedin.com/login?")
    button.click()
    browser.fill("session_key", linkedIn_email)
    browser.fill("session_password", linkedIn_password)
    button = browser.find_by_value("Sign in")
    button.click()


def scrape_profile_metadata(company):
    url = company.linkedin
    browser.visit(url)
    html = browser.html
    data = {}

    followers = re.search(r"[\d,]+ followers", html, re.DOTALL).group()
    followers = re.sub("[^\d]", "", followers)  # returns only digits
    followers = int(followers)

    employees_on_linkedin = re.search(r"[\d,]+ employees", html, re.DOTALL).group()
    employees_on_linkedin = re.sub(
        "[^\d]", "", employees_on_linkedin
    )  # returns only digits
    employees_on_linkedin = int(employees_on_linkedin)

    print(
        f"{company.name} has {followers} followers and {employees_on_linkedin} employees on LinkedIn."
    )

    data["name"] = [company.name]
    data["followers"] = [followers]
    data["employees_on_linkedin"] = [employees_on_linkedin]

    profile_metadata_df = pd.DataFrame(data=data)
    profile_metadata_df.to_csv(f"../data/{company.name}_profile_metadata.csv")


def scrape_profile_posts_by_most_recent():
    button = browser.find_by_css("div[class='sort-dropdown mt2 ember-view']")
    button.click()
    button = browser.find_by_text("Recent")
    button.click()


def scroll_down_until_all_posts_are_loaded():
    number_posts_before_scroll = len(
        browser.find_by_css("div[class='occludable-update ember-view']")
    )

    while number_posts_before_scroll > 1:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        number_posts_after_scroll = len(
            browser.find_by_css("div[class='occludable-update ember-view']")
        )

        if number_posts_before_scroll == number_posts_after_scroll:
            timer = time.time()
            thirty_seconds_elapsed = timer + 30

            while time.time() < thirty_seconds_elapsed:
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                number_posts_after_scroll = len(
                    browser.find_by_css("div[class='occludable-update ember-view']")
                )

            if number_posts_before_scroll == number_posts_after_scroll:
                print("finished")
                break
        else:
            number_posts_before_scroll = len(
                browser.find_by_css("div[class='occludable-update ember-view']")
            )

    print(f"Number of posts {number_posts_before_scroll}")


def scrape_company_posts(id):
    posts = browser.find_by_css("div[class='occludable-update ember-view']")

    data = {"content": [], "like_count": [], "comment_count": [], "date": []}

    for post in posts:
        post = post.text

        try:
            date = re.search(r"^(\w+ •\n|\w+ ago\n)", post, re.MULTILINE).group()
            date = re.sub("\n", "", date)
        except Exception as e:
            print(f"no date: {e}")
            date = ""

        try:
            like_count = re.search(r"^[\d]+$", post, re.MULTILINE).group()
            like_count = int(like_count)
        except Exception as e:
            print(f"no like count: {e}")
            like_count = 0

        try:
            # Content always follows the time the post was published and precedes the like count.
            contentRegex = re.compile(
                f"( •\n| ago\n).*?^({like_count})$", re.MULTILINE | re.DOTALL
            )
            content = re.search(contentRegex, post).group()
            content = re.sub(
                r"( •\n| ago\n)", "", content, re.MULTILINE | re.DOTALL
            )  # Gets rid of the leading timestamp
            content = content[
                : -len(str(like_count))
            ]  # Gets rid of the trailing like count
        except Exception as e:
            print(f"no content: {e}")
            content = ""

        try:
            comment_area = re.search(r"^[\d]+ comment(s)?$", post, re.MULTILINE).group()
            comment_count = re.sub(r"[^\d]", "", comment_area)  # returns only digits
            comment_count = int(comment_count)
        except Exception as e:
            print(f"no comment count: {e}")
            comment_count = 0

        print(f"\n\nlikes: {like_count}")
        print(f"comments: {comment_count}")
        print(f"content: {content}")

        data["content"].append(content)
        data["like_count"].append(like_count)
        data["comment_count"].append(comment_count)
        data["date"].append(date)

    company_posts_df = pd.DataFrame(data)
    company_posts_df.to_csv(f"../data/{companies[id].name}_company_posts.csv")


log_on_to_linkedIn()

for id in range(len(companies)):
    scrape_profile_metadata(companies[id])
    browser.visit(companies[id].linkedin)
    scrape_profile_posts_by_most_recent()
    scroll_down_until_all_posts_are_loaded()
    scrape_company_posts(id)

browser.quit()
