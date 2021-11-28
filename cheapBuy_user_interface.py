"""
Copyright (c) 2021 Anshul Patel
This code is licensed under MIT license (see LICENSE.MD for details)

@author: cheapBuy
"""

# Import Libraries
import sys
sys.path.append('../')
import streamlit as st
import os
from source.web_scrappers.WebScrapper import WebScrapper
import pandas as pd
import webbrowser
#from link_button import link_button

title = '<p style="font-family:sans-serif; color:Orange; font-size: 42px;">CheapBuy</p>'
#st.title("CheapBuy")
st.markdown(title, unsafe_allow_html=True)
st.sidebar.title("Customize Options Here:")
sites = st.sidebar.selectbox("Select the website:", ("All Sites", "amazon", "walmart", "ebay", "bjs", "costco", "bestbuy"))

price_range = st.sidebar.selectbox("Select the price range:", ("search all", "Under $50", "[$50, $100)", "[$100, $150)", "[$150, $200)", "$200 & Above"))
st.header("Search Product in " + sites)

# Hide Footer in Streamlit
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Display Image
st.image("media/cheapBuy_Banner.gif")

st.write("cheapBuy provides you ease to buy any product through your favourite website's like Amazon, Walmart, Ebay, Bjs, Costco, etc, by providing prices of the same product from all different websites")
url = st.text_input('Enter the product website link')


def price_filter(price_range):
    #price_min, price_max = 0.0, 0.0
    if price_range == "Under $50": price_min, price_max = 0.0, 49.99
    elif price_range == "[$50, $100)": price_min, price_max = 50.0, 99.99
    elif price_range == "[$100, $150)": price_min, price_max = 100.0, 149.99
    elif price_range == "[$150, $200)": price_min, price_max = 150.0, 199.99
    elif price_range == "$200 & Above": price_min, price_max = 200.0, float('inf')
    else: 
        price_min, price_max = 0.0, float('inf')
    return price_min, price_max

price_min, price_max = price_filter(price_range)

# Pass url to method
if url:
    webScrapper = WebScrapper(url)
    results = webScrapper.call_scrapper()
    print(results)

    # Use st.columns based on return values
    description, url, price, site = [], [], [], []
    
    if sites == "All Sites":
        for result in results:
            # add results that only fit to selected price range :
            if result: 
                try:
                    if price_min <= float(result['price'][1:]) <= price_max:
                        description.append(result['description'])
                        url.append(result['url'])
                        price.append(float(result['price'].strip('$').rstrip('0')))
                        site.append(result['site'])
                except Exception as e:
                    print(e)

    else:
        #if sites not in site: 
            #st.error('Sorry, there is no same product in your selected website.')
            
        #else:
        for result in results:
            # add results that only fit to selected price range :
            if result:
                try:
                    if price_min <= float(result['price'][1:]) <= price_max:
                #print(result['site'])
                        if result['site'].strip() == sites:
                            description.append(result['description'])
                            url.append(result['url'])
                            price.append(float(result['price'].strip('$').rstrip('0')))
                            site.append(result['site'])
                except Exception as e:
                    print(e)
    
    
    if len(price):
        
        def highlight_row(dataframe):
            #copy df to new - original data are not changed
            df = dataframe.copy()
            minimumPrice = df['Price'].min()
            #set by condition
            mask = df['Price'] == minimumPrice
            df.loc[mask, :] = 'background-color: lightgreen'
            df.loc[~mask,:] = 'background-color: ""'
            return df
        
        dataframe = pd.DataFrame({'Description': description, 'Price':price, 'Link':url}, index = site)
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #1DC5A9;'>RESULT</h1>", unsafe_allow_html=True)
        st.dataframe(dataframe.style.apply(highlight_row, axis=None))
        st.markdown("<h1 style='text-align: center; color: #1DC5A9;'>Visit the Website</h1>", unsafe_allow_html=True)

        for s,u,p in zip(site,url,price):
            if p == min(price):
                if st.button('👉    '+s+'    👈'):
                    #webbrowser.open_new_tab(u)
                    webbrowser.open(u)
            else:
                if st.button(s):
                    #webbrowser.open_new_tab(u)
                    webbrowser.open(u)
            
    #            link_button(site[minimum_i], url[minimum_i])

    elif not description or not url or not price or not site:
        st.error('Sorry, there is no product on your selected options.')
    else:
        st.error('Sorry, there is no other website with same product.')
        


# Add footer to UI
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0%;
width: 100%;
background-color: #CCCCFF;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p><a style='display: block; text-align: center;' href="https://github.com/freakleesin/cheapBuy" target="_blank">Developed with ❤ by cheapBuy</a></p>
<p><a style='display: block; text-align: center;' href="https://github.com/freakleesin/cheapBuy/blob/main/LICENSE" target="_blank">MIT License Copyright (c) 2021 cheapBuy</a></p>
<p>Contributors: 
<a href="https://github.com/Mahaoqu" target="_blank">Haoqu</a>, 
<a href="https://github.com/joshlin5" target="_blank">Joshua</a>, 
<a href="https://github.com/zhijin44 target="_blank">Zhijin</a>, 
<a href="https://github.com/SamuelVivivi" target="_blank">Guanyu</a>, 
<a href="https://github.com/freakleesin" target="_blank">Rundi</a>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)

