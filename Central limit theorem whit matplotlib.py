import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import shapiro, probplot
import time

class DiceExperiment:
    def __init__(self):
        self.fig, self.ax = plt.subplots(2, 3, figsize=(15, 10))
        self.trial_count = 0
        self.mean_values = []

        while True:
            self.update_plots()
            plt.pause(0.5)  # Pause for 0.5 seconds

    def roll_dice(self):
        return [random.randint(1, 6) for _ in range(7)]

    def calculate_mean(self, dice_rolls):
        return np.mean(dice_rolls)

    def update_plots(self):
        dice_rolls = self.roll_dice()
        mean_value = self.calculate_mean(dice_rolls)
        self.mean_values.append(mean_value)
        self.trial_count += 1

        self.plot_histogram()
        self.plot_qq_plot()
        self.plot_shapiro_test_result()
        self.plot_p_values()
        self.plot_original_distribution()

    def plot_histogram(self):
        ax = self.ax[0][0]
        ax.clear()
        ax.hist(self.mean_values, bins=20, range=(0.5, 6.5), alpha=0.75)
        ax.set_title('Histogram of Means')
        ax.set_xlabel('Mean Value')
        ax.set_ylabel('Frequency')
        ax.set_xticks(range(1, 7))
        ax.annotate(f'Trials: {self.trial_count}', xy=(0.7, 0.9), xycoords='axes fraction')

    def plot_qq_plot(self):
        ax = self.ax[0][1]
        ax.clear()
        probplot(self.mean_values, dist="norm", plot=ax)
        ax.set_title('QQ Plot')
        ax.annotate(f'Trials: {self.trial_count}', xy=(0.7, 0.9), xycoords='axes fraction')

    def plot_shapiro_test_result(self):
        ax = self.ax[0][2]
        ax.clear()
        ax.axis('off')

        if len(self.mean_values) >= 3:
            try:
                shapiro_stat, p_value = shapiro(self.mean_values)
                skewness = stats.skew(self.mean_values)
                kurtosis = stats.kurtosis(self.mean_values)

                ax.text(0.1, 0.8, f'Shapiro-Wilk Test:', fontsize=12)
                ax.text(0.1, 0.7, f'p-value: {p_value:.3f}', fontsize=12)
                ax.text(0.1, 0.5, f'Skewness: {skewness:.3f}', fontsize=12)
                ax.text(0.1, 0.3, f'Kurtosis: {kurtosis:.3f}', fontsize=12)
            except Exception as e:
                ax.text(0.1, 0.5, f'Shapiro-Wilk Test Error', fontsize=12)
        else:
            ax.text(0.1, 0.5, 'Insufficient data for Shapiro-Wilk test', fontsize=12)

    def plot_p_values(self):
        ax = self.ax[1][0]
        ax.clear()
        if len(self.mean_values) > 0:
            try:
                p_values = [shapiro(self.mean_values[:i])[1] for i in range(1, self.trial_count + 1)]
                ax.plot([i for i in range(1, self.trial_count + 1)], p_values)
                ax.set_title('P-values from Shapiro-Wilk Test')
                ax.set_xlabel('Trial Number')
                ax.set_ylabel('p-value')
            except Exception as e:
                ax.text(0.1, 0.5, f'Error: {str(e)}', fontsize=12)

    def plot_original_distribution(self):
        ax = self.ax[1][1]
        ax.clear()
        ax.hist(self.mean_values[:self.trial_count], bins=20, range=(0.5, 6.5), alpha=0.75)
        ax.set_title('Original Distribution of Means')
        ax.set_xlabel('Mean Value')
        ax.set_ylabel('Frequency')
        ax.set_xticks(range(1, 7))


if __name__ == "__main__":
    experiment = DiceExperiment()
