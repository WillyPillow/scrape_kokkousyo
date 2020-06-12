from pathlib import PurePath, Path #参考サイト：https://note.nkmk.me/python-pathlib-usage/
import pandas as pd
import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    df['Organization'] = items[0]
    df['Department'] = items[1]
    df['Title'] = items[2]
    df['Format'] = items[3]
    df['Type'] = items[4]
    df['Date1'] = items[5]
    df['Location From'] = items[6]
    df['Location To'] = items[7]
    df['Date2'] = items[8]
    df['Date3'] = items[9]
    df['URL'] = items[10]

    return df


def scrap_items(driver, num_pages=100, timeout=10):
    organs = []
    departments = []
    titles = []
    format_s = []
    type_s = []
    date_1_s = []
    date_2_s = []
    date_3_s = []
    loc_from_s = []
    loc_to_s = []
    urls = []
    items = [organs, departments, titles, format_s, type_s, date_1_s, loc_from_s, loc_to_s, date_2_s, date_3_s, urls]

    try:
        for p in range(num_pages):
            search_list = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'dgrSearchList')))
            trs = search_list.find_elements_by_tag_name('tr')
            for i in range(len(trs)):
                search_list = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'dgrSearchList')))
                trs = search_list.find_elements_by_tag_name('tr')
                tds = trs[i].find_elements_by_tag_name('td')
                if not tds:
                    continue
                else:
                    link = tds[2].find_elements_by_tag_name('a')[0]
                    assert link
                    link.click()
                    time.sleep(1)
                    try:
                        organ = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'lblHachukikan'))).text
                        organs.append(organ)
                        department = driver.find_element_by_id('lblHachusha').text
                        departments.append(department)
                        title = driver.find_element_by_id('lblKojiNm').text
                        titles.append(title)
                        loc_from = driver.find_element_by_id('lblKojiPlaceFrom').text
                        loc_from_s.append(loc_from)
                        loc_to = driver.find_element_by_id('lblKojiPlaceTo').text
                        loc_to_s.append(loc_to)
                        format_ = driver.find_element_by_id('lblNyusatsuPtn').text
                        format_s.append(format_)
                        type_ = driver.find_element_by_id('lblKojiType').text
                        type_s.append(type_)
                        date_1 = driver.find_element_by_id('lblKokokuDate').text
                        date_1_s.append(date_1)
                        date_2 = driver.find_element_by_id('lblkigenDate').text
                        date_2_s.append(date_2)
                        date_3 = driver.find_element_by_id('lblKasatuDate').text
                        date_3_s.append(date_3)
                        url = driver.find_element_by_id('dgrKokoku').find_elements_by_tag_name('a')[0].get_attribute('href')
                        urls.append(url)
                        print(title, url)
                    except Exception as e:
                        print('[ERR] Skipping...')
                        print(e)
                    finally:
                        driver.back()

            driver.find_element_by_id('btnNext2').click()
            time.sleep(1)
    except Exception as e:
        print('[ERR] Exiting at page %d...' % p)
        print(e)
    finally:
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
    driver_home = '/usr/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_home, options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    return driver
