import os
import sys
import time
import random
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

import selenium
import webdriver_manager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from crawler import get_url

variables = {}

def select_level(wd, level: int = None):

    soup = BeautifulSoup(wd.page_source, "lxml")
    if soup.find("div", "css-2ho4nc"):
        d = {
            0: "초급",
            1: "중급",
            2: "고급",
        }
        if not level:
            keys = list(d.keys())
            level = random.randint(min(keys), max(keys))

        variables["level"] = d[level]
        # select level
        levels = wd.find_elements(By.CLASS_NAME, "css-2ho4nc")
        levels[level].click()

        # apply
        wd.find_element(By.CLASS_NAME, "yes").click()
        time.sleep(1)
    
def sign_in(wd, login: int = None, email: str = None, pw: str = None, level: int = None):
    
    # go to login page
    wd.get("https://v2.quantus.kr/login")
    
    # select level
    select_level(wd, level)
    
    d = {
        0: "구글",
        1: "카카오",
    }
    if not login:
        keys = list(d.keys())
        login = random.randint(min(keys), max(keys))

    try:
        login = d[login]
        variables["login"] = login

        wd.find_element(By.ID, login).click()

        if not email or not pw:
            # Enter the login info
            email = 'wjddustjsla@naver.com'
            pw = 'jys1013011!'

        elm_email = wd.find_element(By.ID, "input-loginKey")
        elm_pw = wd.find_element(By.ID, "input-password")

        # input login info
        elm_email.send_keys(email)
        elm_pw.send_keys(pw)
        time.sleep(2.5)
        
        soup = BeautifulSoup(wd.page_source, "lxml")
        if soup.find("div", {"id": "rc-anchor-container"}):
            wd.find_element(By.CLASS_NAME, "recaptcha-checkbox-checkmark").click()
            time.sleep(2)
            
        # click login button
        # wd.find_element(By.CLASS_NAME, "btn_g highlight").click()
        wd.find_element(By.XPATH, "/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]").click()
        time.sleep(3.5)
        print("Complete login!")
    
    except NoSuchElementException:
        pass
    
def select_universe(wd, strategy_name: str = None, universe: int = None, removed_filters: list = [], removed_sectors: list = [], min_filter: int = 2, min_sector: int = 5):
    # /backtest/universe
    # /port/universe
    
    # strategy name
    if not strategy_name:
        now = datetime.now().strftime("%y%m%d_%H_%M_%S")
        strategy_name = f"test_{now}"
    print(f"Strategy name: {strategy_name}")

    # Enter the strategy name
    strategy_name_xpath = "/html/body/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/input"
    elm_strategy_name = wd.find_element(By.XPATH, strategy_name_xpath)
    elm_strategy_name.clear()
    time.sleep(1.5)
    elm_strategy_name.send_keys(strategy_name)
    variables["strategy_name"] = strategy_name
    
    # select universe
    d = {
        0: "한국",
        1: "미국",
        2: "KOSPI",
        3: "KOSDAQ",
    }
    if not universe:
        keys = list(d.keys())
        universe = random.randint(min(keys), max(keys))
        variables["universe"] = d[universe]

    print(f"Universe: {d[universe]}")

    wd.find_element(By.CLASS_NAME, "css-cy3vpx").click()
    universes = wd.find_elements(By.CLASS_NAME, "css-zf30n6")

    universe = universes[universe]
    universe.click()
    
    # check filter & sector    
    soup = BeautifulSoup(wd.page_source, "lxml")
    filter_sector_class = "css-192m3r6"

    filters = soup.find("div", "css-i2b1or").find_all("div", filter_sector_class)
    sectors = soup.find("div", "css-16ww4h3").find_all("div", filter_sector_class)
    len_filters = len(filters)

    # 기본 필터 & 제외할 섹터 elements
    removed_elms = wd.find_elements(By.CLASS_NAME, filter_sector_class)

    if not removed_filters:
        removed_filters = random.sample(filters, random.randint(min_filter, len(filters)))
    variables["removed_filters"] = []
    for filter in removed_filters:
        variables["removed_filters"].append(filter.text.strip())
        i = filters.index(filter)
        removed_elms[i].click()

    if not removed_sectors:
        removed_sectors = random.sample(sectors, random.randint(0, len(sectors) - min_sector))
    variables["removed_sectors"] = []
    for sector in removed_sectors:
        variables["removed_sectors"].append(sector.text.strip())
        i = sectors.index(sector) + len_filters
        removed_elms[i].click()
        
