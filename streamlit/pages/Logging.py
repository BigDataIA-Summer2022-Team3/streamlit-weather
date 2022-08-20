import streamlit as st
import pymysql
import pandas as pd
Host, User, Password = st.secrets["Host"] , st.secrets["User"] , st.secrets["Password"]
con = pymysql.connect(host = Host, user = User, password = Password, database = 'damg', charset = "utf8")
c = con.cursor()
c.execute('select * from log_table')
datainfo = c.fetchall()

users = ['zhijie', 'yijun', 'team4', 'parth', 'srikanth', 'airflow']
visit_times = []
zhijie = 0
yijun = 0
team4 = 0
parth = 0
srikanth = 0
sumairflow = 0
for a in datainfo:
    if a[1] == 1:
        zhijie = zhijie + 1
    elif a[1] == 2:
        yijun = yijun + 1
    elif a[1] == 3:
        team4 = team4 + 1
    elif a[1] == 4:
        parth = parth + 1
    elif a[1] == 5:
        srikanth = srikanth + 1
    else:
        sumairflow = sumairflow + 1

visit_times.append(zhijie)
visit_times.append(yijun)
visit_times.append(team4)
visit_times.append(parth)
visit_times.append(srikanth)
visit_times.append(sumairflow)

prcp_df = pd.DataFrame({
    'users': users,
    'visit_times': visit_times
    })
prcp_df = prcp_df.rename(columns={'users':'index'}).set_index('index')
st.bar_chart(prcp_df)