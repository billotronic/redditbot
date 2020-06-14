# Importing requires modules
import praw
import requests
from bs4 import BeautifulSoup

# Reddit Authentication
# Enter you keys here
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     password="",
                     user_agent="",
                     username="")

# Global Variable
subreddit = reddit.subreddit('Nepal') # Configuring which subreddit to search
keyphrase = "!covid" # Configuring which catchphrase to reply
url = "https://covid19.mohp.gov.np/covid/api/confirmedcases" # Source of data


# Getting data/numbers
def stats(link):
    data = requests.get(link).json()
    tested = data.get('nepal').get('samples_tested')
    negative = data.get('nepal').get('negative')
    positive = data.get('nepal').get('positive')
    deaths = data.get('nepal').get('deaths')
    dt = data.get('nepal').get('created_at')
    recovered = BeautifulSoup(requests.get("https://www.worldometers.info/coronavirus/country/nepal/").text,
                              'html.parser').find_all('div', {'class': 'maincounter-number'})[2].text.strip()
    new_data = f"{tested} {negative} {positive} {deaths} {recovered} {dt}"
    return new_data


def rep():
    new_data = stats(url)
    new_datal = new_data.split(' ')
    msg = f"Total Positive Cases: {new_datal[2]} || Deaths: {new_datal[3]} || Recovered: {new_datal[4]} || Samples Tested: {new_datal[0]}\n"
    return msg


 # Searching Comments
for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        print("Found one!")
        msg=(rep())
        comment.reply(msg) # Replying to catchphrase
        print("replied")

