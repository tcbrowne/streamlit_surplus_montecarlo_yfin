#app.py
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
import app1
import app2
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
from PIL import Image

#configuration must be at top
st.set_page_config(page_title='Financial Model', page_icon = ':bank:', layout = 'wide')

PAGES = {
    #"Stock Profiling": app2,
    "Clean Surplus Model": app1
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

st.sidebar.subheader('About')
st.sidebar.markdown('This app is maintained by Taylor Browne.')
link = '[LinkedIn](http://linkedin.com/in/taylorchristianbrowne)'
st.sidebar.markdown(link, unsafe_allow_html=True)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
