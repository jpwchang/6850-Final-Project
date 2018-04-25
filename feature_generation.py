################################################################################
#
# Utilities for generating feature vectors for nodes
#
################################################################################

class random_vector:
    """
    Produce a random feature vector of length given by parameter "size", by
    sampling from the given random distribution dist. dist should be a
    SciPy random variable object.
    """
    def __init__(self, size, dist, **kwargs):
        self.size = size,
        self.dist = dist
        self.kwargs = kwargs

    def __call__(self):
        return self.dist.rvs(size=self.size, **self.kwargs)