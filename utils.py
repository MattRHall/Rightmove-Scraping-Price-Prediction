import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class data_visualizer():

    def __init__(self, dataset):
        """ Constructs data visualizer object, adding an 'Index' column at beginning """

        self.dataset = dataset
 
    def all_feature_plots(self, dependent, shape = (3,4), figsize = (8,30), remove = [], cat_type = "Boxplot", save_fig = True, verbose_titles = False):
        """ Generates subplots of features variables against dependent variable (scatter if continous, else Boxplot) """

        columns = [i for i in self.dataset.columns if i not in remove]

        fig, axes = plt.subplots(shape[0], shape[1], figsize = figsize, sharey = True, constrained_layout=True)
        for ind, ax in zip(columns, axes.flatten()):

            if self.dataset[ind].dtype == 'float64' or self.dataset[ind].dtype == 'int64':
                ax.scatter(self.dataset[ind], self.dataset[dependent])
                if verbose_titles:
                    ax.set_title(str(ind) +"\n" +" Mean:" + str(round(self.dataset[ind].mean(), 2)) + " Std:" + str(round(self.dataset[ind].std(), 2)) + " Skew:" + str(round(self.dataset[ind].skew(), 2)) + " Kurt:" + str(round(self.dataset[ind].kurtosis(), 2))               )#Mean:{self.dataset[ind].mean:.1f}, std:{self.dataset[ind].std()}, skew:{self.dataset[ind].skew()}, kurt:{self.dataset[ind].kurt()}')
                else:
                    ax.set_title(ind)
            elif self.dataset[ind].dtype == 'O':
                no_nan_col = self.dataset[ind].fillna("nan")
                if cat_type == "Scatter":
                    ax.scatter(no_nan_col, self.dataset[dependent])
                elif cat_type == "Boxplot":
                    data = []
                    ticks = []
                    for i in self.dataset[ind].unique():
                        if pd.isnull(i):
                            data.append(self.dataset[self.dataset[ind].isnull()][dependent])
                            ticks.append('nan')
                        else:
                            data.append(self.dataset[self.dataset[ind] == i][dependent])
                            ticks.append(i) 
                    ax.boxplot(data)
                    ax.set_title(ind)
                    if len(self.dataset[ind].unique()) > 5:
                        ax.set_xticklabels(ticks, rotation = 90)
                    else:
                        ax.set_xticklabels(ticks)

        #plt.tight_layout()
        if save_fig:
            plt.savefig("feature_analysis.png")
        plt.show()