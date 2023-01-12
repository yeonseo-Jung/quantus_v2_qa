'''level
0: "초급"
1: "중급"
2: "고급"
'''
level = 2

'''login
0: "구글"
1: "카카오"
'''
login = 1
email = 'wjddustjsla@naver.com'
pw = 'jys1013011!'
strategy_name = None

# 유니버스 선택 (/backtest/universe, /port/universe)
'''universe
1 "한국"
2: "미국"
3: "KOSPI"
4: "KOSDAQ"
'''
universe = 1

# 기본 필터, 제외할 섹터 선택 (/backtest/universe, /port/universe)
{'기본 필터': {
  0: '금융주 제외',
  1: '지주사 제외',
  2: '관리종목 제외',
  3: '적자기업 제외',
  4: '적자기업 제외 (년간)',
  5: '중국기업 제외',
  6: 'PTP 기업 제외'
  },
 '제외할 섹터': {
  7: '건강관리',
  8: '자동차',
  9: '화장품,의류,완구',
  10: '보험',
  11: '필수 소비재',
  12: '운송',
  13: '상사,자본재',
  14: '비철,목재 등',
  15: '화학',
  16: '건설,건축관련',
  17: '에너지',
  18: '기계',
  19: '철강',
  20: '반도체',
  21: 'IT 하드웨어',
  22: '통신서비스',
  23: '증권',
  24: '디스플레이',
  25: 'IT 가전',
  26: '소매(유통)',
  27: '유틸리티',
  28: '미디어,교육',
  29: '은행',
  30: '호텔,레저서비스',
  31: '소프트웨어',
  32: '조선'
  }
}




removed_filters = [0, 1, 2, 3, 4, 5, 6]
removed_sectors = [15, 29]

# 팩터선택 /backtest/factors, /port/factors
{'가치 팩터 (Price 관련)': {'unavailable': [],
  0: '시가총액',
  1: 'PER',
  2: 'PBR',
  3: 'PSR',
  4: 'POR',
  5: 'PCR',
  6: 'PFCR',
  7: 'PRR',
  8: 'PGPR',
  9: 'PEG',
  10: 'PAR',
  11: 'PACR',
  12: 'NCAV',
  13: '배당수익률',
  14: '주주수익률'},
 '가치 팩터 (EV 관련)': {'unavailable': [],
  15: 'EV',
  16: 'EV/Net',
  17: 'EV/Sales',
  18: 'EV/EBITDA',
  19: 'EV/EBIT',
  20: 'EV/GP',
  21: 'EV/R&D',
  22: 'EV/CF',
  23: 'EV/AC'},
 '퀄리티 팩터': {'unavailable': ['배당성향', '주주환원성향'],
  24: 'ROE',
  25: 'ROA',
  26: 'GP/E',
  27: 'GP/A',
  28: 'Asset Turnover',
  29: 'GPM',
  30: 'OPM',
  31: 'NPM',
  32: 'F-score',
  33: 'R&D / 매출액',
  34: 'R&D / 매출총이익',
  35: 'R&D / 영업이익',
  36: 'R&D / 순이익',
  37: 'AC/A',
  38: 'AC/E',
  39: '변동성 (52주)',
  40: '변동성 (60일)',
  41: '영업이익 / 차입금',
  42: '차입금비율'},
 '가격 팩터': {'unavailable': ['평균 모멘텀',
   '개인순매수대금',
   '기관순매수대금',
   '외국인순매수대금',
   'Turnover Rate'],
  43: '1개월 모멘텀',
  44: '3개월 모멘텀',
  45: '6개월 모멘텀',
  46: '12개월 모멘텀',
  47: '베타',
  48: '베타 (60일)',
  49: '절대값 베타',
  50: '절대값 베타 (60일)'},
 '성장성 팩터': {'unavailable': ['Earning Acceleration (YoY)',
   'Earning Acceleration (QoQ)'],
  51: '순이익성장률 (QoQ)',
  52: '순이익성장률 (YoY)',
  53: '영업이익성장률 (QoQ)',
  54: '영업이익성장률 (YoY)',
  55: '매출총이익성장률 (QoQ)',
  56: '매출총이익성장률 (YoY)',
  57: '매출액성장률 (QoQ)',
  58: '매출액성장률 (YoY)',
  59: '자산성장률 (QoQ)',
  60: '자산성장률 (YoY)',
  61: '자본성장률 (QoQ)',
  62: '자본성장률 (YoY)',
  63: 'GP/A성장률 (QoQ)',
  64: 'GP/A성장률 (YoY)',
  65: '영업이익 / 차입금 성장 (YoY)',
  66: '영업이익 / 차입금 성장 (QoQ)'}}
factors = [0, 1, 3, 4, 8, 24, 51, 52, 53, 54, 57, 58]

# 백테스트 설정, 트레이딩 설정 (/backtest/backtest, /port/port)
conditions = {
    "init_amounts": 4000,
    "fees": 1.5, # %(퍼센트)
    "stock_counts": 12,
    "stop_loss": 16, # %(퍼센트)
    "profit": 26, # %(퍼센트)
    
    # rebalancing_period 
    # 1: "월별",
    # 2: "분기별",
    # 3: "반기별",
    # 4: "매년",
    "rebalancing_period": 2,
    
    "rebalancing_method": None,
    "rebalancing_strategy": None,
}


filter_conditions = {
    "level": level,
    "login": login,
    "email": email,
    "pw": pw,
    "strategy_name": strategy_name,
    "universe": universe,
    "removed_filters": removed_filters,
    "removed_sectors": removed_sectors,
    "factors": factors,
    "conditions": conditions,
}