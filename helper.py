from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji
import re
import seaborn as sns
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter the DataFrame based on the selected_user

    num_messages = df.shape[0]  # Get the number of messages

    words = []
    for message in df['message']:
        words.extend(message.split())  # Split the message and add words to the list

    num_media_messages = len(df[df['message'] == '<Media omitted>\n'])  # Count the number of media messages

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))  # Find and add URLs to the list

    return num_messages, len(words), num_media_messages, len(links)

    # Layman's version:
    # if selected_user == 'Overall':
    #     num_messages = df.shape[0]
    #     #fetch number of words
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
    #     return num_messages, len(words)
    # else:
    #     new_df = df[df['user']==selected_user].shape[0]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #     return num_messages, len(words)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width = 500,height = 50, min_font_size = 10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))
    return df_wc

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    stopwords =['h', 'and', 'na', 'ki', 'ye', 'aa', 'pe', 'ka', 'se', 'ke']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
              words.append(word)

    df2 = pd.DataFrame(Counter(words).most_common(20))
    return df2

def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F6FF]|\u2600-\u26FF\u2700-\u27BF')

    for message in df['message']:
        message_emojis = emoji_pattern.findall(message)
        emojis.extend(message_emojis)

    emoji_counts = pd.Series(emojis).value_counts().reset_index()
    emoji_counts.columns = ['Emoji', 'Count']

    return emoji_counts

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time  # Assign the "time" list to the DataFrame

    return timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap1 = df.pivot_table(index='day_name', columns = 'period', values = 'message', aggfunc ='count').fillna(0)
    return heatmap1