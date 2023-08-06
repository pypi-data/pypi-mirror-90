@njit
def hierarchy(edges):
    """Compute clusters from the output of raw_tomato
    
    Parameters
    ----------
    edges
        output of raw_tomato
    tau : float
        persistence gap
    keep_cluster_labels : bool
        if False, converts the labels to make them contiguous and start from 0
    
    Returns
    -------
    clusters : np.ndarray
        level zero clusters
    tree : list of (float, int, int)
        binary tree with weights
    """
    edges = sorted(edges)
    n = len(edges)
    clusters_ = clusters(edges, 0, keep_cluster_labels=False)
    forest = list(range(clusters_.max() + 1))
    
    last = None
    for pos, (p, a, b) in enumerate(edges):
        if p == 0 : continue
        if np.isinf(p):
            if last is None:
                last = len(forest) + 1
                forest.append(new)
            new = last
        else:
            new = len(forest) + 1
            forest.append(new)
        forest[_find(forest, clusters_[a])] = new
        forest[_find(forest, clusters_[b])] = new
     for i in range(len(forest)):
        _find(forest, i)
   
 
    return forest
