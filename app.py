import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st

import helper
import preprocessor

hide_st_style = """
                <style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/abhiiiman',
        'Report a bug': "https://www.github.com/abhiiiman",
        'About': "## A 'WhatsApp Chat Analyzer Tool' by Abhijit Mandal"
    }
)

# remove all the default streamlit configs here
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.title("Whatsapp Chat Analyzer 🤖")

uploaded_file = st.sidebar.file_uploader("Choose a file 📂")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("1️⃣ Top Statistics 📊")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(f"📩 {num_messages}")
        with col2:
            st.header("Total Words")
            st.title(f"🔠 {words}")
        with col3:
            st.header("Media Shared")
            st.title(f"🖼️ {num_media_messages}")
        with col4:
            st.header("Links Shared")
            st.title(f"🔗 {num_links}")

        # monthly timeline
        st.title("2️⃣ Monthly Timeline 🗓️")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("3️⃣ Daily Timeline 🗓️")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('4️⃣ Activity Map 🎭')
        col1, col2 = st.columns(2)

        with col1:
            st.header("4.1 Most Active Day 🤩")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("4.2 Most Active Month 🤩")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("5️⃣ Weekly Activity Map 🎭")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        h_map = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('6️⃣ Most Active Users 🤩')
            # x, new_df = helper.most_busy_users(df)
            x, new_df, most_msgs, least_msgs = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                st.write(f"⭐ Most Active User is `{most_msgs[0]}` with `{most_msgs[1]}` Chats.")
                st.write(f"⭐ Least Active User is `{least_msgs[0]}` with `{least_msgs[1]}` Chats.)")

            # WordCloud
            st.title("7️⃣ Wordcloud ☁️")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('8️⃣ Most common words ➕')
            st.pyplot(fig)

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("9️⃣ Emoji Analysis 🫢")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = px.pie(emoji_df.head(), values='count', names='emoji', title='⭐ Emoji Distribution', hole=0.3,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig)
