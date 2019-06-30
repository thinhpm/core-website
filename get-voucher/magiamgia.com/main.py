import requests
from lxml import html
import re
import datetime

id_deep_link = '4945784097639239041'


def process_deep_link(string_link):
    if 'lazada' in string_link:
        return ''

    id = re.findall(r'deep_link/(.*?)\?url', string_link)[0]

    return string_link.replace(id, id_deep_link).replace('BGG_COUPON', 'MGGHOT_COUPON')


def get_code(string_link):
    code = re.findall(r'&sub_id1=(.*?)&sub_id2', string_link)[0]

    return code


def get_link_aff(string_link):
    link_aff = re.findall(r'window\.open\(\'(.*?)\'\)', string_link)[0]

    return link_aff


def get_date(date_exp):
    list_number = [int(s) for s in date_exp.split() if s.isdigit()]

    if len(list_number) == 0:
        if date_exp == 'Còn hiệu lực':
            return date_exp

        return 'Hết hạn'

    date_exp = list_number[0]
    today = datetime.date.today()
    date_1 = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    end_date = date_1 + datetime.timedelta(days=date_exp)

    end_date = "{:%d/%m/%Y}".format(end_date)

    return end_date


def handle_item(item, results):
    for i in range(len(item) - 1):
        if (len(item[i].xpath('*')) == 0):
            print(item[i])
            # result = []
            # id_coupon = ''
            # is_voucher = "LẤY MÃ" in item[i].xpath('div/div[3]/a/span[1]/text()')[1]
            # percent = item[i].xpath('div/div[1]/div/span[2]/text()')[0].strip()
            # description = item[i].xpath('div/div[2]/h5/text()')[0]
            # date_exp = item[i].xpath('div/div[2]/p[1]/text()')[0].strip() + '/2019'
            # code = item[i].xpath('div/div[3]/a/span[2]/text()')[0].strip()
            # link_aff = ''
            #
            # if is_voucher:
            #     # link_aff = i.xpath('div/div/div/div[2]/div/a/@onclick')[0]
            #     # code = get_code(link_aff)
            #     # link_aff = get_link_aff(link_aff)
            #     is_voucher = 1
            # else:
            #     # link_aff = i.xpath('div/div/div/div[2]/div/a/@href')[0]
            #     is_voucher = 0
            #
            # # link_aff = process_deep_link(link_aff)
            #
            # # date_exp = get_date(date_exp)
            #
            # result.append({
            #     'id_coupon': id_coupon,
            #     'is_voucher': is_voucher,
            #     'percent': percent.strip(),
            #     'description': description,
            #     'name': description,
            #     'date_exp': date_exp,
            #     'code': code.strip(),
            #     'link_aff': link_aff,
            #     'name_cate': name_cate,
            #     'website': website
            # })
            # results.append(result)

    return results


if __name__ == "__main__":
    websites = ['ma-giam-gia-tiki']

    for website in websites:
        url = "https://magiamgia.com/" + website + "/"
        re2 = requests.get(url)
        root = html.fromstring(re2.content)

        category = root.xpath('//h4[@class="mgg-coupon-cat-title"]')

        results = []

        if len(category) == 0:
            print(1)
            # name_cate = 'Khuyến mãi khác'
            # item = root.xpath('//div[@class="offers-details"]')
            # results = handle_item(item, results)
        else:
            for item_cate in category:
                arr_name_cate = item_cate.xpath('text()')
                if len(arr_name_cate) == 0:
                    name_cate = "Khuyến mãi khác"
                else:
                    name_cate = arr_name_cate[0]

                item = item_cate.xpath('following-sibling::div')


                results = handle_item(item, results)
                # break
        break
        # for item in results:
        #     data = item[0]
        #     data['action'] = 'set_voucher'
        #     req = requests.post('http://localhost/analysis-center/wp-admin/admin-ajax.php', data=data)