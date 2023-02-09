import os
import re
import sys
import time
import shutil
import random
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# abs path
cur_dir = os.path.dirname(os.path.realpath(__file__))
src = os.path.abspath(os.path.join(cur_dir, os.pardir))
sys.path.append(src)

from crawling.crawler import get_url, click_elm

class QuantusQA:
    def __init__(self, env):
        if env == "prod" or env == "production":
            self.url = "https://www.quantus.kr"
        elif env == "dev" or env == "develop":
            self.url = "https://dev.quantus.kr"
        else:
            raise AttributeError("올바른 환경을 입력하세요. ('prod' or 'dev')")
        
        self.init_variables()
            
    def init_variables(self):
        self.variables = {
            "custom_filters": [],
            "custom_factors": [],
            "logs": [],
            "alert_msg": [],
            "errors": [],
        }
        self.gauges = {
            # "init": "",
            # "backtest": "",
            # "decile": "",
            # "port": "",
            # "past": "",
        }

    def select_level(self, wd, level: int = None):
        """Select Level

        Args:
            wd (_type_): _description_
            level (int, optional): _description_. Defaults to None.
        """
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

            self.variables["level"] = d[level]
            # select level
            levels = wd.find_elements(By.CLASS_NAME, "css-2ho4nc")
            levels[level].click()
            time.sleep(1.5)

            # apply
            wd.find_element(By.CLASS_NAME, "second_button").click()
            time.sleep(1.5)
        
    def sign_in(self, wd, login: int = None, email: str = None, pw: str = None, level: int = None):
        """Sign in (Log in)

        Args:
            wd (_type_): _description_
            login (int, optional): _description_. Defaults to None.
            email (str, optional): _description_. Defaults to None.
            pw (str, optional): _description_. Defaults to None.
            level (int, optional): _description_. Defaults to None.
        """
        # go to login page
        wd.get(f"{self.url}/login")
        time.sleep(3.5)
        
        # select level
        self.select_level(wd, level)
        
        d = {
            0: "구글",
            1: "카카오",
        }
        if not login:
            keys = list(d.keys())
            login = random.randint(min(keys), max(keys))

        try:
            login = d[login]
            self.variables["login"] = login

            wd.find_element(By.ID, login).click()

            if not email or not pw:
                # Enter the login info
                email = 'wjddustjsla@naver.com'
                pw = 'jys1013011!'

            elm_email = wd.find_element(By.NAME, "loginKey")
            elm_pw = wd.find_element(By.NAME, "password")

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
            
            # gauge init
            self.gauges["init"] = self.get_gauge(wd)
        
        except NoSuchElementException:
            pass
        
    def select_universe(self, wd, strategy_name: str = None, universe: int = None, removed_filters: list = [], removed_sectors: list = [], min_filter: int = 2, min_sector: int = 5):
        """Select universe, filter, sector

        Args:
            wd (_type_): _description_
            strategy_name (str, optional): _description_. Defaults to None.
            universe (int, optional): _description_. Defaults to None.
            removed_filters (list, optional): _description_. Defaults to [].
            removed_sectors (list, optional): _description_. Defaults to [].
            min_filter (int, optional): _description_. Defaults to 2.
            min_sector (int, optional): _description_. Defaults to 5.
        """
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
        self.variables["strategy_name"] = strategy_name
        
        if universe != 0:
            # select universe
            d = {
                1: "한국",
                2: "미국",
                3: "KOSPI",
                4: "KOSDAQ",
            }
            if universe is None:
                keys = list(d.keys())
                universe = random.randint(min(keys), max(keys))
            self.variables["universe"] = d[universe]
            print(f"Universe: {d[universe]}")

            universe_class = "css-cy3vpx"
            wd.find_element(By.CLASS_NAME, universe_class).click()
            universes = wd.find_elements(By.CLASS_NAME, universe_class)

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

        if removed_filters is None:
            removed_filters = random.sample(range(len_filters), random.randint(min_filter, len(filters)))
        elif removed_filters == "all":
            removed_filters = range(0, len_filters)
        
        removed_filters = sorted(removed_filters)
        self.variables["removed_filters"] = []
        for i in removed_filters:
            self.variables["removed_filters"].append(filters[i].text.strip())
            removed_elms[i].click()

        if removed_sectors is None:
            removed_sectors = random.sample(range(len_filters, len_filters+len(sectors)), random.randint(0, len(sectors) - min_sector))
        removed_sectors = sorted(removed_sectors)
        self.variables["removed_sectors"] = []
        for j in removed_sectors:
            i = j - len_filters
            self.variables["removed_sectors"].append(sectors[i].text.strip())
            removed_elms[j].click()
            
    def click_next_btn(self, wd):
        # /backtest, /port에서 click '다음' button
        next_btn_class = "css-1qm89cl"
        wd.find_element(By.CLASS_NAME, next_btn_class).click()
        time.sleep(1)
        
    def select_factors(self, wd, factors: list = None):
        """Select factors

        Args:
            wd (_type_): _description_
            factors (list, optional): _description_. Defaults to None.
        """
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
            # self.variables[factor_kind] = []
            nms = fs.find_all("div", factor_elm_class)
            factor_kinds[factor_kind] = [nm.text.replace("?", "").strip() for nm in nms]
            
        if factors is None:
            factors = random.sample(range(len(elm_factors)), random.randint(1, len(elm_factors)-1))
        elif factors == "all":
            factors = range(0, len(elm_factors))
            
        factors = sorted(factors)
        self.variables["factors"] = []
        for i in factors:
            elm_factor = elm_factors[i]
            elm_factor.click()
            time.sleep(0.25)
            factor = factor_nms[i].text.replace("?", "").strip()
            
            for k, v in factor_kinds.items():
                if factor in v:
                    # self.variables[k].append(factor)
                    self.variables["factors"].append(factor)
                    break
    
    def select_custom_factors(self, wd, custom_factors: dict = None):
        """Select custom factors

        Args:
            wd (_type_): _description_
            custom_factors (list, optional): _description_. Defaults to None.
        """
        
        if custom_factors is not None:
            denominators = custom_factors["denominators"]
            numerators = custom_factors["numerators"]
            custom_btn_class = "css-1bz1c0h"
            custom_select_class = "css-9n7j5m"

            custom_factor_index = 0
            for i, j in zip(denominators, numerators):
                custom_deno_elms_id = f"커스텀 팩터 {custom_factor_index+1}.denominator"
                custom_numer_elms_id = f"커스텀 팩터 {custom_factor_index+1}.numerator"
                
                # add button
                click_elm(wd, by="class", value=custom_btn_class)
                
                # set denominator 
                click_elm(wd, by="class", value=custom_select_class, index=custom_factor_index * 2)
                deno_elms = wd.find_elements(By.ID, custom_deno_elms_id)
                deno = deno_elms[i].get_attribute("value")
                deno_elms[i].click()
                time.sleep(1.5)

                # set numerator
                click_elm(wd, by="class", value=custom_select_class, index=custom_factor_index * 2 + 1)
                numer_elms = wd.find_elements(By.ID, custom_numer_elms_id)
                numer = numer_elms[j].get_attribute("value")
                numer_elms[j].click()
                time.sleep(1.5)
                
                self.variables["custom_factors"].append(f"{deno} / {numer}")
                custom_factor_index += 1


    def set_rebal_prd(self, wd, rebalancing_period: int):
        """Select rebalancing period

        Args:
            wd (_type_): _description_
            rebalancing_period (int): _description_
        """
        # rebalancing_period_xpath = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[6]/div[1]/div[2]/input"
        # wd.find_element(By.XPATH, rebalancing_period_xpath).click()
        
        rebalancing_class = "css-1pud7n6"
        click_elm(wd, by="class", value=rebalancing_class)

        d = {
            0: "월별",
            1: "분기별",
            2: "반기별",
            3: "매년",
        }

        # keys = list(d.keys())
        # j = random.randint(min(keys), max(keys))
        
        self.variables["rebalancing_period"] = d[rebalancing_period]
        
        # rebalancing_period_xpath = f"/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[6]/div[3]/div[{rebalancing_period}]/div/input"
        # wd.find_element(By.XPATH, rebalancing_period_xpath).click()
        rebalancing_elm_class = "css-1h6hvk5"
        click_elm(wd, by="class", value=rebalancing_elm_class, index=rebalancing_period)
        time.sleep(1)


    def set_conditions(self, wd, **kwargs):

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
            # 0: ["초기 투자 금액", kwargs["init_amounts"]],
            # 1: ["거래 수수료", kwargs["fees"]],
            # 2: ["종목 수", kwargs["stock_counts"]],
            # 3: ["손절기준", kwargs["stop_loss"]],
            # 4: ["익절기준", kwargs["profit"]],
            0: ["init_amounts", kwargs["init_amounts"]],
            1: ["fees", kwargs["fees"]],
            2: ["stock_counts", kwargs["stock_counts"]],
            3: ["stop_loss", kwargs["stop_loss"]],
            4: ["profit", kwargs["profit"]],
        }
        
        port_conditions = {
            # 0: ["초기 투자 금액", kwargs["init_amounts"]],
            # 1: ["종목 수", kwargs["stock_counts"]],
            0: ["init_amounts", kwargs["init_amounts"]],
            1: ["stock_counts", kwargs["stock_counts"]],
        }
        
        input_class = "css-1n7t3r7"
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
            self.variables[cond] = val
            
            if val is not None:
                elm.clear()
                time.sleep(1.5)
                elm.send_keys(val)
            if i == 1 and kind == "backtest":
                # 리밸런싱 기간 선택
                rebalancing_period = kwargs["rebalancing_period"]
                if rebalancing_period is not None:
                    self.set_rebal_prd(wd, rebalancing_period)
            i += 1

    def save_strategy(self, wd):
        # save strategy
        save_button_class = "css-72wevi"
        wd.find_element(By.CLASS_NAME, save_button_class).click()
        time.sleep(2)
        self.check_alert(wd)
        
    def backtest(self, wd):
        # backtest
        backtest_button_class = "css-1qm89cl"
        wd.find_element(By.CLASS_NAME, backtest_button_class).click()
        st = time.time()
        time.sleep(10)
        self.check_alert(wd)
        return st
        
    def reset(self, wd):
        try:
            wd.find_element(By.CLASS_NAME, "css-87arup").click()
            time.sleep(1)
        except:
            try:
                wd.find_element(By.CLASS_NAME, "button").click()
                time.sleep(1)
            except:
                print("\n\n** 설정 값 초기화에 실패하였습니다. **")
        

    def check_alert(self, wd):
        
        # 여기에 alert class를 추가하세요
        alert_classes = [
            "css-1pzp69m",    # 전략적용, 전략 삭제
            "css-16mgwj1",    # 팩터 설정 오류
            "css-1x7ny0l",
            "css-1aq7lc0",
            "css-1t6s947",
            "css-2fz7y1",
            "css-1pgvb8v",
            "css-1hqfcmt",
            # "css-1iat9ul",
        ]
        check_classes = [
            "css-1lcj2w",
            "css-73nldo",
            "css-1lcj2w",
            "css-28mzi7",
            "css-m76kg7",    # 취소, 확인 버튼 둘다 존재할 때 확인 버튼
        ]
        time.sleep(2)
        soup = BeautifulSoup(wd.page_source, "lxml")
        alert_msg = None
        i = 0
        ck = False
        while i < len(alert_classes):
            alert_area = soup.find("div", alert_classes[i])
            if alert_area:
                alert_msg = alert_area.text.replace("확인", "").replace("취소", "")
                alert_msg = re.sub(r' +', ' ', alert_msg).strip()
                print(f"ALERT: {alert_msg}")
                self.variables["alert_msg"].append(alert_msg)
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


    def read_result(self, wd, kind, start_time):
        for p in sys.path:
            if "Users" in p:
                user_name = p.split("/")[2]    
                download_dir = f"/Users/{user_name}/Downloads"
                bak_dir = os.path.join(download_dir, "bak")
                if not os.path.exists(bak_dir):
                    os.mkdir(bak_dir)
                break

        files = os.listdir(download_dir)
        files = [os.path.join(download_dir, f) for f in files]
        files.sort(key=lambda x: os.path.getmtime(x))

        # strategy_name 
        strategy_name = f'{self.variables["strategy_name"]}'
        
        if kind == 0:
            # backtest
            file = strategy_name + "_backtest_result.html"
            path = os.path.join(download_dir, file)
            bak = os.path.join(bak_dir, file)
            
            # 결과 파일 생성 여부 확인
            ck = True
            st = time.time()
            while not os.path.exists(path):
                time.sleep(10)
                # 백테스트에 100초 이상 소요되면 에러로 간주
                if time.time() - st > 100:
                    ck = False
                    self.variables["errors"].append("backtest error")
                    break

            if ck:
                # elapsed time
                self.variables["backtest_elapsed"] = round(time.time() - start_time, 2)
                
                _wd = get_url("file://" + path)
                soup = BeautifulSoup(_wd.page_source, "lxml")
                tbl = soup.find("div", {"id": "right"}).find("table")
                tbl_trs = tbl.find_all("tr")

                # Cumulative Return
                tbl_tr_td = tbl_trs[4].find_all("td")
                self.variables[tbl_tr_td[0].text] = tbl_tr_td[1].text
                # CAGR
                tbl_tr_td = tbl_trs[5].find_all("td")
                self.variables[tbl_tr_td[0].text] = tbl_tr_td[1].text
                # Max Drawdown	
                tbl_tr_td = tbl_trs[15].find_all("td")
                self.variables[tbl_tr_td[0].text] = tbl_tr_td[1].text
                
                shutil.move(path, bak)
                _wd.quit()
                
                # get gauge & init gauge
                gauge = self.get_gauge(wd)
                used = self.gauges["init"] - gauge
                self.gauges["init"] = gauge
                self.gauges["backtest"] = used
                
                
        elif kind == 1:
            # port extraction
            file = strategy_name + "_portfolio_result.csv"
            path = os.path.join(download_dir, file)
            bak = os.path.join(bak_dir, file)
            
            # 결과 파일 생성 여부 확인
            ck = True
            st = time.time()            
            while not os.path.exists(path):
                time.sleep(10)
                # 백테스트에 100초 이상 소요되면 에러로 간주
                if time.time() - st > 60:
                    self.variables["errors"].append("port extraction error")
                    ck = False
                    break
            
            if ck:
                self.variables["port_elapsed"] = round(time.time() - start_time, 2)
                df = pd.read_csv(path)
                self.variables["portfolio"] = str(df["Name"].tolist())
                self.variables["industry"] = str(df["업종명"].tolist())
                shutil.move(path, bak)
                
                # get gauge & init gauge
                gauge = self.get_gauge(wd)
                used = self.gauges["init"] - gauge
                self.gauges["init"] = gauge
                self.gauges["port"] = used
                
                
        elif kind == 2:
            # 10분위 테스트
            file = strategy_name + "_quantile_result.csv"
            path = os.path.join(download_dir, file)
            bak = os.path.join(bak_dir, file)
            
            # 결과 파일 생성 여부 확인
            ck = True
            st = time.time()            
            while not os.path.exists(path):
                time.sleep(10)
                # 10분위 테스트에 180초 이상 소요되면 에러로 간주
                if time.time() - st > 180:
                    self.variables["errors"].append("decile test error")
                    ck = False
                    break
            
            if ck:
                self.variables["decile_elapsed"] = round(time.time() - start_time, 2)
                df = pd.read_csv(path)
                
                data = df.iloc[4, :].tolist()
                self.variables[data[0].strip() + "s"] = data[1:]

                data = df.iloc[5, :].tolist()
                self.variables[data[0].strip() + "s"] = data[1:]

                data = df.iloc[10, :].tolist()
                self.variables[data[0].strip() + "s"] = data[1:]
                shutil.move(path, bak)
                
                # get gauge & init gauge
                gauge = self.get_gauge(wd)
                used = self.gauges["init"] - gauge
                self.gauges["init"] = gauge
                self.gauges["decile"] = used
        else:
            raise TypeError("올바른 kind(0: backtest, 1: port, 2: decile)를 입력하세요")


    def init_page(self, **kwargs):
        time.sleep(1.5)
        url = self.url
        wd = get_url(url, window=True, image=True, logging=True)
        time.sleep(3.5)

        # 로그인
        self.sign_in(wd, kwargs["login"], kwargs["email"], kwargs["pw"], kwargs["level"])
        
        return wd

    def test_back_port(self, wd, kind: int = None, **kwargs):
        
        if kind is None:
            kind = random.randint(0, 1)
        
        if kind == 0:
            # backtest
            wd.get(f"{self.url}/backtest/universe")
        elif kind == 1:
            # port 
            wd.get(f"{self.url}/port/universe")
        else:
            raise ValueError("올바른 kind(0: backtest, 1: port)를 입력하세요")

        # init gauge
        self.gauges["init"] = self.get_gauge(wd)
        
        # reset settings
        time.sleep(1.5)
        self.reset(wd)
        
        # 유니버스 선택
        self.select_universe(wd, kwargs["strategy_name"], kwargs["universe"], kwargs["removed_filters"], kwargs["removed_sectors"])
        time.sleep(2)
        self.click_next_btn(wd)

        # 팩터 선택
        self.select_factors(wd, kwargs["factors"])
        time.sleep(2)
        
        # 커스텀 팩터 선택
        self.select_custom_factors(wd, kwargs["custom_factors"])
        self.click_next_btn(wd)
        
        # 설정
        self.set_conditions(wd, **kwargs["conditions"])
            
        # 전략 저장
        self.save_strategy(wd)
        self.check_alert(wd)
        time.sleep(1.5)
        
        # 테스트 실행 및 결과 얻기
        self.get_result(wd, kind)
        
    def get_result(self, wd, kind):
        # 백테스트 or 포트추출 실행
        st = self.backtest(wd)
        
        # get log
        _log = wd.get_log(log_type="browser")
        if len(_log) != 0:
            self.variables['logs'].append(_log)
        
        # get result data
        self.read_result(wd, kind=kind, start_time=st)

    def remove_strategy(self, wd):
        # 가장 최근에 저장한 전략 삭제
        wd.get(f"{self.url}/mypage/strategy")
        time.sleep(1.5)
        
        remove_xpath = "/html/body/div[1]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/img"
        wd.find_element(By.XPATH, remove_xpath).click()
        self.check_alert(wd)
        self.check_alert(wd)

    def remove_startegies(self, wd):
        # 모든 전략 삭제
        i = 0
        while True:
            try:
                self.remove_strategy(wd)
            except:
                break
            i += 1
            
        print(f"삭제한 전략 수: {i}")
        
        
    def get_gauge(self, wd):
        # 게이지 정보 얻기
        gauge_class = "gaugediv"
        try:
            elm = wd.find_element(By.CLASS_NAME, gauge_class)
            remain_gauge = int(elm.get_attribute("innerHTML").replace("%", "").strip())
        except NoSuchElementException:
            remain_gauge = 1e10
            
        
        return remain_gauge