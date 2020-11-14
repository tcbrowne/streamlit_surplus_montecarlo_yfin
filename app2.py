# app2.py
import numpy as np
import scipy.stats as si
import sympy as sy
import matplotlib as mpl
import random
import pandas as pd
import streamlit as st
import seaborn as sns
import yfinance as yf
import plotly.figure_factory as ff
import plotly.express as px
import datetime
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
from PIL import Image

def app():
    st.title('Stock Profiling')

    
    st.subheader("Select the company you wish to profile")

    option = st.text_input("Input ticker here:", "GOOG")
    tkr = yf.Ticker(option)

    st.markdown("Company Logo")
    url = tkr.info['logo_url']
    st.markdown("![Alt Text]({})".format(url))

    # col7, col8 = st.beta_columns((4,1))
    # with col7:
    #     option = st.text_input("Input ticker here:", "GOOG")
    #     tkr = yf.Ticker(option)
    # with col8:
    #     st.markdown("Company Logo")
    #     url = tkr.info['logo_url']
    #     st.markdown("![Alt Text]({})".format(url))

    st.title("About {}".format(option))
    st.write(tkr.info['longBusinessSummary'])

    st.title("{} Recommendations".format(option))
    st.subheader("Select Date Range")

    col1, col2 = st.beta_columns(2)
    with col1:
        date1 = st.date_input("Start Date",datetime.date(2020, 1, 1))
    with col2:
        date2 = st.date_input("End Date",datetime.date(2020, 11, 1))

    stock_recom1 = tkr.recommendations
    stock_recom2 = stock_recom1.loc[date1:date2]
    stock_recom3 = stock_recom2.groupby(['To Grade'],as_index=False)[['Firm']].count()
    
    st.subheader("Stock Recommendations between dates {} and {}".format(date1,date2)) #include slicer / slider in future to pick date range
    
    col5, col6 = st.beta_columns((1,1))
    with col5:
        st.dataframe(stock_recom2,height=400)
    with col6:
        fig = px.pie(stock_recom3, values='Firm', names='To Grade', title='Distribution by Recommendations')
        st.plotly_chart(fig, use_container_width=True)

#     st.title("Sustainability Reports for {}".format(option))
#     st.write(tkr.sustainability)

#     st.title("Event Calendar for {}".format(option))
#     st.write(tkr.calendar)

#     st.title("Earnings for {}".format(option))
#     st.write(tkr.earnings)
    
    bs = tkr.balance_sheet
    pl = tkr.financials

    bs[~bs.index.str.contains("Total")]
    bs[~bs.index.str.contains("Net Assets")]
    pl[~pl.index.str.contains("Total")]

    bs.rename(columns={ bs.columns[0]: "Current Year", bs.columns[1]: "Prior Year"}, inplace = True)
    pl.rename(columns={ pl.columns[0]: "Current Year", pl.columns[1]: "Prior Year"}, inplace = True)

    col3, col4 = st.beta_columns((1,1))
    with col3:
        st.title("Balance Sheet for {}".format(option))
        st.dataframe(bs)
    with col4:
        st.title("P&L for {}".format(option))
        st.dataframe(pl)


    yrselect = st.selectbox(
        'Select Year',
        ('Current Year','Prior Year'))

    st.title("Balance Sheet Visualization")
    fig2 = px.histogram(bs, histfunc="sum", x = bs.index, y = yrselect)
    st.plotly_chart(fig2, use_container_width=True)

    st.title("P&L Visualization")
    fig3 = px.histogram(pl, histfunc="sum", x = pl.index, y = yrselect)
    st.plotly_chart(fig3, use_container_width=True)
