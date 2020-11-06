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
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
from PIL import Image
init_printing()

# include values in millions
st.title("Select the company you wish to value")
# option = st.radio(
#     'Ticker Selection',
#     ('GOOG', 'AAPL', 'FB'))

# image = Image.open('machine-learning.jpg')

# st.image(image, caption='',
#   use_column_width=True)

option = st.text_input("Input ticker here:", "GOOG")

tkr = yf.Ticker(option)

#Financial Statement Variables
by = 2019
py = by - 1

netincome = tkr.financials.loc['Net Income',:].tolist()
byNI = netincome[0]
print(byNI)

numshares = tkr.info['sharesOutstanding']
print(numshares)

bookvalue1 = tkr.balancesheet.loc['Total Stockholder Equity',:].tolist()
byBV = bookvalue1[0]
pyBV = bookvalue1[1]
print(byBV)
print(pyBV)

divy = tkr.dividends.tolist()
byDivtemp = divy.reverse()
byDivtemp = divy[0:4]
byDiv = (sum(byDivtemp) * numshares)

print(byDiv)

#CAPM Variables
vRf = 0.0085
vMRP = 0.058
Bta = tkr.info['beta']
vMR = vRf + vMRP
Kc = (vRf * (1 - Bta)) + (Bta*vMR)
print(Kc)

pytrt = byDiv / byNI #payout ratio defined as Dividend (base year) / NI (base year), assume will contineu for seven years
print(pytrt)

def fun(currentyear, finalyear, BVpy, pytrt, vROE):
  Book_Values = []
  BVcy = BVpy
  for i in range(int(currentyear), int(finalyear)):
    BVcy = BVcy*(1+((1-pytrt)*vROE))
    Book_Values.append(float(BVcy))
  return Book_Values
 

def some(voxvalues, Kc):
    temp = []
    n = 1
    for i in voxvalues:
        temp.append(i/((1+Kc)**(n)))
        n = n+1
    return temp

def ValuationStatement(currentprice, intrinsicprice, ValueComparison):
    if currentprice -  intrinsicprice >= 0:
        statement = "Shares overvalued by {}".format(ValueComparison)
    elif currentprice - intrinsicprice <= 0:
        statement = "Shares undervalued by {}".format(ValueComparison)
    
    return statement

def SurplusModel(vROE_input,vROE):
    Book_Values = fun(by + 1, by + vROE_input - 1, byBV, pytrt, vROE)

    Book_Values.insert(0,byBV)

    vOX_Values = [i * (vROE - Kc) for i in Book_Values]

    vPA = byBV + sum(some(vOX_Values, Kc))

    # Share_Value = vPA / (numshares / 1000000)
    Share_Value = vPA / numshares 
    
    return Share_Value


def crude_monte_carlo(num_samples):

    sum_of_samples = 0

    Value_var = []
    roe_len_Var = []
    roe_var = []

    for i in range(num_samples):
        x1 = random.uniform(z1,z2) # range of vROE len 3,20
        x2 = random.uniform(n1,n2) # range of vROE, 0.08,0.23
        
        sum_of_samples += SurplusModel(x1,x2)
        
        Value_var.append(SurplusModel(x1,x2))
        roe_len_Var.append(x1)
        roe_var.append(x2)

    print(float(sum_of_samples/num_samples))

    return (Value_var,roe_len_Var,roe_var) #float(sum_of_samples/num_samples)

#Streamlit Section for WebApp
st.sidebar.subheader('How is the valuation calculated?')
st.sidebar.markdown('The **Clean-Surplus-Model (Risidual Income Model)** is used to determining market value, utilizing balance sheet and income statement fundamentals. The two variables hard to define in this model are Return on Equity (RoE) and the horizon in which RoE exceeds Cost of Capital (Kc). Therefore, we leverage a monte carlo simulation over a uniform probability for input variables to determine the possible range of valuations')

st.sidebar.subheader('Assumptions')
st.sidebar.markdown('Assumes capital market conditions are stable and dividend irrelevancy.')
st.sidebar.markdown('Assumes that the company is not in a growth stage (i.e., negative ROE). Might be more appropriate to use projected or industry average ROE.')
st.sidebar.markdown('Assumes that ROE stays constant for horizon input. In reality, ROE can change in response to a number of factors such as competition. ROE has been determined from the fundamentals of the financial statements in one particular year. Therefore, it is static and may not encapsulate all the information gathered / researched, for instances, by analysts.')
st.sidebar.markdown('Additionally, model assumes that abnormal earnings persist for the horizon given and then drop to zero. Reality could be quite different, for example, persist for only three years or fifteen. There is potential for a "declining abnormal earnings pattern" that is not captured in this model.')

st.title('Monte Carlo: Share Price of {}'.format(option))

# sim1 = st.slider('How many simulations would you like to run?',100,100000,1000)
sim1 = st.select_slider(
     'How many simulations would you like to run?',
     options=[100, 1000, 10000, 100000, 1000000])

st.subheader("Variable #1: Length of expected earnings surprise (RoE > cost of capital).")

col1, col2 = st.beta_columns(2)

with col1:
    z1 = st.slider('Lower bound of expected earnings surprise.',1,100,3)

with col2:
    z2 = st.slider('Upper bound of expected earnings surprise.',1,100,20)


st.subheader("Variable #2: Expected RoE over the period.")

col3, col4 = st.beta_columns(2)

with col3:
    n1 = st.slider('Lower bound of expected RoE.',0.01,1.00,0.08)

with col4:
    n2 = st.slider('Upper bound of expected RoE.',0.01,1.00,0.23)

Monte_Distribution = crude_monte_carlo(sim1)

value_list = Monte_Distribution[0]
roe_len_list = Monte_Distribution[1]
roe_list = Monte_Distribution[2]

monte_df = pd.DataFrame({'Valuation':value_list, 'Years of RoE > Kc':roe_len_list,"RoE":roe_list})

avrg_value = monte_df['Valuation'].sum() / len(monte_df.index)

st.subheader("Simulated Mean Share Price")
st.write('Average value of {} Share Price simulated {} times'.format(option, len(monte_df.index)))
st.write(avrg_value)

# Graphs & Density Distribution
# st.subheader("Distribution of All Simulations")
# monte_df[['Valuation']].plot(kind='density') # or pd.Series()
# plt.title('{} Share Price Distribution'.format(option))
# st.pyplot()

st.set_option('deprecation.showPyplotGlobalUse', False)
ax = sns.histplot(value_list)
plt.title('{} Share Price Distribution'.format(option))
ax.set(xlabel='Share Valuation', ylabel='Frequency')
st.pyplot()

st.subheader("Summary Statistics of Simulations")
st.table(monte_df[["Valuation", "Years of RoE > Kc", "RoE"]].describe())

#THis shows whole dataframe which is too much
# st.subheader("Simulations of Share Price")
# st.table(monte_df)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
