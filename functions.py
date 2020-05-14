from pathlib import PurePath, Path #参考サイト：https://note.nkmk.me/python-pathlib-usage/
import pandas as pd
import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# 参考サイト：https://pythondatascience.plavox.info/pandas/%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%82%92%E3%82%BD%E3%83%BC%E3%83%88%E3%81%99%E3%82%8B
#日付順にソートして再保存＆当日更新分のみ表示
def sort_csv(data_dir):
    path = PurePath.joinpath(data_dir, '入札公告.csv')
    f = pd.read_csv(path)
    sorted_data = f.sort_values(by='公告日', ascending=False)
    sorted_data.to_csv(path, index=False)


def save_data(data_dir, df_new):
    csv_data = PurePath.joinpath(data_dir, '入札公告.csv')
    new_titles = list(df_new['工事名'])
    if csv_data.exists():
        df_old = pd.read_csv(csv_data)
        old_titles = list(df_old['工事名'])
        for title in new_titles:
            if title in old_titles:
                pass
            else:
                df_new[df_new['工事名'] == title].to_csv(csv_data, mode='a', index=False, header=False)
        today = datetime.date.today().strftime('%Y/%m/%d')
        print(today, '更新分', sep='')
        if df_old[df_old['公告日'] == today].empty:
            print('本日の更新はありません')
        else:
            print(df_old[df_old['公告日'] == today])
        sort_csv(data_dir)

    else:
        df_new.to_csv(csv_data, index=False)
        print('df_new')
        print(df_new)


#main.py(=__file__)のあるディレクトリにdataディレクトリ作成し、パスobjを返す
def make_data_dir():
    target_path = Path(sys.argv[0]).parent.resolve()
    data_dir = PurePath.joinpath(target_path, 'data')
    if data_dir.exists():
        return data_dir
    else:
        data_dir.mkdir()
        return data_dir


def make_df(items):
    df = pd.DataFrame()
    df['発注機関'] = items[0]
    df['担当部・事務所'] = items[1]
    df['工事名'] = items[2]
    df['入札契約方式'] = items[3]
    df['工事区分'] = items[4]
    df['公告日'] = items[5]

    return df


def scrap_items(driver):
    organs = []
    departments = []
    titles = []
    format_s = []
    type_s = []
    date_s = []
    items = [organs, departments, titles, format_s, type_s, date_s]

    search_list = driver.find_element_by_id('dgrSearchList')
    trs = search_list.find_elements_by_tag_name('tr')
    time.sleep(1)
    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        if not tds:
            continue
        else:
            _organ = tds[1].text
            _organs = _organ.split('／')
            organ = _organs[0]
            organs.append(organ)
            department = _organs[1]
            departments.append(department)
            title = tds[2].text.replace('\u3000', '')
            titles.append(title)
            format_ = tds[3].text
            format_s.append(format_)
            type_ = tds[4].text
            type_s.append(type_)
            date_ = tds[5].text
            date_s.append(date_)

    return items


#参考URL：https://qiita.com/redoriva/items/aa9fa4c0bf2aeb8e1bff
#ドロップダウン選択で工事検索
def select_drop(driver, id_, value):
    elem = driver.find_element_by_id(id_)
    select_elem = Select(elem)
    select_elem.select_by_value(value)
    time.sleep(1)


#webdriverの位置を都度変える
def driver_get(url):
    driver_home = 'C:/chromedriver_win32/chromedriver'
    driver_gae = r'C:\Users\g2945\chromedriver\chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    try:
        driver = webdriver.Chrome(driver_home, options=options)
        driver.implicitly_wait(10)
        driver.get(url)
        return driver
    except:
        driver2 = webdriver.Chrome(driver_gae, options=options)
        driver2.implicitly_wait(10)
        driver2.get(url)
        return driver2