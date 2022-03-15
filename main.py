from math import ceil
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


def main():
    st.set_page_config(page_title="Spider Scraper", layout='wide')
    names            = ['team merch','team exa']
    usernames        = ['merch','exa']
    hashed_passwords = ["$2b$12$HwAdj.1ql8/ftD8LSzCqReE5jWKXNK7R2AJf5p/hfvqKwctS/v1fe",
                        "$2b$12$SgSFaxyEXOeVhUY7iJdsUe3ivc5KSQgWmtM9z98e1qhfsaPJRHmlK"]
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


    def update_pages():
        st.session_state.page_awal = st.session_state.page

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
        src = st.selectbox('Data Source', ['Tokopedia', 'Shopee'])
        if src == 'Tokopedia':
            folder = os.listdir('Data-Tokopedia/')
            folder.sort(reverse=True)
            if folder:
                res = st.selectbox('Dataset', folder)
                df  =  pd.read_excel('Data-Tokopedia/'+ res)
                st.write('***Result**' , df)

                data = df.to_csv().encode('utf-8')
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
                        time.sleep(1)
		
            else:
                st.warning("No datasets found")
        else:
            folder = os.listdir('Data-Shopee/')
            folder.sort(reverse=True)
            if folder:
                res = st.selectbox('Dataset', folder)
                df  =  pd.read_excel('Data-Shopee/'+ res)
                st.write('***Result**' , df)

                data = df.to_csv().encode('utf-8')
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

    if authentication_status:
        
        with st.sidebar:
            
            st.markdown("<h1 style='text-align: center;'> EXA x MERCH </h1>", unsafe_allow_html=True)
            option = st.selectbox('Target Website', ['Tokopedia', 'Shopee'])
            option2 = st.selectbox('Crawl by: ', ['Keyword', 'Shop Link'])
            if option == 'Tokopedia':
                    
                if option2 == 'Keyword':

                    keyword = st.text_area('Input Keyword(s)', placeholder='Seperate word by new line')
                    keyword = keyword.split('\n')
                    keyword = [x for x in keyword if x != '']
                    filter_by = st.selectbox('Filter By : ', ['Paling Sesuai', 'Ulasan', 'Terbaru', 'Harga Tertinggi', 'Harga Terendah'])
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
                    filter_by = st.selectbox('Filter By : ', ['Paling Sesuai', 'Terbaru', 'Harga Tertinggi',
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
                    st.markdown("<h4 style='text-align: center; color: red;'> Please notes that scraping with shop address will get single page by default </h4>", unsafe_allow_html=True)
            # =====================================================================================================================================
            # =====================================================================================================================================
            # =====================================================================================================================================
            else:
                if option2 == 'Keyword':

                    keyword = st.text_area('Input Keyword(s)', placeholder='Seperate word by new line')
                    keyword = keyword.split('\n')
                    keyword = [x for x in keyword if x != '']
                    filter_by = st.selectbox('Filter By : ', ['Terkait', 'Terbaru', 'Terlaris', 'Termurah', 'Sales', 'Termahal'])
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
                    filter_by = st.selectbox('Filter By : ', ['Terkait', 'Terbaru', 'Terlaris', 'Termurah', 'Sales', 'Termahal'])
                    
                    shopInfo = st.button('Show Shop Information')
                    
                    # if shopLink:
                        # name, loc, prCount, prSold, tx = Tokopedia(Search=shopLink).get_shop_products(info=True)
                        # st.text_input('Possible pages to be crawled', placeholder='Max : {}'.format(ceil(int(prCount) / 80)), key='page', on_change=update_pages)
                        
                    start_scraping = st.button('Scrape Website')
                    st.markdown("<h4 style='text-align: center; color: red;'> Please notes that scraping with shop address will get single page by default </h4>", unsafe_allow_html=True)


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
                    - [x] Development phase (Current)
                    - [ ] Testing Phase
                    
                    |Website(supported) | Features |
                    | ----------- | ----------- |
                    |Tokopedia          | Keyword Search , By Store| 
                    |Shopee          | Keyword Search, By Store|
                    
                    --------------------------------------------------------

                    """)


        if option2 == 'Keyword':
            if start_crawl:
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d-%H-%M")
                if option == 'Tokopedia':
                    for key in keyword:
                        temp = TokpedKeys(Search=key).get_keys_products(sort_val=res_filter(filter_by), pages=int(pages))
                        temp.to_excel('Data-Tokopedia//%s - Tokopedia - %s.xlsx' %(current_time, key), index=False)
                else:
                    for key in keyword:
                        
                        temp = Shopee(Search=key).global_search(sort_by_key=filter_by, max_page=int(pages))
                        temp.to_excel('Data-Shopee/%s - Shopee - %s.xlsx' %(current_time, key), index=False)

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
                            current_time = now.strftime("%Y-%m-%d-%H-%M")
                            print("YOOOOOOO")
                            isSuccess = True
                            df = Tokopedia(Search=shopLink).get_shop_products(page=1, sort=sort_by(filter_by))
                            df.to_excel('Data-Tokopedia/%s - Tokopedia.xlsx' %(current_time), index=False)
                        else:
                            now = datetime.now()
                            current_time = now.strftime("%Y-%m-%d-%H-%M")
                            isSuccess = True
                            df = Tokopedia(Search=shopLink).get_shop_products(page=1, sort=sort_by(filter_by))
                            df.to_excel('Data-Tokopedia/%s -  Tokopedia.xlsx' %(current_time), index=False)
                    except:
                        st.error('Please input Shop link address')
                        isSuccess = False
                else:
                    if keyword:
                        now = datetime.now()
                        current_time = now.strftime("%Y-%m-%d-%H-%M")
                        for key in keyword:

                            temp = store_search(shopLink, key, int(pages), filter_by)
                            temp.to_excel('Data-Shopee/%s - Shopee - %s.xlsx' %(current_time, key), index=False)
                    else:
                        now = datetime.now()
                        current_time = now.strftime("%Y-%m-%d-%H-%M")
                        df = store_all_search(shopLink, int(pages), filter_by)
                        df.to_excel('Data-Shopee/%s - Shopee.xlsx' %(current_time), index=False)

                    
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



