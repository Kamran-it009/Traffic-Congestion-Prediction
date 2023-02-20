import pandas as pd
import streamlit as st
from functions import main
st.set_page_config(page_title="Traffic JAM Prediction", page_icon=":guardsman:", layout="centered")
st.title("Traffic Congestion Prediction")

options = ["Breda--Tilburg", "Tilburg--Breda"]
selected_option = st.selectbox("Choose an option:", options)


df = main(0, 1) if options.index(selected_option) == 0 else main(1, 0)
dates_list = list(df.Date.unique())
# for date in dates_list:
#     button = st.button(str(date))
#     if button:
#         df1 = df[df['Date'] == date]

display_flag = False
button_dates = dates_list
print(button_dates)
for i in range(0, 4):
    for col in st.columns(4):
        with col:
            date = button_dates.pop(0) if len(button_dates) > 0 else None
            if date == None:
                break
            button = st.button(str(date))
            if button:
                df1 = df[df['Date'] == date]
                display_flag = True

if display_flag:
    st.write('Best Time to drive')
    st.dataframe(df1[['Time', 'Traffic Jam']])

# print(dates_list)
# print(df)
