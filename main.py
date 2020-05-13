from functions import make_df, scrap_items, make_data_dir, save_data, driver_get, select_drop


#参考URL：https://tanuhack.com/selenium/#WebDriver-2

def main():
    url = 'http://www.i-ppi.jp/Search/Web/Koji/Kokoku/SearchEasy.aspx?data1=8'
    driver = driver_get(url)

    select_drop(driver, 'drpTopKikanInf', '0')
    select_drop(driver, 'drpLargeKikanInf2', '21')
    select_drop(driver, 'drpMiddleKikanInf', '08')
    select_drop(driver, 'drpDistrict', '8')
    select_drop(driver, 'drpKokokuYear', '1')

    search_btn = driver.find_element_by_id('btnSearch')
    search_btn.click()

    items = scrap_items(driver)
    df_new = make_df(items)

    data_dir = make_data_dir()
    save_data(data_dir, df_new)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()