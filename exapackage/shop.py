from numpy import NaN
import json
import requests as req
import pandas as pd
from stqdm import stqdm

class Tokopedia:
    
    def __init__(self, Search = "https://www.tokopedia.com/lg-official") :
        self.SHOPLINK = Search.split('https://www.tokopedia.com/')[1]
        print(self.SHOPLINK)
        self.ENDPOINT = "https://gql.tokopedia.com/"
        self.PAYLOAD  = {
    "operationName": "ShopInfoCore",
    "variables": {
      "id": 0,
      "domain": self.SHOPLINK
    },
    "query": "query ShopInfoCore($id: Int!, $domain: String) {\n  shopInfoByID(input: {shopIDs: [$id], fields: [\"active_product\", \"address\", \"allow_manage_all\", \"assets\", \"core\", \"closed_info\", \"create_info\", \"favorite\", \"location\", \"status\", \"is_open\", \"other-goldos\", \"shipment\", \"shopstats\", \"shop-snippet\", \"other-shiploc\", \"shopHomeType\", \"branch-link\"], domain: $domain, source: \"shoppage\"}) {\n    result {\n      shopCore {\n        description\n        domain\n        shopID\n        name\n        tagLine\n        defaultSort\n        __typename\n      }\n      createInfo {\n        openSince\n        __typename\n      }\n      favoriteData {\n        totalFavorite\n        alreadyFavorited\n        __typename\n      }\n      activeProduct\n      shopAssets {\n        avatar\n        cover\n        __typename\n      }\n      location\n      isAllowManage\n      branchLinkDomain\n      isOpen\n      address {\n        name\n        id\n        email\n        phone\n        area\n        districtName\n        __typename\n      }\n      shipmentInfo {\n        isAvailable\n        image\n        name\n        product {\n          isAvailable\n          productName\n          uiHidden\n          __typename\n        }\n        __typename\n      }\n      shippingLoc {\n        districtName\n        cityName\n        __typename\n      }\n      shopStats {\n        productSold\n        totalTxSuccess\n        totalShowcase\n        __typename\n      }\n      statusInfo {\n        shopStatus\n        statusMessage\n        statusTitle\n        __typename\n      }\n      closedInfo {\n        closedNote\n        until\n        reason\n        detail {\n          status\n          __typename\n        }\n        __typename\n      }\n      bbInfo {\n        bbName\n        bbDesc\n        bbNameEN\n        bbDescEN\n        __typename\n      }\n      goldOS {\n        isGold\n        isGoldBadge\n        isOfficial\n        badge\n        shopTier\n        __typename\n      }\n      shopSnippetURL\n      customSEO {\n        title\n        description\n        bottomContent\n        __typename\n      }\n      __typename\n    }\n    error {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
  }
    
    def get_shop_products(self, page=None, sort=2, info=False):
        
        
      request_products = json.loads(req.post(self.ENDPOINT, json = self.PAYLOAD).content)
      

      shopID = request_products['data']['shopInfoByID']['result'][0]['shopCore']['shopID']
      shopName = request_products['data']['shopInfoByID']['result'][0]['shopCore']['name']
      shopLoc = request_products['data']['shopInfoByID']['result'][0]['location']
      productsCount = request_products['data']['shopInfoByID']['result'][0]['activeProduct']
      productSold = request_products['data']['shopInfoByID']['result'][0]['shopStats']['productSold']
      totalTX = request_products['data']['shopInfoByID']['result'][0]['shopStats']['totalTxSuccess']

      if info == True:
          return shopName, shopLoc, productsCount, productSold, totalTX
      
      # print(json.dumps(request_products, indent=4))
        
    
      def getShopProduct(shopID, loc, name, page=1):

        sid = str(shopID)
        prod_json = {
                      "operationName": "ShopProducts",
                      "variables": {
                        "sid": sid,
                        "page": page,
                        "perPage": 80,
                        "etalaseId": "etalase",
                        "sort": sort,
                        "user_districtId": "",
                        "user_cityId": "",
                        "user_lat": "",
                        "user_long": ""
                      },
                      "query": "query ShopProducts($sid: String!, $page: Int, $perPage: Int, $keyword: String, $etalaseId: String, $sort: Int, $user_districtId: String, $user_cityId: String, $user_lat: String, $user_long: String) {\n  GetShopProduct(shopID: $sid, filter: {page: $page, perPage: $perPage, fkeyword: $keyword, fmenu: $etalaseId, sort: $sort, user_districtId: $user_districtId, user_cityId: $user_cityId, user_lat: $user_lat, user_long: $user_long}) {\n    status\n    errors\n    links {\n      prev\n      next\n      __typename\n    }\n    data {\n      name\n      product_url\n      product_id\n      price {\n        text_idr\n        __typename\n      }\n      primary_image {\n        original\n        thumbnail\n        resize300\n        __typename\n      }\n      flags {\n        isSold\n        isPreorder\n        isWholesale\n        isWishlist\n        __typename\n      }\n      campaign {\n        discounted_percentage\n        original_price_fmt\n        start_date\n        end_date\n        __typename\n      }\n      label {\n        color_hex\n        content\n        __typename\n      }\n      label_groups {\n        position\n        title\n        type\n        url\n        __typename\n      }\n      badge {\n        title\n        image_url\n        __typename\n      }\n      stats {\n        reviewCount\n        rating\n        __typename\n      }\n      category {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
                    }

        request_products = json.loads(req.post(self.ENDPOINT, json = prod_json).content)

        prod_total = len(request_products['data']['GetShopProduct']['data'])

        all_products = []
        for idx_prod in range(prod_total):
          try:
            qty = request_products['data']['GetShopProduct']['data'][idx_prod]['label_groups'][0]['title']
          except IndexError:
            qty = NaN


          products = {
            'Shop Name' : name,
            'Shop Location' : loc,
            'Product Name' : request_products['data']['GetShopProduct']['data'][idx_prod]['name'],
            'ID' : request_products['data']['GetShopProduct']['data'][idx_prod]['product_id'],
            'Qty Sold' : qty,
            'Final Price' : request_products['data']['GetShopProduct']['data'][idx_prod]['price']['text_idr'],
            'Disc Value in Percent' : request_products['data']['GetShopProduct']['data'][idx_prod]['campaign']['discounted_percentage'],
            'Original Price' : request_products['data']['GetShopProduct']['data'][idx_prod]['campaign']['original_price_fmt'],
            'Rating' : request_products['data']['GetShopProduct']['data'][idx_prod]['stats']['rating'],
            'Reviewed' : request_products['data']['GetShopProduct']['data'][idx_prod]['stats']['reviewCount'],
            'Product URL'       : request_products['data']['GetShopProduct']['data'][idx_prod]['product_url'],
            'Badge'       : request_products['data']['GetShopProduct']['data'][idx_prod]['badge'][0]['title']

            }
          
          all_products.append(products)
        # print(len(request_products['data']['GetShopProduct']['data']))
        # print(json.dumps(request_products['data']['GetShopProduct']['data'],  indent=4))
        # print(len(request_products['data']['GetShopProduct']['data']))
        # print(json.dumps(request_products, indent=4))
        return pd.DataFrame(all_products)
      
      if page:
          df = pd.DataFrame()
          for halaman in stqdm(range(1, page + 1)):
              temp = getShopProduct(shopID,  shopLoc, shopName, halaman)
              df = pd.concat([df, temp], ignore_index=True)
      
          return df