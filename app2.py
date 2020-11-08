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

    url = tkr.info['logo_url']
    st.markdown("![Alt Text]({})".format(url))

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
    st.write(stock_recom2)

    fig = px.pie(stock_recom3, values='Firm', names='To Grade', title='Distribution by Recommendations')
    st.plotly_chart(fig, use_container_width=True)