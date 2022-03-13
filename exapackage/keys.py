from numpy import NaN
import json
import requests as req
import pandas as pd
from stqdm import stqdm
import streamlit as st

class Tokopedia:
    
    def __init__(self, Search) :
        self.keyword  = Search
        self.PARAMS   = f'device=desktop&navsource=home&ob=23&page=1&q={Search}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&st=product&start=0&topads_bucket=true&unique_id=c2df653a61e4087d4e74823c68513669&user_addressId=&user_cityId=&user_districtId=&user_id=&user_lat=&user_long=&user_postCode=&variants='
        self.ENDPOINT = "https://gql.tokopedia.com/"
        self.PAYLOAD  =  {
            
            'operationName': 'SearchProductQueryV4',
            
            'variables': 
                {'params': 
                
                    self.PARAMS
              
                },
              ''
            'query': "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    
    def get_keys_products(self, sort_val, pages, info=False):

        
      
      request_products = json.loads(req.post(self.ENDPOINT, json = self.PAYLOAD, timeout=5).content)
      

      totalProducts = request_products['data']['ace_search_product_v4']['header']['totalDataText']

      if info == True:
          return totalProducts
        
    
      def getShopProduct(page):
        new_params   = f'device=desktop&navsource=home&ob={sort_val}&page={page}&q={self.keyword}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&st=product&start=0&topads_bucket=true&unique_id=c2df653a61e4087d4e74823c68513669&user_addressId=&user_cityId=&user_districtId=&user_id=&user_lat=&user_long=&user_postCode=&variants='
        custom_json =  {
            
            'operationName': 'SearchProductQueryV4',
            
            'variables': 
                {'params': 
                
                    new_params
                
                },
              ''
            'query': "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

        respon   = json.loads(req.post(self.ENDPOINT, json = custom_json).content)
        data_len = len(respon['data']['ace_search_product_v4']['data']['products'])

        all_prods = []
        for idx_prod in range(data_len):
          name = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['name']
          id = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['id']
          try:
            badge = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['badges'][0]['title']
          except:
            badge = NaN

          rev_count = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['countReview']
          discPercent = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['discountPercentage']
          try:
            sold = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['labelGroups'][-1]['title']
            if 'Terjual' not in sold:
		sold = NaN
          except:
            sold = NaN
          original_price = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['originalPrice']
          final_price = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['price']
          avg_rating = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['ratingAverage']
          seller = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['shop']['name']
          seller_id = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['shop']['shopId']
          seller_city = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['shop']['city']
          seller_url = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['shop']['url']
          prod_url = respon['data']['ace_search_product_v4']['data']['products'][idx_prod]['url']

          data = {

            'Name': name,
            'ID': id,
            'Badge': badge,
            'Reviewed': rev_count,
            'Disc Percent': discPercent,
            'Qty Sold': sold,
            'Original Price': original_price,
            'Final Price': final_price,
            'Avg Rating': avg_rating,
            'Prod URL': prod_url,
            'Shop Name': seller,
            'Shop ID': seller_id,
            'Shop City': seller_city,
            'Shop URL': seller_url,

            }
          
          all_prods.append(data, ignore_index=True)
        
        return pd.DataFrame(all_prods)
      

      if pages:
          df = pd.DataFrame()
          for halaman in stqdm(range(1, pages + 1)):
              temp = getShopProduct(halaman)
              df = pd.concat([df, temp], ignore_index=True)
      
          return df

          
