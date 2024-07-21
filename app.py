import streamlit as st
import preprocessor,helper                      #helper is used to fetch values from function made in another file
import matplotlib.pyplot as plt
import pandas as pd

st.sidebar.title('Whatsapp chat analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:                    #got this piece of code from streamlit documentation for file uploader
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode("utf-8")           #converting data in bytes to data in string
     df = preprocessor.preprocess(data)          #preprocessing done with function call(function preprocess is called)

     user_list = df['user'].unique().tolist()
     user_list.remove('group_notification')
     user_list.sort()
     user_list.insert(0,'overall')
     selected_user=st.sidebar.selectbox("show analysis wrt ",user_list)


     st.title('Analysis')
     st.dataframe(df)
     if st.sidebar.button('View analysis'):
          num_message,words,media,links=helper.fetch_stats(selected_user,df)    #getting values from function made in another file named as helper
          col1, col2, col3 ,col4= st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(num_message)

          with col2:
               st.header("Total words ")
               st.title(words)


          with col3:
               st.header("Media used")
               st.title(media)

          with col4:
               st.header("Links shared")
               st.title(links)


          #finding busiest user in the group
          if selected_user=='overall':

               x,new_df=helper.most_busy_users(df)
               name=x.index
               count=x.values
               col1, col2 = st.columns([4,2],gap="medium")
               fig, ax = plt.subplots()

               with col1:
                    st.header("Most active users")
                    ax.bar(name,count,color='green')
                    st.pyplot(fig)

               with col2:
                    st.title('% Message sent')
                    st.dataframe(new_df)



               #world cloud
          st.header("wordcloud")
          image_wc=helper.wordcloud_creation(selected_user,df)
          fig, ax = plt.subplots()     #is plotting an image which we are getting as a result from the function
          ax.imshow(image_wc)
          st.pyplot(fig)


          # # count emoji
          emoji_df = helper.emoji_helper(selected_user, df)
          st.title("Emoji Analysis")

          col1, col2 = st.columns(2)

          with col1:
               st.dataframe(emoji_df)
          with col2:
               fig, ax = plt.subplots()
               ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
               st.pyplot(fig)



          x = helper.week_activity_map(selected_user,df)
          col1, col2 = st.columns(2)
          fig, ax = plt.subplots()


          with col1:
               st.header("Most active days")
               st.dataframe(x)
          with col2:
               st.header("Most active days")
               ax.bar(x.index, x.values, color='purple')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)


