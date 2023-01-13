from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from crawler import get_url, click_elm


def scraping_factors():
    # factor scraping
    wd = get_url("https://v2.quantus.kr/backtest/factors")
    soup = BeautifulSoup(wd.page_source, "lxml")

    factor_area_class = "css-kwx3if"
    factor_kind_class = "css-12hmsi2"
    factor_elm_class = "css-1z2md3"
    available_factor_class = "css-192m3r6"

    factor_area = soup.find_all("div", factor_area_class)
    elm_factors = wd.find_elements(By.CLASS_NAME, factor_elm_class)

    variables = {}
    i = 0
    for fs in factor_area:
        factor_kind = fs.find("div", factor_kind_class).text.strip()
        variables[factor_kind] = {}
        variables[factor_kind]["unavailable"] = []
        fs_nms = fs.find_all("div", factor_elm_class)
        for fs_nm in fs_nms:
            _fs_nm = fs_nm.text.strip().replace("?", "")
            if fs_nm.find("div", available_factor_class):
                variables[factor_kind][i] = _fs_nm
                i += 1
            else:
                variables[factor_kind]["unavailable"].append(_fs_nm)

    return variables, i



def scraping_sectors():
    # 기본 필터, 제외할 섹터 스크레이핑
    wd = get_url("https://v2.quantus.kr/backtest/universe")
    soup = BeautifulSoup(wd.page_source, "lxml")
    filter_sector_class = "css-192m3r6"

    filters = soup.find("div", "css-i2b1or").find_all("div", filter_sector_class)
    sectors = soup.find("div", "css-16ww4h3").find_all("div", filter_sector_class)

    d = {
        "기본 필터": {},
        "제외할 섹터": {},
    }
    for i in range(len(filters) + len(sectors)):
        if i < len(filters):
            d["기본 필터"][i] = filters[i].text.strip()
            
        else:
            d["제외할 섹터"][i] = sectors[i - len(filters)].text.strip()
            
    return d

def scraping_custom_factors():
    wd = get_url("https://v2.quantus.kr/backtest/factors", window=True, image=True)

    # 다음에 할게요 
    wd.find_element(By.CLASS_NAME, "close_button").click()
    
    custom_btn_class = "css-1bz1c0h"
    click_elm(wd, by="class", value=custom_btn_class)
    
    custom_select_class = "css-9n7j5m"
    click_elm(wd, by="class", value=custom_select_class)


    custom_deno_elms_id = "커스텀 팩터 1.denominator"
    deno_elms = wd.find_elements(By.ID, custom_deno_elms_id)
    custom_factors = {}
    i = 0
    for elm in deno_elms:
        custom_factors[i] = elm.get_attribute('value')
        i += 1
    
    wd.quit()
    return custom_factors