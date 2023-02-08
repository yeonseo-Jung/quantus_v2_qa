import os
import sys
import traceback
import pandas as pd

# abs path
cur_dir = os.path.dirname(os.path.realpath(__file__))
src = os.path.abspath(os.path.join(cur_dir, os.pardir))
sys.path.append(src)

from qa.quantus_qa import QuantusQA
from db.conn import AccessDataBase

db = AccessDataBase("quantus_test")

# env = input("Enter the quantus env ('production' or 'develop'): ")
# self.qqa = QuantusQA(env)

class QATests:
    def __init__(self, env, filter_conditions):
        self.env = env
        self.qqa = QuantusQA(env)
        self.init_filter(filter_conditions)
        self.wd = self.qqa.init_page(**self.filter_conditions)
        
    def init_filter(self, filter_conditions):
        self.filter_conditions = filter_conditions
    
    def __quit__(self):
        self.wd.quit()

    def testing(self):
        self.qqa.init_variables()
        
        # 초기 설정 (유니버스, 필터, 팩터)
        # backtest
        self.qqa.test_back_port(self.wd, kind=0, **self.filter_conditions)

        # 이미 설정이 완료되었을 때
        # 10분위 테스트
        self.qqa.check_alert(self.wd)
        self.wd.get(f"{self.qqa.url}/backtest/backtest/decile")
        self.qqa.get_result(self.wd, kind=2)
        
        # 이미 설정이 완료되었을 때
        # 포트 추출
        self.qqa.check_alert(self.wd)
        self.wd.get(f"{self.qqa.url}/port/port")
        self.qqa.get_result(self.wd, kind=1)
        
        # gauges
        self.qqa.variables["gauges"] = self.qqa.gauges
        
        
    def single_test(self, kind):
        self.qqa.init_variables()
        self.qqa.test_back_port(self.wd, kind=kind, **self.filter_conditions)
        
        # gauges
        self.qqa.variables["gauges"] = self.qqa.gauges

        
    def upload(self):
        variables_list = [self.qqa.variables]
        result_df = pd.DataFrame(variables_list).astype("str")
        
        if self.env == "dev" or self.env == "develop":
            db.engine_upload(upload_df=result_df, table_name="qa_test_results_dev")
        elif self.env == "prod" or self.env == "production":
            db.engine_upload(upload_df=result_df, table_name="qa_test_results_prod")
        else:
            raise AttributeError("올바른 환경을 입력하세요. ('prod' or 'dev')")