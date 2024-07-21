from urlextract import URLExtract    #helps to fetch links from string
from wordcloud import WordCloud
import emoji
from collections import Counter
import pandas as pd

# #import library for sentiment analysis
# from textblob import TextBlob

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    num_message=df.shape[0]
    words=[]
    media=0
    links=[]
    for message in df['message']:
        words.extend(message.split())
        if message=="<Media omitted>\n":     # I have used \n because it is originally there in dataframe
            media=media+1
    for message in df['message']:
        links.extend(extract.find_urls(message))     # This is adding all links found in links list
    return num_message,len(words),media,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head(3)
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    return x,new_df  # z is not in the form of dataframe



def wordcloud_creation(selected_user,df):
    f = open('stopwords.txt.rtf', 'r')
    stop_words = f.read()
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def emoji_helper(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def week_activity_map(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    z=df['day_name'].value_counts()
    return z  #z is not in the form of dataframe









