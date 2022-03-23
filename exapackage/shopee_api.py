import string
import requests
import json 
import pandas as pd 
import math
from stqdm import stqdm
import streamlit as st

class ShopeeKeyword:

    def search_keywords(self, search: str, sort_key: str):
        def sort_keyword_by(val):
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
        
        limit_item_page = 60
        keywords        = search
        sort_by_key     = sort_keyword_by(sort_key)

        params = (
            ('by', sort_by_key['by']),
            ('keyword', keywords),
            ('limit', limit_item_page),
            ('newest', str(limit_item_page)),
            ('order', sort_by_key['order']),
            ('page_type', 'search'),
            ('scenario', 'PAGE_GLOBAL_SEARCH'),
            ('version', '2')
        )

        response = requests.get('https://shopee.co.id/api/v4/search/search_items', params=params)
        response.raise_for_status()
        headers = response.headers["content-type"].strip().startswith("application/json")
        if (response.status_code != 204 and headers):
            total_page = int(math.ceil(int(response['total_count']) / limit_item_page))
            return json.load(response.json()) , total_page
        
    def process_response(self, response: dict, max_page: int):

        if(response['total_count'] > 0):
            product_list = []
            for i in stqdm(range (max_page), desc="Scraping Shopee Page"):
                item_list = response['items']
                #CONSTRUCT ROW DATA
                for item in stqdm(item_list, desc="Loading data.."):
                    #GET DATA STORE
                    params_get_store = {
                        'shopid': item['item_basic']['shopid']
                    }
                    response_store = requests.get('https://shopee.co.id/api/v4/product/get_shop_info', params = params_get_store)
                    response_store.raise_for_status()
                    json_data_store = json.loads(response_store.json())
                    params_get_item_detail = (
                        ('itemid', item['item_basic']['itemid']),
                        ('shopid', item['item_basic']['shopid'])
                    )        
                    response_item_detail = requests.get('https://shopee.co.id/api/v4/item/get', params = params_get_item_detail)
                    response_item_detail.raise_for_status()
                    json_data_item_detail = json.loads(response_item_detail.json())
                    if(json_data_item_detail['data']['condition'] == 4):
                        is_used = 'yes'
                    else:
                        is_used = 'no'
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







