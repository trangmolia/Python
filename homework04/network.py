from igraph import Graph, plot
import numpy

from api import get_friends


def get_network(user_id, as_edgelist=True):
    user_friends = get_friends(user_id, fields='sex')

    # adja_list = adjacency list - the same with adja_matrix
    adja_list = []
    adja_matrix = numpy.zeros((len(user_friends), len(user_friends)), dtype=int)

    for i in range(len(user_friends)):
        fr_of_fr = user_friends[i]
        friends = get_friends(fr_of_fr['id'], fields='sex')
        if friends is not None:
            for j in range(i + 1, len(user_friends)):
                if user_friends[j] in friends:
                    if as_edgelist:
                        adja_list.append((i, j))
                    else:
                        adja_matrix[i][j] = 1
                        adja_matrix[j][i] = 1

    if as_edgelist:
        return adja_list

    return adja_matrix


def plot_graph(user_id):
    fr_sex = get_friends(user_id, fields='sex')
    graph = get_network(user_id, as_edgelist=True)

    vertices = []
    for i in range(len(fr_sex)):
        vertices.append(fr_sex[i]['first_name'])

    g = Graph(vertex_attrs={'label': vertices}, edges=graph, directed=False)

    N = len(vertices)
    visual_style = {"layout": g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N ** 3,
        repulserad=N ** 3)}

    plot(g, **visual_style)
    g.simplify(multiple=True, loops=True)
    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    print(clusters)

if __name__ == '__main__':
    plot_graph(user_id=462579673)
