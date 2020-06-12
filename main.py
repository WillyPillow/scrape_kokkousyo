from functions import make_df, scrap_items, make_data_dir, save_data, driver_get, select_drop


#参考URL：https://tanuhack.com/selenium/#WebDriver-2

def main():
    url = 'https://www.i-ppi.jp/IPPI/SearchServices/Web/Koji/Kokoku/Search.aspx'
    driver = driver_get(url)

    select_drop(driver, 'drpCount', '100')
    driver.find_element_by_id('rbtKokokuDate1').click()

    search_btn = driver.find_element_by_id('btnSearch')
    search_btn.click()

    items = scrap_items(driver)
    df_new = make_df(items)

    print(df_new)
    df_new.to_json('out.json', default_handler=str)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    main()