def click_next_btn(wd):
    # /backtest, /port에서 click '다음' button
    wd.find_element(By.CLASS_NAME, "css-etpc0o").click()
    time.sleep(1)
    
def select_factors(wd, factors: list = None):
    # /backtest/factors
    # /port/factors
    
    factor_area_class = "css-kwx3if"
    factor_kind_class = "css-12hmsi2"
    factor_elm_class = "css-192m3r6"

    soup = BeautifulSoup(wd.page_source, "lxml")
    factor_area = soup.find_all("div", factor_area_class)
    elm_factors = wd.find_elements(By.CLASS_NAME, factor_elm_class)
    factor_nms = soup.find_all("div", factor_elm_class)

    factor_kinds = {}
    for fs in factor_area:
        factor_kind = fs.find("div", factor_kind_class).text.strip()
        variables[factor_kind] = []
        nms = fs.find_all("div", factor_elm_class)
        factor_kinds[factor_kind] = [nm.text.replace("?", "").strip() for nm in nms]
        
    if not factors:
        factors = random.sample(range(len(elm_factors)), random.randint(1, len(elm_factors)-1))
    elif factors == "all":
        factors = range(0, len(elm_factors))
        
    factors = sorted(factors)
    print(factors)
    for i in factors:
        elm_factor = elm_factors[i]
        elm_factor.click()
        time.sleep(0.25)
        factor = factor_nms[i].text.replace("?", "").strip()
        print(factor)
        
        for k, v in factor_kinds.items():
            if factor in v:
                variables[k].append(factor)
                break

def set_rebal_prd(wd, rebalancing_period: int):
    
    # 리밸런싱 기간 선택
    rebalancing_period_xpath = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[6]/div[1]/div[2]/input"
    wd.find_element(By.XPATH, rebalancing_period_xpath).click()

    d = {
        1: "월별",
        2: "분기별",
        3: "반기별",
        4: "매년",
    }

    # keys = list(d.keys())
    # j = random.randint(min(keys), max(keys))

    variables["리벨런싱 기간"] = d[rebalancing_period]
    rebalancing_period_xpath = f"/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[6]/div[3]/div[{rebalancing_period}]/div/input"
    
    wd.find_element(By.XPATH, rebalancing_period_xpath).click()
    time.sleep(1)

# def set_backtest_conditions(wd, init_amounts: int = None, fees: int = None, rebalancing_period: int = None, stock_counts: int = None, stop_loss: int = None, profit: int = None):

def set_conditions(wd, **kwargs):

    ''' input box
    0. 초기 투자 금액 *
    1. 거래 수수료 *
    2. 종목수 (20으로 입력되어 있음)
    3. 손절기준 *
    4. 익절기준 *
    '''

    ''' select box
    5. 리밸런싱 기간 *
    6. 비중 조절 방법 ('동일 비중'으로 지정되어 있음)
    7. 리밸런싱 전략 ('분할 매수/매도'로 지정되어 있음)
    '''
    
    backtest_conditions = {
        0: ["초기 투자 금액", kwargs["init_amounts"]],
        1: ["거래 수수료", kwargs["fees"]],
        2: ["종목 수", kwargs["stock_counts"]],
        3: ["손절기준", kwargs["stop_loss"]],
        4: ["익절기준", kwargs["profit"]],
    }
    
    port_conditions = {
        0: ["초기 투자 금액", kwargs["init_amounts"]],
        1: ["종목 수", kwargs["stock_counts"]],
    }
    
    input_class = "css-1tmhs6j"
    input_elms = wd.find_elements(By.CLASS_NAME, input_class)

    url = wd.current_url
    kind = url.split("/")[-1]

    if kind == "backtest":
        conditions = backtest_conditions
    elif kind == "port":
        conditions = port_conditions
    else:
        raise TypeError("잘못된 경로입니다.")

    i = 0
    for elm in input_elms:
        cond, val = conditions[i]
        variables[cond] = val
        elm.clear()
        time.sleep(1.5)
        elm.send_keys(val)
        if i == 1 and kind == "backtest":
            # 리밸런싱 기간 선택
            rebalancing_period = kwargs["rebalancing_period"]
            if rebalancing_period:
                set_rebal_prd(wd, rebalancing_period)
        i += 1

def save_strategy(wd):
    # save strategy
    save_button_class = "css-1o923v9"
    wd.find_element(By.CLASS_NAME, save_button_class).click()
    time.sleep(2)
    check_alert(wd)
    
