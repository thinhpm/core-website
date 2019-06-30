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
    arr_code = re.findall(r'\((.*?)\)', string_link)[0]
    list_code = arr_code.split(",")[2]
    list_code = list_code.replace("'", "")
    return list_code


def get_link_aff(string_link):
    link_aff = re.findall(r'window\.open\(\'(.*?)\'\)', string_link)[0]

    return link_aff


def get_date(date_exp):

    return date_exp
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
    for i in item:
        result = []
        id_coupon = i.xpath('div/div/div/div[2]/div/a/@id')[0]
        is_voucher = 'pull-right' not in i.xpath('div/div/div/div[2]/div/a/@class')[0]
        percent = i.xpath('div/div/div/div/div/div[3]/text()')[0].strip()

        description = i.xpath('div/div/div/div/div/div[4]/div[2]/div/div/div[3]/text()')
        if len(description) == 0:
            continue

        name = i.xpath('div/div/div/div[1]/div/div[4]/div[1]/text()')[0]
        description = description[0]
        date_exp = i.xpath('div/div/div/div/div/div[4]/div[2]/div/div/div[2]/text()')[0]
        code = i.xpath('div/div/div/div[2]/div/a/div/span/text()')[0].strip()

        if is_voucher:
            link_aff = i.xpath('div/div/div/div[2]/div/a/@onclick')[0]
            code = get_code(link_aff)
            link_aff = get_link_aff(link_aff)
            is_voucher = 1
        else:
            link_aff = i.xpath('div/div/div/div[2]/div/a/@href')[0]
            is_voucher = 0

        # link_aff = process_deep_link(link_aff)
        link_aff = ''
        date_exp = get_date(date_exp)

        result.append({
            'id_coupon': id_coupon,
            'is_voucher': is_voucher,
            'percent': percent.strip(),
            'description': description,
            'name': name,
            'date_exp': date_exp,
            'code': code.strip(),
            'link_aff': link_aff,
            'name_cate': name_cate,
            'website': website
        })

        results.append(result)

    return results


if __name__ == "__main__":
    websites = ['sendo', 'tiki']

    for website in websites:
        url = "https://bloggiamgia.vn/ma-giam-gia/" + website + "/"
        re2 = requests.get(url)
        root = html.fromstring(re2.content)

        category = root.xpath('//h2[@class="wpsm_toplist_heading"]')
        results = []

        if len(category) == 0:
            name_cate = 'Khuyến mãi khác'
            item = root.xpath('//div[@class="offers-details"]')
            results = handle_item(item, results)
        else:
            for item_cate in category:
                arr_name_cate = item_cate.xpath('span/strong/text()')
                if len(arr_name_cate) == 0:
                    name_cate = "Khuyến mãi khác"
                else:
                    name_cate = arr_name_cate[0]

                t = item_cate.xpath('following-sibling::div[@class="clearfix"][1]')[0]
                item = t.xpath('div/div[@class="offers-details"]')

                results = handle_item(item, results)
        print(len(results))
        for item in results:
            data = item[0]
            data['action'] = 'set_voucher'
            req = requests.post('http://mgghot.com/wp-admin/admin-ajax.php', data=data)
            print(req.status_code)