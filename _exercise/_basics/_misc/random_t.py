from numpy import random
import matplotlib.pyplot as plt
import seaborn as sns

def normal_distx():
    random.seed(2)
    x = random.normal(3, 1, 100)
    y = random.normal(150, 40, 100) / x

    plt.scatter(x, y)
    plt.show()


def norm_dist():
    sns.distplot(random.normal(size=1000), hist=False)
    plt.show()


if __name__ == "__main__":
    norm_dist()
