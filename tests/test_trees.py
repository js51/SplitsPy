import pytest
from splitp import *


@pytest.fixture(scope='class')
def get_trees():
    matrix = [[0.95, 0.05],[0.05, 0.95]]
    initial_dist = [0.50, 0.50]
    ### Tree 1 (6 Taxon binary) ###
    T6_2 = tree(11, 2)
    T6_2.initDist = initial_dist
    T6_2.addNode(node(None, 0))
    T6_2.addNode(node(matrix, 1),  0)
    T6_2.addNode(node([[1,0],[0,1]], 2),  0)
    T6_2.addNode(node(matrix, 3),  1)
    T6_2.addNode(node(matrix, 7),  1)
    T6_2.addNode(node(matrix, 8),  2)
    T6_2.addNode(node(matrix, 4),  2)
    T6_2.addNode(node(matrix, 5),  3)
    T6_2.addNode(node(matrix, 6),  3)
    T6_2.addNode(node(matrix, 9),  4)
    T6_2.addNode(node(matrix, 10), 4)

    # 7 Taxa Tree
    num_nodes = 13
    num_bases = 4
    initial_dist = [0.25, 0.25, 0.25, 0.25]
    matrix_a = makeSubsMatrix(0.01, 4)
    matrix_b = makeSubsMatrix(0.03, 4)
    matrix_c = makeSubsMatrix(0.08, 4)
    T7_4 = tree(num_nodes, num_bases, name="7TaxonTreeA")
    T7_4.initDist = initial_dist
    T7_4.addNode(node(None, 0))  # Root Node
    T7_4.addNode(node(matrix_a, 1), 0)
    T7_4.addNode(node(matrix_a, 2), 0)
    # Internal Nodes:
    T7_4.addNode(node(matrix_b, 4), 1)
    T7_4.addNode(node(matrix_b, 6), 2)
    T7_4.addNode(node(matrix_b, 10), 6)
    # Leaves:
    T7_4.addNode(node(matrix_c, 3), 1)
    T7_4.addNode(node(matrix_c, 5), 4)
    T7_4.addNode(node(matrix_c, 7), 4)
    T7_4.addNode(node(matrix_c, 8), 2)
    T7_4.addNode(node(matrix_c, 9), 6)
    T7_4.addNode(node(matrix_c, 11), 10)
    T7_4.addNode(node(matrix_c, 12), 10)
    ###
    return [T6_2, T7_4]

def test_trivial_parsimony(get_trees):
    """ Testing that all trivial splits have parsimony of 1 """
    for tree in get_trees:
        splits = generateAllSplits(tree.get_num_taxa(), True, True)
        scores = [tree.parsimony_score(s) for s in splits]
        assert all([s == 1 for s in scores])


def test_subflats_equal(get_trees):
    for tree in get_trees:
        if tree.num_bases == 4:
            splits = generateAllSplits(tree.get_num_taxa(), trivial=False)
            patternProbs = tree.get_pattern_probabilities()
            for sp in splits[::6]:
                F = tree.flattening(sp, patternProbs)
                SF1 = tree.subflattening(tree.transformed_flattening(F))
                SF2 = tree.subflattening_alt(F)
                assert np.all(np.isclose(SF1, SF2))
