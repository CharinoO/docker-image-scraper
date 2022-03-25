import requests
from datetime import datetime, timedelta
import json 
import pandas as pd 
import math
from stqdm import stqdm

#PILIHAN SORT BY : 'terkait', 'terbaru', 'terlaris', 'termurah', 'termahal'
def search_sort_by(val):
    if(val.lower() == 'terkait'):
        return { "by" : "relevancy", "order" : "desc" }
    if(val.lower() == 'terbaru'):
        return { "by" : "ctime", "order" : "desc" }
    if(val.lower() == 'terlaris'):
        return { "by" : "sales", "order" : "desc" }
    if(val.lower() == 'termurah'):
        return { "by" : "price", "order" : "asc" }
    if(val.lower() == 'termahal'):
        return { "by" : "price", "order" : "desc" }

#GET SHOP ID FROM INPUT LINK
def store_search(store_url_link, keyword, max_page, sort_by_val, info=False):
    print('Input shopee store url link with this format (https://shopee.co.id/storenameexample): ')
    # store_url_link = input()
    domain = 'shopee.co.id/'
    pos = store_url_link.find(domain) + len(domain)
    store_username_input = store_url_link[pos:]
    # print(store_url_link)
    params_store_detail = (
        ('sort_sold_out', 0),
        ('username', store_username_input),
    )
    response_store_detail = requests.get('https://shopee.co.id/api/v4/shop/get_shop_detail', params = params_store_detail)
    json_data_store_detail = json.loads(response_store_detail.text)
    target_shop_id = json_data_store_detail['data']['shopid']

    #NORMAL SHOPEE SEARCH FLOW                

    sort_by_key = search_sort_by(sort_by_val)
    limit_item_page = 60

    try:   
        #MENENTUKAN TOTAL PAGE DARI SEARCH RESULT
        params = (
            ('by', sort_by_key['by']),
            ('keyword', keyword),
            ('limit', limit_item_page),
            ('newest', str(limit_item_page)),
            ('order', sort_by_key['order']),
            ('page_type', 'shop'),
            ('pdp_l3cat', 100226),
            ('scenario', 'PAGE_SHOP_SEARCH'),
            ('version', '2'),
            ('entry_point', 'ShopBySearch'),
            ('match_id', str(target_shop_id)),
        )
        response = requests.get('https://shopee.co.id/api/v4/search/search_items', params=params)
        json_data = json.loads(response.text)
    
        #SET MAXIMUM TOTAL PAGE CRAWL
        if(json_data['total_count'] > 0):
            total_data = json_data['total_count']
            page_count = int(math.ceil(int(json_data['total_count']) / limit_item_page))
            if info:
                return total_data
            if(page_count > 5):
                page_count = 5
            print('total page: ' + str(page_count))
            #MELAKUKAN PENARIKAN DATA PER PAGE DI LOOPING
            product_list = []
            for i in stqdm(range (max_page)):
                print('pulling data from page-' + str(i+1) +'...')
                params = (
                    ('by', 'relevancy'),
                    ('keyword', keyword),
                    ('limit', limit_item_page),
                    ('newest', str(i * limit_item_page)),
                    ('order', 'desc'),
                    ('page_type', 'search'),
                    ('scenario', 'PAGE_GLOBAL_SEARCH'),
                    ('version', '2')
                )
                response = requests.get('https://shopee.co.id/api/v4/search/search_items', params=params)
                json_data = json.loads(response.text)
                item_list = json_data['items']

                params_get_store = {
                    'shopid': item[0]['item_basic']['shopid']
                }
                response_store = requests.get('https://shopee.co.id/api/v4/product/get_shop_info', params = params_get_store)
                json_data_store = json.loads(response_store.text)
                #CONSTRUCT ROW DATA
                for item in item_list:
                    #GET DATA STORE
                    
                    params_get_item_detail = (
                        ('itemid', item['item_basic']['itemid']),
                        ('shopid', item['item_basic']['shopid'])
                    )        
                    response_item_detail = requests.get('https://shopee.co.id/api/v4/item/get', params = params_get_item_detail)
                    json_data_item_detail = json.loads(response_item_detail.text)
                    if(json_data_item_detail['data']['condition'] == 4):
                        is_used = 'yes'
                    else:
                        is_used = 'no'
                    #SHOPEE STAR SELLER : is_shopee_verified = true
                    #SHOPEE STAR+ SELLER : is_shopee_verified = true and is_preferred_plus_seller = true
                    #SHOPEE MALL : is_official_shop = true
                    product = {
                    'name' : item['item_basic']['name'],
                    'is_official_shop' : json_data_store['data']['is_official_shop'],
                    'is_preferred_plus_seller' : json_data_store['data']['is_preferred_plus_seller'],
                    'is_shopee_verified' : json_data_store['data']['is_shopee_verified'],
                    'shop_name' :json_data_store['data']['account']['username'],
                    'price' : int(item['item_basic']['price'] / 100000),
                    'price_min' : int(item['item_basic']['price_min'] / 100000),
                    'price_max' : int(item['item_basic']['price_max'] / 100000),
                    'is_ads' :json.loads(item['search_item_tracking'])['is_ads'],
                    'loc' : item['item_basic']['shop_location'],
                    'qty_sold' : item['item_basic']['historical_sold'],
                    'is_used' : is_used,
                    'liked_count' : item['item_basic']['liked_count'],
                    'detail_url': 'https://shopee.co.id/' + (item['item_basic']['name']).replace(' ', '-') + '-i.'+str(item['item_basic']['shopid']) + '.' + str(item['item_basic']['itemid'])
                    }
                    product_list.append(product)
            df_item_list = pd.DataFrame.from_records(product_list)

            return df_item_list.reset_index(drop=True)
        else:
            print('search result not found')
    except Exception as e:
        print('there is a problem when pulling data')
        print('error code :' + str(e))
