from StrategyBuilder import Strategys , ShortIronCondor
from StrategyPlot import StrategyPloter


a=ShortIronCondor()
# print(a.RiskReward("BANKNIFTY","2022-11-10",42200,41200,42400,41000))
# print(a.CallPrice("TCS","2022-11-24",3260))

s=StrategyPloter()
Index="NIFTY"
Expiry="2022-11-10"
Expiry1="2022-11-17"
strike1= 18600
strike2= 18400
strike3= 18000
strike4= 17800
con=1

def plotter(Index,Expiry,strike1,strike2,strike3,strike4,Con):
    if Index=="NIFTY":
        Con = Con * 50
    if Index=="BANKNIFTY":
        Con = Con * 25
    op_list=[
        {'op_type': 'C', 'strike': strike1, 'tr_type': 'B', 'op_pr': a.CallPrice(Index,Expiry,strike1),'contract': Con},
        {'op_type': 'C', 'strike': strike2, 'tr_type': 'S', 'op_pr': a.CallPrice(Index,Expiry,strike2),'contract': Con},
        {'op_type': 'P', 'strike': strike3, 'tr_type': 'S', 'op_pr': a.PutPrice(Index,Expiry,strike3),'contract': Con},
        {'op_type': 'P', 'strike': strike4, 'tr_type': 'B', 'op_pr': a.PutPrice(Index,Expiry,strike4),'contract': Con}
    ]
    s.multi_plotter(spot=a.StrikePrice(Index,Expiry),spot_range=3, op_list=op_list)

plotter(Index,Expiry,strike1,strike2,strike3,strike4,con)