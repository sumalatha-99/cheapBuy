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
st.sidebar.title("Choose the site where you want to find the cheapest product here:")
sites = st.sidebar.selectbox("Which site?", ("All Sites", "amazon", "walmart", "ebay", "bjs", "costco", "bestbuy"))

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


# Pass url to method
if url:
    webScrapper = WebScrapper(url)
    results = webScrapper.call_scrapper()

    # Use st.columns based on return values
    description, url, price, site = [], [], [], []
    
    if sites == "All Sites":
        for result in results:
            if result!={}:
                description.append(result['description'])
                url.append(result['url'])
                price.append(float(result['price'].strip('$').rstrip('0')))
                site.append(result['site'])

    else:
        #if sites not in site: 
            #st.error('Sorry, there is no same product in your selected website.')
            
        #else:
        for result in results:
            if result != {}:
                #print(result['site'])
                if result['site'].strip() == sites:
                    print("1")
                    description.append(result['description'])
                    url.append(result['url'])
                    price.append(float(result['price'].strip('$').rstrip('0')))
                    site.append(result['site'])
    
    

        
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
        min_value = min(price)
        min_idx = [i for i, x in enumerate(price) if x == min_value]

        for minimum_i in min_idx:

            link = url[minimum_i]
            if st.button(site[minimum_i]):
                # link a button to the new page.
                webbrowser.open_new_tab(url[minimum_i])

    #            link_button(site[minimum_i], url[minimum_i])

    elif not description or not url or not price or not site:
        st.error('Sorry, there is no same product on your selected website.')
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
background-color: #DFFFFA;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/freakleesin/cheapBuy" target="_blank">cheapBuy</a></p>
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

