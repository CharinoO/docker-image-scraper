from math import ceil
from numpy import NaN
import streamlit as st
from PIL import Image
from exapackage.shop import Tokopedia
from exapackage.keys import Tokopedia as TokpedKeys
from exapackage.shopee_global import Shopee
from exapackage.shopee_store_item import store_search
from exapackage.shopee_store_item_all import store_all_search
import os
import time
from datetime import datetime
import pandas as pd
import streamlit_authenticator as stauth
import numpy as np

def main():
    def update_pages():
        """
        update state initial text box from max page
        """
        st.session_state.page_awal = st.session_state.page

    def update_data_source():
        """
        update state initial data source from target website
        """
        st.session_state.data_folder = st.session_state.source
    
    def condition_shopee_seller(df):
        #create a list of our conditions
        data = df.copy()
        conditions = [
            (data['is_official_shop'] == True),
            (data['is_preferred_plus_seller'] == True) & (data['is_shopee_verified'] == True),
            (data['is_shopee_verified'] == True),
            (data['is_preferred_plus_seller'] == False ) & (data['is_shopee_verified'] == False) & (data['is_official_shop'] == False)
            ]

        # create a list of the values we want to assign for each condition
        values = ['Mall', 'Star plus seller', 'star seller', NaN]

        # create a new column and use np.select to assign values to it using our lists as arguments
        data['tier'] = np.select(conditions, values)
        return data


    def qty_to_int(s):
        if type(s) == str:
            s_split = s.split()

            if len(s_split) > 1:
                if s_split[-1] == 'rb':
                    return int(s_split[1].replace(',', '')) * 100 if ',' in s_split[1] else int(s_split[1]) * 1000
                else:
                    return int(s_split[1])
        # if NaN
        return int(0)

    def process_data(df) -> pd.DataFrame:
        """
        Processing column in a dataframe.
        output -> Dataframe
        """
        # Data pada kolom 'Original Price' dan 'Final Price' semuanya berupa string
        df['Original Price'] =  [int(x.replace('Rp', '').replace('.', '')) if 'Rp' in x else int(0) for x in df['Original Price']]
        df['Final Price'] =  [int(x.replace('Rp', '').replace('.', '')) if 'Rp' in x else int(0) for x in df['Final Price']]
        df['Qty Sold'] = [qty_to_int(x) for x in df['Qty Sold']]

        return df


    def sort_by(name):
        val = {'Paling Sesuai':23, 'Terbaru':2, 'Harga Tertinggi':10,
                'Harga Terendah':9, 'Ulasan Terbanyak':11, 'Pembelian Terbanyak':8,
                'Dilihat Terbanyak':5, 'Pembaruan Terakhir':3}
        return val[name]

    def res_filter(name):
        val = {'Paling Sesuai':23, 'Ulasan':5, 'Terbaru':9,
                'Harga Tertinggi':4, 'Harga Terendah':3}
        
        return val[name]

    def show_dataset():
        src = st.selectbox('Data Source', ['Tokopedia', 'Shopee'], key='data_folder')
        if src == 'Tokopedia':
            folder = os.listdir('Data-Tokopedia/')
            folder.sort(reverse=True)
            if folder:
                res = st.selectbox('Dataset', folder)
                df  =  pd.read_csv('Data-Tokopedia/'+ res, sep=';')
                badge = st.multiselect("Filter by Store Badge : ", default= df['Badge'].unique(), options=df['Badge'].unique())
                st.write('***Result**')
                df_final = df.query("Badge == @badge")
                st.dataframe(df_final)


                data = df_final.to_csv(sep=';').encode('utf-8')
                col_sh1, col_sh2, col_sh3 = st.columns(3)
                with col_sh1:
                    st.download_button("Download here", data=data, file_name=res, mime='text/csv', key='download-csv')
                with col_sh2:
                    st.write('')
                with col_sh3:
                    delete_button = st.button("Delete this file")
                    if delete_button:
                        os.remove("Data-Tokopedia/" + res)
                        st.warning("Data deleted")
                        st.experimental_rerun()
		
            else:
                st.warning("No datasets found")
        else:
            folder = os.listdir('Data-Shopee/')
            folder.sort(reverse=True)
            if folder:
                res = st.selectbox('Dataset', folder)
                df  =  pd.read_csv('Data-Shopee/'+ res, sep=';')
                df  = condition_shopee_seller(df)
                cols = df.columns[(df.columns != 'is_official_shop') & (df.columns != 'is_preferred_plus_seller') & (df.columns != 'is_shopee_verified')]
                cols = list(cols)
                cols.remove('tier')
                cols.insert(1, 'tier')
                df  = df[cols]
                badge_shopee = st.multiselect("Filter by Store Badge : ", default= df['tier'].unique(), options=df['tier'].unique())
                st.write('***Result**')
                df_final_shopee = df.query("tier == @badge_shopee")
                st.dataframe(df_final_shopee)

                data = df_final_shopee.to_csv(sep=';').encode('utf-8')
                col_sh1, col_sh2, col_sh3 = st.columns(3)
                with col_sh1:
                    st.download_button("Download here", data=data, file_name=res, mime='text/csv', key='download-csv')
                with col_sh2:
                    st.write('')
                with col_sh3:
                    delete_button = st.button("Delete this file")
                    if delete_button:
                        os.remove("Data-Shopee/" + res)
                        st.warning("Data deleted")
                        time.sleep(1)
            else:
                st.warning("No datasets found")
    
    st.set_page_config(page_title="Spider Scraper", layout='wide')
    names            = ['team merch','team exa']
    usernames        = ['merch','exa']
    hashed_passwords = ("$2b$12$HwAdj.1ql8/ftD8LSzCqReE5jWKXNK7R2AJf5p/hfvqKwctS/v1fe",
                        "$2b$12$SgSFaxyEXOeVhUY7iJdsUe3ivc5KSQgWmtM9z98e1qhfsaPJRHmlK")
    cookie_name      = "EXAMERCH_cookies_and_cream"
    
    authenticator = stauth.authenticate(names,usernames,hashed_passwords,
        cookie_name, "some_signature_name",cookie_expiry_days=1)
    log_1, log_2, log_3 = st.columns(3)
    with log_1:
        st.write('')
    with log_2:
        name, authentication_status = authenticator.login('Login','main')
        if authentication_status == None:
            st.warning("Input Username and Email")
        elif authentication_status == False:
            st.warning("Wrong Username or Email")
    with log_3:
        st.write('')

    if authentication_status:
        
        with st.sidebar:
            
            st.markdown("<h1 style='text-align: center;'>EXA x MERCH  </h1>", unsafe_allow_html=True)
            option = st.selectbox('Website to crawl', ['Tokopedia', 'Shopee'], key="source", on_change=update_data_source)
            option2 = st.selectbox('Get data by: ', ['Keyword', 'Shop Link'])
            if option == 'Tokopedia':
                    
                if option2 == 'Keyword':

                    keyword = st.text_area('Input Keyword(s)', placeholder='Seperate word by new line')
                    keyword = keyword.split('\n')
                    keyword = [x for x in keyword if x != '']
                    filter_by = st.selectbox('Sort By : ', ['Paling Sesuai', 'Ulasan', 'Terbaru', 'Harga Tertinggi', 'Harga Terendah'])
                    info = 0
                    total_page = ''
                    if keyword:
                        total_page = ''
                        for key in keyword:
                            
                            info = TokpedKeys(Search=key).get_keys_products(sort_val=res_filter(filter_by), pages=1, info=True)
                            
                            total_page = total_page + '%s : %s\n'%(key, info)
                    pages = st.text_input('Max pages to be crawled', placeholder='Number only')
                    start_crawl = st.button('Scrape Website')
                    st.markdown("<h4 style='text-align: center; color: red;'> Single page contain 60 products </h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                                ```
                                {total_page}
                                """)

                else:
                    shopLink = st.text_input('Shop link address', placeholder='URL')
                    st.text_input('Max pages to be crawled', placeholder='Number only', key='page_awal')
                    filter_by = st.selectbox('Sort By : ', ['Paling Sesuai', 'Terbaru', 'Harga Tertinggi',
                        'Harga Terendah', 'Ulasan Terbanyak', 'Pembelian Terbanyak',
                        'Dilihat Terbanyak', 'Pembaruan Terakhir'])
                    
                    shopInfo = st.button('Show Shop Information')
                    
                    if shopInfo and shopLink:
                        name, loc, prCount, prSold, tx = Tokopedia(Search=shopLink).get_shop_products(info=True)
                        st.text_input('Possible pages to be crawled', placeholder='Max : {}'.format(ceil(int(prCount) / 80)), key='page', on_change=update_pages)
                        
                        
                        print('step 1 : ', st.session_state.page)
                        print('side 1 : ', filter_by)
                        if filter_by == 'Terbaru':
                            filter_by = '2'
                            print('side 2 : ', filter_by)
                    start_scraping = st.button('Scrape Website')
                    st.markdown("<h4 style='text-align: center; color: red;'> Please notes that scraping with shop address will get single page by default (80 Products) </h4>", unsafe_allow_html=True)
            # =====================================================================================================================================
            # =====================================================================================================================================
            # =====================================================================================================================================
            else:
                if option2 == 'Keyword':

                    keyword = st.text_area('Input Keyword(s)', placeholder='Seperate word by new line')
                    keyword = keyword.split('\n')
                    keyword = [x for x in keyword if x != '']
                    filter_by = st.selectbox('Sort By : ', ['Terkait', 'Terbaru', 'Terlaris', 'Termurah', 'Sales', 'Termahal'])
                    info = 0
                    total_page = ''
                    if keyword:
                        total_page = ''
                        for key in keyword:
                            info = Shopee(Search=key).global_search(sort_by_key=filter_by, info=True)
                            total_page = total_page + '%s : %s\n'%(key, info)
                    pages = st.text_input('Max pages to be crawled', placeholder='Number only')
                    start_crawl = st.button('Scrape Website')
                    st.markdown("<h4 style='text-align: center; color: red;'> Single page contain 60 products </h4>", unsafe_allow_html=True)
                    st.markdown(f"""
                                ```
                                {total_page}
                                """)

                else:
                    shopLink = st.text_input('Shop link address', placeholder='URL')
                    keyword = st.text_area('Input Keyword(s)', placeholder='Seperate word by new line')
                    keyword = keyword.split('\n')
                    keyword = [x for x in keyword if x != '']
                    pages = st.text_input('Max pages to be crawled', placeholder='Number only', key='page_awal')
                    filter_by = st.selectbox('Sort By : ', ['Terkait', 'Terbaru', 'Terlaris', 'Termurah', 'Sales', 'Termahal'])
                    
                    shopInfo = False

                    if shopLink:
                        total_data  = store_all_search(shopLink, 1, filter_by, info=True)
                        st.markdown(f"""
                                ```
                                total page : {total_data}
                                """)
                    #     name, loc, prCount, prSold, tx = Tokopedia(Search=shopLink).get_shop_products(info=True)
                    #     st.text_input('Possible pages to be crawled', placeholder='Max : {}'.format(ceil(int(prCount) / 80)), key='page', on_change=update_pages)
                        
                    start_scraping = st.button('Scrape Website')
                    st.markdown("<h4 style='text-align: center; color: red;'> Please notes that scraping with shop address will get single page by default (30 products) </h4>", unsafe_allow_html=True)


        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            image = Image.open('logo/images.png')

            st.image(image)

        with col3:
            st.write(' ')

        with st.expander("Spider Bot Details"):
            st.markdown("<h1 style='text-align: center;'> SHOPEDIA SPIDER </h1>", unsafe_allow_html=True)
            st.write("""
                    **ver 0.1**
                    
                    --------------------------------
                    
                    - [x] Version 0.5
                    - [x] Development phase
                    - [x] Testing Phase
                    - [x] Production V1.0
                    
                    |Website(supported) | Features |
                    | ----------- | ----------- |
                    |Tokopedia          | Keyword Search , By Store| 
                    |Shopee          | Keyword Search, By Store|
                    
                    --------------------------------------------------------

                    """)


        if option2 == 'Keyword':
            if start_crawl:
                now = datetime.now()
                current_time = now.strftime("%d %B, %Y at %I_%M %p")
                if option == 'Tokopedia':
                    for key in keyword:
                        temp = TokpedKeys(Search=key).get_keys_products(sort_val=res_filter(filter_by), pages=int(pages))
                        temp = process_data(temp)
                        temp.to_csv('Data-Tokopedia/%s - Tokopedia - %s.csv' %(current_time, key), index=False, sep=';')
                else:
                    for key in keyword:
                        
                        temp = Shopee(Search=key).global_search(sort_by_key=filter_by, max_page=int(pages))
                        temp.to_csv('Data-Shopee/%s - Shopee - %s.csv' %(current_time, key), index=False, sep=';')

            with st.container():
                show_dataset()
            
            
                    
        if option2 == 'Shop Link':
            if shopInfo and shopLink:
                with st.expander('Shop Details'):
                        
                        st.markdown(f"""
                                    Shop Info : 

                                    ------------------------

                                    - Name : {name}
                                    - Location : {loc}
                                    - Total Products : {prCount}
                                    - Products Sold : {prSold}
                                    - Transaction Success : {tx}
                                    
                                    """)

            if start_scraping:
                if option == "Tokopedia":

                    try :
                        if st.session_state.page_awal:
                            now = datetime.now()
                            current_time = now.strftime("%d %B, %Y at %I_%M %p")
                            print("YOOOOOOO")
                            isSuccess = True
                            df = Tokopedia(Search=shopLink).get_shop_products(page=1, sort=sort_by(filter_by))
                            df.to_csv('Data-Tokopedia/%s - Tokopedia.csv' %(current_time), index=False, sep=';')
                        else:
                            now = datetime.now()
                            current_time = now.strftime("%d %B, %Y at %I_%M %p")
                            isSuccess = True
                            df = Tokopedia(Search=shopLink).get_shop_products(page=1, sort=sort_by(filter_by))
                            df.to_csv('Data-Tokopedia/%s -  Tokopedia.csv' %(current_time), index=False, sep=';')
                    except:
                        st.error('Please input Shop link address')
                        isSuccess = False
                else:
                    if keyword:
                        now = datetime.now()
                        current_time = now.strftime("%d %B, %Y at %I_%M %p")
                        for key in keyword:

                            temp = store_search(shopLink, key, int(pages), filter_by)
                            print(temp)
                            temp.to_csv('Data-Shopee/%s - Shopee - %s.csv' %(current_time, key), index=False, sep=';')
                    else:
                        now = datetime.now()
                        current_time = now.strftime("%d %B, %Y at %I_%M %p")
                        df = store_all_search(shopLink, int(pages), filter_by)
                        df.to_csv('Data-Shopee/%s - Shopee.csv' %(current_time), index=False, sep=';')

                    
                # with st.expander('Result Details'):
                        
                #         st.markdown(f"""
                #                     Parameters : 

                #                     ------------------------
                #                     - Url : {shopLink}
                #                     - Filter By : {filter_by}
                #                     - Scraped Pages : {st.session_state.page_awal}
                                    
                #                     """)
                # if isSuccess:
                #     st.write('**Result**', df)

            with st.container():
                show_dataset()


if __name__ == '__main__':
    main()



