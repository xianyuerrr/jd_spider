import pandas as pd
from selenium import webdriver
import time


# 查询商品
def get_product(keyword):
    driver.find_element_by_css_selector('#key').send_keys(keyword)
    driver.find_element_by_css_selector(
        '#search > div > div.form > button').click()
    driver.implicitly_wait(10)  # 等待渲染


# 模拟鼠标滚动
def drop_down():
    for i in range(1, 10):
        time.sleep(0.3)
        j = i / 10
        js = 'document.documentElement.scrollTop=document.documentElement.scrollHeight * %s' % j
        driver.execute_script(js)


# 解析数据
def analyse_data():
    rows = pd.DataFrame()
    lis = driver.find_elements_by_css_selector('.gl-item')
    # print(lis)
    for li in lis:
        try:
            sku = li.get_attribute("data-sku")
            spu = li.get_attribute(("data-spu"))
            name = li.find_element_by_css_selector('.p-name a em').text
            name = name.replace('京东超市',
                                '').replace('京品数码',
                                            '').replace('京品电脑',
                                                        '').replace('\n', '')
            promo_words = li.find_element_by_css_selector('.p-name a i').text
            link = li.find_element_by_css_selector('.p-name a').get_attribute("href")
            price = li.find_element_by_css_selector(
                ' .p-price > strong > i').text + '元'
            comment = li.find_element_by_css_selector(
                '.p-commit strong a').text
            comment_link = li.find_element_by_css_selector(
                '.p-commit strong a').get_attribute("href")
            shop = li.find_element_by_css_selector('.p-shop span a').text
            shop_link = li.find_element_by_css_selector('.p-shop span a').get_attribute("href")
            # print(name, price, comment, shop, sep=' | ')
            rows = rows.append([{'商品': name, '价格': price, '评论数量': comment, '店铺': shop, "促销信息": promo_words,
                                 "sku": sku, "spu": spu, "商品链接": link, "评论链接": comment_link, "店铺链接": shop_link}])
        except:
            pass
    return rows


def nextpage():
    driver.find_element_by_css_selector(
        '#J_bottomPage > span.p-num > a.pn-next > em').click()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    # driver.maximize_window()  # 最大化窗口
    driver.get('https://jd.com')
    # keyword = input('请输入要查询的商品名称：\n')
    keyword = "螺蛳粉"
    get_product(keyword)
    data = pd.DataFrame()
    for i in range(0, 50):
        drop_down()
        data = data.append(analyse_data())
        nextpage()
    # print(data)
    data.to_csv('data.csv', index=False, encoding='utf-8-sig')  # gb2312 也可
    driver.quit()
