import streamlit as st
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

import Preprocessor
from Preprocessor import preprocess
import helper
import seaborn as sns
import emoji


st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = Preprocessor.preprocess(data)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    for i in range(len(user_list)):
        if user_list[i] == 'group_notification':
            user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total links shared")
            st.title(links)

        #timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            st.pyplot(fig)

        st.title("Heatmap")
        heatmap1 = helper.heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap1)
        st.pyplot(fig)
        #finding the busiest users in the group chat
        if selected_user == 'Overall':
            st.title('most busy person')
            col1, col2 = st.columns(2)
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #mosgt common words
        most_common = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common[0], most_common[1])
        plt.xticks(rotation = 'vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        #emoji analysis
        st.title("emoji analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            counts = emoji_df['Count'].astype(int)
            ax.pie(counts.head(10), labels=emoji_df['Emoji'].head(10), autopct ='%0.2f')
            st.pyplot(fig)