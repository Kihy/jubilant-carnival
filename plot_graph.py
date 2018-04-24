import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
def plot_pie(labels,sizes,explode=None, startangle=90):
    plt.style.use('ggplot')
    cs=cm.Set1(np.arange(len(labels))/float(len(labels)))

    plt.pie(sizes,labels=labels,explode=explode,autopct='%1.1f%%',startangle=startangle,colors=cs,pctdistance=0.85, labeldistance=1.1)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis('equal')
    # plt.tight_layout()
    plt.show()
