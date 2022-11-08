from StrategyBuilder import Strategys
from StrategyPlot import StrategyPloter


a=Strategys()
# print(a.RiskReward("TCS","2022-11-24",3400,3600,2800,2600))
# print(a.CallPrice("TCS","2022-11-24",3260))

s=StrategyPloter()
Index="NIFTY"
Expiry="2022-11-10"
Expiry1="2022-11-17"
strike2= 18600
strike1= 18400
strike3= 18000
strike4= 17800
op_list=[
    {'op_type': 'C', 'strike': strike1, 'tr_type': 'S', 'op_pr': a.CallPrice(Index,Expiry,strike1),'contract': 50},
    # {'op_type': 'C', 'strike': strike2, 'tr_type': 'B', 'op_pr': a.CallPrice(Index,Expiry,strike2),'contract': 50},
    {'op_type': 'P', 'strike': strike3, 'tr_type': 'S', 'op_pr': a.PutPrice(Index,Expiry,strike3),'contract': 50},
    {'op_type': 'P', 'strike': strike4, 'tr_type': 'B', 'op_pr': a.PutPrice(Index,Expiry,strike4),'contract': 50}
]
s.multi_plotter(spot=a.StrikePrice(Index,Expiry),spot_range=3, op_list=op_list)