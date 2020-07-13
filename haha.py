# Importing requires modules
import praw
import requests

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
submission = reddit.submission(id='')


# Getting data/numbers
def stats(link):
    data = requests.get(link).json()
    tested = data.get('nepal').get('samples_tested')
    negative = data.get('nepal').get('negative')
    positive = data.get('nepal').get('positive')
    deaths = data.get('nepal').get('deaths')
    dt = data.get('nepal').get('created_at')
    recovered = data.get('nepal').get('extra1')
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
     



def prev_data():
    text = submission.selftext
    data = text.split()

    i = 0
    for word in data:
        if word == 'Cases:':
            total = data[i+1]
        elif word == 'Deaths:':
            deaths = data[i+1]
        elif word == 'Recovered:':
            recovered = data[i+1]

        i +=1

    msg = f'{total} {deaths} {recovered}'

    print("previous data extracted")
    print(msg)
    return msg

while True:
    time.sleep(10)
    wau = prev_data()
    db_data = wau.strip().split(' ')
    new_data = stats(url)
    new_datal = new_data.split(' ')
    if new_datal[3] != db_data[1] or new_datal[2] != db_data[0]:
        msg = f"Total Positive Cases: {new_datal[2]}\n\nDeaths: {new_datal[3]}\n\nRecovered: {new_datal[4]}\n\nSamples Tested: {new_datal[0]}\n"
        print("New data found.... Tweeting...")
        print(new_datal,db_data)
        submission.edit(msg)


