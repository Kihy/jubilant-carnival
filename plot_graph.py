import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import networkx as nx


def draw_network(G):
    # G = nx.star_graph(20)
    # pos = nx.spring_layout(G)
    # colors = range(20)
    # nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors,
    #         width=4, edge_cmap=plt.cm.Blues, with_labels=False)
    # plt.show()

    weights = []
    pos = nx.shell_layout(G)
    for i in G.edges.data("weight"):
        weights.append(i[2])
    nx.draw(G, pos, node_color=range(len(G.nodes)), edge_color=weights,
            width=4, cmap=plt.cm.Pastel1, edge_cmap=plt.cm.tab20, with_labels=False)
    for p in pos:  # raise text positions
        pos[p][1] -= 0.1
    nx.draw_networkx_labels(G, pos)
    plt.show()


def plot_tags(hash_dict, invalid_dict):
    # plots summarized hashes
    labels = []
    values = []
    explode = []
    for label, freq in hash_dict.items():
        labels.append(label)
        values.append(freq)
        if label == '#invalid':
            explode.append(0.05)
        else:
            explode.append(0)

    plt.subplot(121)
    plot_pie(labels, values, explode)
    plt.title("Frequency of tags")
    plt.suptitle("Analysis of tags excluding task with stories")
    # plots invalid hashes
    plt.subplot(122)
    plot_pie(list(invalid_dict.keys()), list(
        invalid_dict.values()), startangle=45)
    plt.title("Frequency of incorrect tags")
    plt.show()


def plot_pie(labels, sizes, explode=None, startangle=90):
    plt.style.use('ggplot')
    cs = cm.Set1(np.arange(len(labels)) / float(len(labels)))

    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
            startangle=startangle, colors=cs, pctdistance=0.85, labeldistance=1.1)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.axis('equal')
    # plt.tight_layout()


def plot_scatter_with_line(x, y, line_height=60):
    plot_scatter(x,y,"Commit Time analysis","Minutes Spent","Member",False)
    plt.axhline(line_height, ls='--', label="Recommended commit time(1 hr)")
    plt.legend()
    plt.show()

def plot_scatter(x,y,title,ylabel,xlabel,show=True):
    plt.style.use('ggplot')
    plt.scatter(x, y)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if show:
        plt.show()


def plot_stacked_bar(data, fullNames):
    plt.style.use('seaborn-poster')
    story_names = sorted(list(data.keys()))
    member_participation = [[0 for x in range(len(story_names))] for x in range(
        len(fullNames))]  # each row is a member, column is a story
    for i in range(len(story_names)):
        for j in range(len(fullNames)):
            try:
                member_participation[j][i] = data[story_names[i]][fullNames[j]]
            except:
                continue

    graphs = []
    for i in range(len(member_participation)):
        if i == 0:
            graphs.append(plt.bar(story_names, member_participation[i])[0])
        else:
            graphs.append(plt.bar(
                story_names, member_participation[i], bottom=member_participation[i - 1])[0])

    plt.legend(tuple(graphs), fullNames)
    plt.title("Bus factor Analysis")
    plt.ylabel("Time spent(minutes)")
    plt.xlabel("Story Number")
    plt.show()
