# general imports
import numpy as np
import torch
from tqdm.auto import tqdm
from torch_geometric.utils import from_networkx

# embedding techniques
from sklearn.manifold import TSNE
from umap import UMAP
from utils import remove_attributes_from_graph


def normalize(mat):
    mat_n = mat - np.min(mat, axis=0)
    mat_n /= np.max(mat_n, axis=0)
    return mat_n


def get_projections(rs, dim=2, method='tsne', norm=True):

    # get projections (unnormalized)
    if method=='tsne': proj = TSNE(n_components=dim, perplexity=50, n_iter=5000).fit_transform(rs)
    elif method=='umap': proj = UMAP(n_components=dim).fit_transform(rs)
    else: raise NotImplementedError("Only TSNE ('tsne') and UMAP ('umap') are implemented.")

    # normalize if wanted
    if norm: proj = normalize(proj)

    return proj


def get_features(model, dataloader, device='cuda:0' if torch.cuda.is_available() else 'cpu'):

    ids, feats = [], []
    for i, data in tqdm(enumerate(dataloader), total=len(dataloader)):

        # extract information from batched data
        edge_index = data['edge_index'].to(device)
        x_geom = data['geometry'].float().to(device)
        x_cats = data['category'].long().to(device)
        edge_feats = data['inter-geometry'].float().to(device)
        batch = data['batch'].to(device)

        # inference; get representations
        with torch.no_grad():
            _, graph_feats = model(edge_index, x_geom, x_cats, edge_feats, batch)

        # append to lists
        feats.append(graph_feats)
        ids.append(torch.tensor(data['id']).to(device))

    # concatenate lists to tensors
    feats = torch.cat(feats, dim=0)
    ids = torch.cat(ids, dim=0)

    # return floor plan identities paired with feature vectors
    return ids, feats


def get_embeddings_gcn(graphs, model, device='cpu'):

    # set model to eval mode; no randomness
    model.eval()

    # initialize list of names and embeddings
    names, embeddings = [], []

    for graph in tqdm(graphs):

        # convert graph to pytorch geometric
        graph = from_networkx(remove_attributes_from_graph(graph, ['polygon']))

        # extract information from batched data
        edge_index = graph['edge_index'].to(device)
        x_geom = graph['geometry'].float().to(device)
        x_cats = graph['category'].long().to(device)
        edge_feats = graph['inter-geometry'].float().to(device)
        batch = torch.zeros(x_geom.size()[0], dtype=torch.int64).to(device)

        # inference; get representations
        with torch.no_grad():
            _, graph_feats = model(edge_index, x_geom, x_cats, edge_feats, batch)

        # append to lists
        embeddings.append(graph_feats)
        names.append(graph['name'])

    # concatenate embeddings list to tensor
    embeddings = torch.cat(embeddings, dim=0)

    return names, embeddings


def sample_features_distance(names, embeddings, t=0.025):

    embeddings_reduced = []
    names_reduced = []

    for name, embedding in tqdm(zip(names, embeddings), total=len(names)):
        embedding = np.array(embedding)
        if len(embeddings_reduced) == 0:
            embeddings_reduced.append(embedding)
            names_reduced.append(name)
        else:
            if np.min([np.sqrt(np.sum(np.power(embedding - f, 2))) for f in embeddings_reduced]) > t:
                embeddings_reduced.append(embedding)
                names_reduced.append(name)
            else:
                continue

    return names_reduced, np.array(embeddings_reduced)