def backtest(wd):
    # backtest
    backtest_button_class = "css-etpc0o"
    wd.find_element(By.CLASS_NAME, backtest_button_class).click()
    time.sleep(1)
    
def reset(wd):
    reset_btn_xpath = "/html/body/div[1]/div/div[2]/div/div/div[3]/div[2]/div/div"
    wd.find_element(By.XPATH, reset_btn_xpath).click()
    time.sleep(1)
    

def check_alert(wd):
    
    # 여기에 alert class를 추가하세요
    alert_classes = [
        "css-1x7ny0l",
        "css-1aq7lc0",
        "css-1t6s947",
        "css-2fz7y1",
        "css-1pgvb8v",
    ]
    check_classes = [
        "css-1lcj2w",
        "css-73nldo",
        "css-1lcj2w",
        "css-28mzi7",
        "css-m76kg7",
    ]
    time.sleep(2)
    soup = BeautifulSoup(wd.page_source, "lxml")
    alert_msg = None
    i = 0
    ck = False
    while i < len(alert_classes):
        alert_area = soup.find("div", alert_classes[i])
        if alert_area:
            alert_msg = alert_area.text
            j = 0
            while j < len(check_classes):
                check_class = check_classes[j]
                check_btn = alert_area.find("div", check_class)
                if check_btn:
                    wd.find_element(By.CLASS_NAME, check_class).click()
                    time.sleep(1)
                    ck = True
                    break
                j += 1
            
            if ck:
                break
        i += 1
    
    return alert_msg


def read_result(kind):
    for p in sys.path:
        if "Users" in p: 
            user_name = p.split("/")[2]    
            download_dir = f"/Users/{user_name}/Downloads"
            break

    files = os.listdir(download_dir)
    files = [os.path.join(download_dir, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))

    if kind == 0:
        # backtest
        path = [f for f in files if f.endswith(".html")][-1]
        
        _wd = get_url("file://" + path)
        soup = BeautifulSoup(_wd.page_source, "lxml")
        _wd.quit()
        
        tbl = soup.find("div", {"id": "right"}).find("table")
        tbl_trs = tbl.find_all("tr")

        results = {}
        # Cumulative Return
        tbl_tr_td = tbl_trs[4].find_all("td")
        results[tbl_tr_td[0].text] = tbl_tr_td[1].text
        # CAGR
        tbl_tr_td = tbl_trs[5].find_all("td")
        results[tbl_tr_td[0].text] = tbl_tr_td[1].text
        # Max Drawdown	
        tbl_tr_td = tbl_trs[15].find_all("td")
        results[tbl_tr_td[0].text] = tbl_tr_td[1].text
        
    elif kind == 1:
        # port extraction
        path = [f for f in files if f.endswith(".csv")][-1]
        df = pd.read_csv(path)
        print(df)
        results = df["Name"].tolist()
        
    return results


def init_page(**kwargs):
    time.sleep(1.5)
    url = "https://v2.quantus.kr/"
    wd = get_url(url, window=True, image=True, logging=True)
    time.sleep(3.5)

    # 로그인
    sign_in(wd, kwargs["login"], kwargs["email"], kwargs["pw"])
    
    return wd

def test_back_port(wd, kind: int = None, **kwargs):
    
    if not kind:
        kind = random.randint(0, 1)
    elif kind == 0:
        # backtest
        wd.get("https://v2.quantus.kr/backtest/universe")
    elif kind == 1:
        # port 
        wd.get("https://v2.quantus.kr/port/universe")
    else:
        raise TypeError("올바른 kind(0: backtest, 1: port)를 입력하세요")
    
    # 유니버스 선택
    select_universe(wd, kwargs["strategy_name"], kwargs["universe"], kwargs["removed_filters"], kwargs["removed_sectors"])
    time.sleep(2)
    click_next_btn(wd)

    # 팩터 선택
    select_factors(wd, kwargs["factors"])
    time.sleep(2)
    click_next_btn(wd)

    set_conditions(wd, **kwargs["conditions"])
        
    # 전략 저장
    save_strategy(wd)
    check_alert(wd)
    time.sleep(1.5)
    
    # 백테스트 or 포트추출 실행
    backtest(wd)
    
    variables['logs'] = wd.get_log(log_type="browser")
    
    results = read_result(kind)
    variables["results"] = results
    
    return variables