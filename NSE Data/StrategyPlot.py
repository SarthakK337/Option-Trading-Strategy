import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class StrategyPloter:

    def __init__(self):
        self.abb = {'c': 'Call',
                    'p': 'Put',
                    'b': 'Long',
                    's': 'Short'}

    def check_optype(self,op_type):
        if (op_type not in ['p', 'c']):
            raise ValueError("Input 'p' for put and 'c' for call!")

    def check_trtype(self, tr_type):
        if (tr_type not in ['b', 's']):
            raise ValueError("Input 'b' for Buy and 's' for Sell!")

    def payoff_calculator(self, x, op_type, strike, op_pr, tr_type, n):
        y = []
        if op_type == 'c':
            for i in range(len(x)):
                y.append(max((x[i] - strike - op_pr), -op_pr))
        else:
            for i in range(len(x)):
                y.append(max(strike - x[i] - op_pr, -op_pr))
        y = np.array(y)

        if tr_type == 's':
            y = -y
        return y * n


    def multi_plotter(self, spot_range=20, spot=100, op_list=[{'op_type': 'c', 'strike': 110, 'tr_type': 's', 'op_pr': 2, 'contract': 1},
                                                              {'op_type': 'p', 'strike': 95, 'tr_type': 's', 'op_pr': 6, 'contract': 1}],
                      save=False, file='fig.png'):
        """
        Plots a basic option payoff diagram for a multiple options and resultant payoff diagram

        Parameters
        ----------
        spot: int, float, default: 100
           Spot Price

        spot_range: int, float, optional, default: 20
           Range of spot variation in percentage

        op_list: list of dictionary

           Each dictionary must contiain following keys
           'strike': int, float, default: 720
               Strike Price
           'tr_type': kind {'b', 's'} default:'b'
              Transaction Type>> 'b': long, 's': short
           'op_pr': int, float, default: 10
              Option Price
           'op_type': kind {'c','p'}, default:'c'
              Opion type>> 'c': call option, 'p':put option
           'contracts': int default:1, optional
               Number of contracts

        save: Boolean, default False
            Save figure

        file: String, default: 'fig.png'
            Filename with extension

        Example
        -------
        op1={'op_type':'c','strike':110,'tr_type':'s','op_pr':2,'contract':1}
        op2={'op_type':'p','strike':95,'tr_type':'s','op_pr':6,'contract':1}

        import opstrat  as op
        op.multi_plotter(spot_range=20, spot=100, op_list=[op1,op2])

        #Plots option payoff diagrams for each op1 and op2 and combined payoff

        """
        x = spot * np.arange(100 - spot_range, 101 + spot_range, 0.01) / 100
        y0 = np.zeros_like(x)

        y_list = []
        for op in op_list:
            op_type = (op['op_type']).lower()
            tr_type = (op['tr_type']).lower()
            self.check_optype(op_type)
            self.check_trtype(tr_type)

            strike = op['strike']
            op_pr = op['op_pr']
            try:
                contract = op['contract']
            except:
                contract = 1
            y_list.append(self.payoff_calculator(x, op_type, strike, op_pr, tr_type, contract))


        def plotter():
            y = 0
            plt.figure(figsize=(11, 5))
            for i in range(len(op_list)):
                try:
                    contract = str(op_list[i]['contract'])
                except:
                    contract = '1'

                # label = contract + ' ' + str(self.abb[op_list[i]['tr_type'].lower()]) + ' ' + str(
                #     self.abb[op_list[i]['op_type'].lower()]) + ' ST: ' + str(op_list[i]['strike'])
                # sns.lineplot(x=x, y=y_list[i], label=label, alpha=0.5)
                y += np.array(y_list[i])

            ml = []
            for i in y_list:
                ml.append(max(i))
                ml.append(min(i))

            maxprofit = round(max(y), 2)
            maxloss = round(min(y), 2)
            RiskReward = round(-maxloss / maxprofit, 2)

            if maxprofit >= max(ml):
                maxprofit = "Unlimited"

            if maxloss<=min(ml):
                maxloss="Unlimited"

            sns.lineplot(x=x, y=y, label="Maxprofit: " + str(maxprofit), alpha=0.1, color='k', linestyle='--')
            sns.lineplot(x=x, y=y, label="MaxLoss: " + str(maxloss), alpha=0.1, color='k', linestyle='--')
            sns.lineplot(x=x, y=y, label="RiskReward: " + str(RiskReward), alpha=0.1, color='k', linestyle='--')
            sns.lineplot(x=x, y=y, label='combined', alpha=1, color='k')
            plt.axhline(color='k', linestyle='--')
            plt.axvline(x=spot, color='r', linestyle='--', label='spot price')
            plt.legend()
            plt.legend(loc='upper right')
            title = "Multiple Options Plotter"
            plt.title(title)
            plt.fill_between(x, y, 0, alpha=0.2, where=y > y0, facecolor='green', interpolate=True)
            plt.fill_between(x, y, 0, alpha=0.2, where=y < y0, facecolor='red', interpolate=True)
            plt.tight_layout()
            if save == True:
                plt.savefig(file)
            plt.show()

        plotter()
