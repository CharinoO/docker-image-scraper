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
                        total_data, json_data  = ShopeeItemAll().store_all_search(shopLink, filter_by)
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
                            df.to_csv('Data-Tokopedia/%s - Tokopedia-%s.csv' %(current_time,  shopLink.split('/')[-1]), index=False, sep=';')
                        else:
                            now = datetime.now()
                            current_time = now.strftime("%d %B, %Y at %I_%M %p")
                            isSuccess = True
                            df = Tokopedia(Search=shopLink).get_shop_products(page=1, sort=sort_by(filter_by))
                            df.to_csv('Data-Tokopedia/%s -  Tokopedia-%s.csv' %(current_time, shopLink.split('/')[-1]), index=False, sep=';')
                    except:
                        st.error('Please input Shop link address')
                        isSuccess = False
                else:
                    if keyword:
                        now = datetime.now()
                        current_time = now.strftime("%d %B, %Y at %I_%M %p")
                        for key in keyword:

                            temp = ShopeeItem().process_json(json_data, int(pages), key)
                            print(temp)
                            temp.to_csv('Data-Shopee/%s - Shopee - %s.csv' %(current_time, key), index=False, sep=';')
                    else:
                        now = datetime.now()
                        current_time = now.strftime("%d %B, %Y at %I_%M %p")
                        df = ShopeeItemAll().process_json(json_data, int(pages), filter_by)
                        df.to_csv('Data-Shopee/%s - Shopee-%s.csv' %(current_time,  shopLink.split('/')[-1]), index=False, sep=';')

                    
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