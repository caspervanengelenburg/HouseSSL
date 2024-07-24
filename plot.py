import networkx as nx
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
import numpy as np
import cv2

from constants import CMAP_RPLAN


def plot_shapes(ax, polygons, colors, **kwargs):

    for poly, color in zip(polygons, colors):
        plot_polygon(ax, Polygon(poly), color=color, **kwargs)


# Plot a floor plan graph
def plot_graph(G, ax,
               c_node='black', c_edge='black',  # coloring
               dw_edge=False, pos=None,  # edge type and node positioning
               node_size=10, edge_size=10,
               shapes=None, **kwargs):  # node and edge sizes

    """
    Plots the topological graph structure of a floor plan.
    Nodes can be colored based on the room category;
    Two possible edge types (if you want to show them in the first place):
    1) access connectivity (passage) e.g. by door; 2) adjacency e.g. by wall;
    Node positions are in 2D and could be for example the room centroids.
    """

    # Determine node position (if None is given)
    if pos is None:
        pos = nx.spring_layout(G, seed=7)  # random position for the nodes

    if shapes is not None:
        for poly, cat in zip(shapes):
            plot_polygon(ax, Polygon(poly), color=np.array(CMAP_RPLAN(cat)).reshape(1, 4), **kwargs)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=c_node, ax=ax)

    # Draw edges
    if dw_edge:

        # Door connections
        edges = [(u, v) for (u, v, d) in G.edges(data="door") if int(d) == 1]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=c_edge,
                               width=edge_size, ax=ax)

        # Adjacent connections
        edges = [(u, v) for (u, v, d) in G.edges(data="door") if int(d) == 0]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=c_edge,
                               width=edge_size, style="dashed", ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, edge_color=c_edge,
                               width=edge_size, ax=ax)


def plot_graph_msd(G, ax, c_node='black', c_edge=['white']*4, dw_edge=False, pos=None, node_size=10,
               edge_size=10):

    """
    Plots the adjacency or access graph of a floor plan's corresponding graph structure.
    """

    # position
    if pos is None:
        pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=c_node, ax=ax)

    # edges
    if dw_edge:
        epass = [(u, v) for (u, v, d) in G.edges(data=True) if d["connectivity"] == 'passage']
        edoor = [(u, v) for (u, v, d) in G.edges(data=True) if d["connectivity"] == 'door']
        efront = [(u, v) for (u, v, d) in G.edges(data=True) if d["connectivity"] == 'entrance']
        # red full for passage, red dashed for door, yellow dashed for front
        nx.draw_networkx_edges(G, pos, edgelist=epass, edge_color=c_edge[1],
                               width=edge_size, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edoor, edge_color=c_edge[2],
                               width=edge_size, style="dashed", ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=efront, edge_color=c_edge[3],
                               width=edge_size, style="-.", ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, edge_color=c_edge[0],
                               width=edge_size, ax=ax)

    ax.axis('off')


def plot_polygon(ax, poly, label=None, **kwargs):
    if poly.geom_type == 'MultiPolygon':
        for subpoly in poly:
            x, y = subpoly.exterior.xy
            ax.fill(x, y, label=label, **kwargs)
    elif poly.geom_type == 'Polygon':
        x, y = poly.exterior.xy
        ax.fill(x, y, label=label, **kwargs)
    else:
        raise NotImplementedError
    return


# Custom figure set up (instead of repeating everything all the time)
def set_figure(nc, nr,
               fs=10,
               fs_title=7.5,
               fs_legend=10,
               fs_xtick=3,
               fs_ytick=3,
               fs_axes=4,
               ratio=1,
               fc='black',
               aspect='equal'):
    """
    Custom figure setup function that generates a nicely looking figure outline.
    It includes "making-sense"-fontsizes across all text locations (e.g. title, axes).
    You can always change things later yourself through the outputs or plt.rc(...).
    """

    fig, axs = plt.subplots(nc, nr, figsize=(fs*nr*ratio, fs*nc))
    fig.set_facecolor(fc)

    try:
        axs = axs.flatten()
        for ax in axs:
            ax.set_facecolor(fc)
            ax.set_aspect(aspect)
    except:
        axs.set_facecolor(fc)
        axs.set_aspect(aspect)

    plt.rc("figure", titlesize=fs*fs_title)
    plt.rc("legend", fontsize=fs*fs_legend)
    plt.rc("xtick", labelsize=fs*fs_xtick)
    plt.rc("ytick", labelsize=fs*fs_ytick)
    plt.rc("axes", labelsize=fs*fs_axes, titlesize=fs*fs_title)

    return fig, axs


def im_convert(img, mean=0.5, std=0.5):
    img = img.cpu().clone().detach().numpy()
    img = img.transpose(1,2,0) #swap around dimensions: color should be in the back (3rd dimension instead of 1st)
    img = np.array([mean, mean, mean]) + img*np.array([std, std, std]) #transform the image to have mean and std similar to before
    img = img.clip(0, 1)
    return img


def plotting_triplets(anc, pos, neg, nr_triplets=9, loss=None, **kwargs):

    # setting figure
    nr_rows  = np.sqrt(nr_triplets).astype(int)
    _, axs = set_figure(nr_rows, nr_rows, ratio=3, **kwargs)

    for i in range(nr_triplets):
        img_triplet = cv2.hconcat([im_convert(data[i]) for data in [anc, pos, neg]])
        axs[i].imshow(img_triplet)
        if loss == None:
            axs[i].set_title("Anchor | Positive | Negative")
        else:
            axs[i].set_title(f"Anchor | Positive | Negative\n"
                                f"Loss:{loss[i]:3.6f}", color = ("g" if loss[i] <= 0 else "r"))
        axs[i].axis("off")