import os
import ssl
from requests_html import HTMLSession
import re
import json

from requests.adapters import HTTPAdapter

class TLSAdapter(HTTPAdapter):
    """A custom adapter to enforce TLS 1.2 and ignore certificate errors."""
    def init_poolmanager(self, *args, **kwargs):
        # Create an SSL context for TLS 1.2
        ssl_context = ssl.create_default_context()
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        # Disable certificate verification
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_context.verify_flags = ssl.CERT_NONE
        kwargs['ssl_context'] = ssl_context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


class Reviews:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.session = HTMLSession()
        # Mount the custom adapter to enforce TLS 1.2
        self.session.mount('https://', TLSAdapter())
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Cache-Control': 'max-age=0',
            'Device-Memory': '8',
            'Dnt': '1',
            'Downlink': '10',
            'Dpr': '1.25',
            'Ect': '4g',
            'Priority': 'u=0, i',
            'Rtt': '50',
            'Viewport-Width': '1920',
            'Sec-Ch-Device-Memory': '8',
            'Sec-Ch-Dpr': '1.25',
            'Sec-Ch-Ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'Sec-Ch-Ua-Mobile' : '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Ua-Platform-Version': '"19.0.0"',
            'Sec-Ch-Viewport-Width': '1920',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Cookie': 'session-id=131-9125800-9215568; ubid-main=135-1831962-8682202; lc-main=en_US; at-main=Atza|IwEBIGuxYz_Ei9YSVOaikkMIyzsBrioW2g3t_ymNbYMEQegyDttOpfYCO56n2mAM07_tkkA05SNTHS3ubCkIMjuZCYFEix1eHpn6-weoq1Gp_5_FY05kB8d_XsyX3JldSz0N4b7MxoSySHaxTLsMhmUKh4NQpFGp8eZ645X51gWXe19gLU-kERc0gjNHqeOUj0IAAI7WQgWGh8nfP83POKkQA8TJbH4M5F4aQebFVG9j7222aw; sess-at-main="h/Jt5FWnyYre9doU9iTjH5j9r2x42PPogvfv/uGyPD4="; sst-main=Sst1|PQHEbP6YnBwxsqTSF3cYKSAhCS7g90U3UWnCfDqgU3AimM4l32O6OqVIN6eelVmio0k9KRQJDXNG-x_y93Ho2ee22Hmb9fvl8yuEUSmjCwUC1w_MigkQUj5ETVwyX_LcMBGi17c7qkrYnn-1TUFGKsjS5TfvCYHKg-Qn3iUm_Vq1aOMyaP1txl8FmRK7m9qYK3wdASQu5QAWdoUAcnYlZtyk5TyfXdOrMxxjMUrvxu7edcAtTyEcKZI1mwECdWjLu2LM0mpuwGrCNvAKqR2L_oEshMF0p7BMawvtya7NhYV4-oE; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; session-token=hEG/4E0BsVOOu4IVyNew+R5eI5Nc1Mo5tFd5BKS8WkJWIrk6TIziGl/a2Di0FlYWhaMp5ETpIAuTxc2Mu73SvSrQKA3VTdCfBrMoAXtUVYO1Ci5tCCBEH5ftb8+b1l/a7YtKt0gls4ZW2WfT3NRsELLaLfKCXOYn7G9M+4vagFtXyLtft3IwBO6A/4AATsQtrbvZYF0C4ycP0ZzHGzAdD9IH23P915X3wCwcfDlks1RXvZTJUVFJuCOS+fbT642Pg5NGkeqLOlGscA/14p7w7up471JYHq2OkO5tIm3DMuNg+M5dZALlcB5AaSQPo/uRSXew6m2LQryMN2qsbLf3i5cf+W2ER33a4d37e6jjvtL/B4XC1tPID/NyGuyfiHid; x-main="P3PbVLlimjidF7NGDG@kJdlIK7kFzRFs48uSPzKM08e75LtPDfDMbzvGzee2bsY9"; sp-cdn="L5Z9:EG"; csm-hit=tb:YNQXQQPETQEQ9EY4FDTZ+s-513WA6VG9HT30RPBYQ10|1744993188371&t:1744993188371&adb:adblk_none'
            #'Cookie': 'lc-main=en_US;'
        }
        #self.session.headers.update(self.headers)
        self.session.keep_alive = True
        self.url = f'https://www.amazon.com/product-reviews/{self.asin}/ref=acr_dp_hist_5?ie=UTF8&reviewerType=all_reviews&pageNumber='
        self.productName = None
        
    def pagination(self, page: int):
        #r = self.session.get(self.url + str(page), headers=self.headers, proxies={ 'http' : 'http://localhost:8888', 'https' : 'http://localhost:8888' }, verify=False)
        r = self.session.get(self.url + str(page), headers=self.headers)
        reviews = r.html.find('li[data-hook=review]')
        if self.productName is None:
            productName = r.html.find('a[data-hook=product-link]', first=True)
            if productName:
                self.productName = productName.text
            else:
                self.productName = 'Unknown Product'
        if not reviews:
            return False
        else:
            return self.parse(reviews)
        
    def parse(self, reviews):

        total = []
        for review in reviews:
            reviewData = {}
            nameSpan = review.find('span.a-profile-name', first=True)
            if not nameSpan:
                continue
            reviewData['name'] = nameSpan.text
            dateSpan = review.find('span[data-hook=review-date]', first=True)
            if dateSpan:
                dateSpanText = dateSpan.text
                match = re.search(r"Reviewed in(?: the)? (.+?)(?= on) on (.+)", dateSpanText)
                if match:
                    reviewData['location'] = match.group(1)  # Group 1: Location
                    reviewData['date'] = match.group(2)      # Group 2: Date

            verified = review.find('span[data-hook=avp-badge]', first=True)
            if verified:
                reviewData['verified-purchase'] = True
            else:
                reviewData['verified-purchase'] = False

            reviewBodyText = review.find('span[data-hook=review-body]', first=True)
            if not reviewBodyText:
                continue
            reviewData['review-body'] = reviewBodyText.text
            ratingI = review.find('i[data-hook=review-star-rating]', first=True)
            if not ratingI:
                continue
            ratingText = ratingI.text
            ratingMatch = re.search(r'(\d+(?:\.\d+)?) out of 5 stars', ratingText)
            if ratingMatch:
                reviewData['rating'] = float(ratingMatch.group(1))
            else:
                continue
                
            total.append(reviewData)
        return total
    def getAllReviews(self):
        page = 1
        allReviews = []
        while True:
            reviews = self.pagination(page)
            if not reviews:
                break
            allReviews.extend(reviews)
            page += 1
        return allReviews


def getReviews(asin):
    file_path = f'data/{asin}.json'
    if os.path.exists(file_path):
        return
    
    if not os.path.exists('data'):
        os.makedirs('data')
    reviews = Reviews(asin)
    result = reviews.getAllReviews()
    productData = {
        'asin': asin,
        'productName': reviews.productName,
        'reviews': result
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(productData, f, ensure_ascii=False, indent=4)


products = ['B0DP3FP5P3', 'B0CRHZZLYR', 'B0DHKHXMQH', 'B0BJLCWFNM', 'B0DSSBWLYM', 'B0D897WH4K', 'B0DCJPKQ8S']


for product in products:
    getReviews(product)
    print(f'Finished {product}')