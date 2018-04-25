################################################################################
#
# Routines for edge generation logic
#
################################################################################

def threshold_edge_gen(sim, threshold):
    """
    Deterministically produce an edge between pairs based on a similarity
    threshold. If the magnitude of the similarity exceeds the threshold an edge
    is returned with sign equal to the sign of the similarity, otherwise no
    edge is returned
    """
    if abs(sim) > threshold:
        return (1 if sim > 0 else -1)
    else:
        return 0