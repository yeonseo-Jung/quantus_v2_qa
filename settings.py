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
0: "한국"
1: "미국"
2: "KOSPI"
3: "KOSDAQ"
'''
universe = 1

# filters & sectors
removed_filters = []
removed_sectors = []

# 팩터선택 /backtest/factors, /port/factors
'''
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
 '퀄리티 팩터': {'unavailable': [],
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
  42: '차입금비율',
  43: '배당성향',
  44: '주주환원성향'},
 '가격 팩터': {'unavailable': ['평균 모멘텀', '개인순매수대금', '기관순매수대금', '외국인순매수대금'],
  45: '1개월 모멘텀',
  46: '3개월 모멘텀',
  47: '6개월 모멘텀',
  48: '12개월 모멘텀',
  49: '베타',
  50: '베타 (60일)',
  51: '절대값 베타',
  52: '절대값 베타 (60일)',
  53: 'Turnover Rate'},
 '성장성 팩터': {'unavailable': [],
  54: '순이익성장률 (QoQ)',
  55: '순이익성장률 (YoY)',
  56: '영업이익성장률 (QoQ)',
  57: '영업이익성장률 (YoY)',
  58: '매출총이익성장률 (QoQ)',
  59: '매출총이익성장률 (YoY)',
  60: '매출액성장률 (QoQ)',
  61: '매출액성장률 (YoY)',
  62: '자산성장률 (QoQ)',
  63: '자산성장률 (YoY)',
  64: '자본성장률 (QoQ)',
  65: '자본성장률 (YoY)',
  66: 'GP/A성장률 (QoQ)',
  67: 'GP/A성장률 (YoY)',
  68: '영업이익 / 차입금 성장 (YoY)',
  69: '영업이익 / 차입금 성장 (QoQ)',
  70: 'Earning Acceleration (YoY)',
  71: 'Earning Acceleration (QoQ)'}}
  '''
factors = [1, 2, 3, 4]

# 백테스트 설정, 트레이딩 설정 (/backtest/backtest, /port/port)
conditions = {
    "init_amounts": 2000,
    "fees": 1, # %(퍼센트)
    "stock_counts": 12,
    "stop_loss": 13, # %(퍼센트)
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