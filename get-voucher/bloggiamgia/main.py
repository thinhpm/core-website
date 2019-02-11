import requests
from lxml import html
import re

id_deep_link = '2323'


def process_deep_link(string_link):
    if 'lazada' in string_link:
        return ''

    id = re.findall(r'deep_link/(.*?)\?url', string_link)[0]
    return string_link.replace(id, id_deep_link).replace('BGG_COUPON', 'MGGHOT_COUPON')


if __name__ == "__main__":
    url = "https://bloggiamgia.vn/ma-giam-gia/shopee/"
    re2 = requests.get(url)
    root = html.fromstring(re2.content)

    category = root.xpath('//h2[@class="wpsm_toplist_heading"]')

    for item_cate in category:
        name_cate = item_cate.xpath('span/strong/text()')[0]
        t = item_cate.xpath('following-sibling::div[@class="clearfix"][1]')[0]
        item = t.xpath('div/div[@class="offers-details"]')
        print(name_cate)
        for i in item:
            id_coupon = i.xpath('div/div/div/div[2]/div/a/@id')[0]
            is_voucher = 'pull-right' not in i.xpath('div/div/div/div[2]/div/a/@class')[0]
            percent = i.xpath('div/div/div/div/div/div[3]/text()')[0].strip()
            description = i.xpath('div/div/div/div/div/div[4]/span/text()')[0]
            date_exp = i.xpath('div/div/div/div/div/div[4]/div/div[2]/span/span/text()')[0]
            code = i.xpath('div/div/div/div[2]/div/a/div/span/text()')[0].strip()

            if is_voucher:
                string_link = i.xpath('div/div/div/div[2]/div/a/@onclick')[0]
            else:
                string_link = i.xpath('div/div/div/div[2]/div/a/@href')[0]

            string_link = process_deep_link(string_link)

            print(id_coupon)
            print(is_voucher)
            print(percent.strip())
            print(description)
            print(date_exp)
            print(code.strip())
            print(string_link)
            # break
        # break