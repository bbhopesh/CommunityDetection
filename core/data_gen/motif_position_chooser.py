from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.special import perm


class MotifPositionChooser(object):

    """An object to choose next position where motif should be inserted in the graph.

    Intuitively, we would want to choose position for next motif in multiple ways.
    If you want a strong community, then with high probability, you would want to choose already chosen positions.
    On the other hand, if you want dispersed motifs, with high probability, you'd want to choose positions that aren't
    chosen till now. In neutral scenario, you don't care and just want to choose positions with uniform distribution.

    """

    @abstractmethod
    def next_motif_position(self):
        """ Next position where motif should be inserted in the graph.

        :return: next position. A tuple containing node indexes where next motif should be inserted.
        """
        pass


class AbstractMotifPositionChooser(MotifPositionChooser):
    __metaclass__ = ABCMeta # Indicates that class is abstract.

    def __init__(self, graph_size, motif_size):
        """Create instance.

        :param graph_size: size of the graph.
        :param motif_size: size of the motif.
        Asserts that graph_size is greater than or equal to motif_size.

        """
        # Graph size should be greater than or equal to motif size.
        assert graph_size >= motif_size
        # Initialize.
        self.graph_size = graph_size
        self.motif_size = motif_size
        # Compute total motifs possible.
        self.motif_permutations = perm(graph_size, motif_size, exact=True)  # Calculate graph_size perm motif_size
        # Initialize a list to keep track of chosen motif positions till now
        self.chosen_motif_positions = set()


class UniformDistMotifPositionChooser(AbstractMotifPositionChooser):

    """An implementation of motif position chooser that chooses next motif position using a uniform distribution.

    On each call to next_motif_position, this implementation chooses nodes equal to motif size from a uniform distribution.
    However, there is an additional check that you don't return the same motif nodes twice e.g. if motif size is 3,
    and you have already returned (3,1,5), then you won't return it again. Some other ordering of same three nodes can
    be returned e.g. (1,5,3) can still be returned.
    """

    def __init__(self, graph_size, motif_size):
        # super class constructor call.
        super(UniformDistMotifPositionChooser, self).__init__(graph_size, motif_size)

    def next_motif_position(self):
        assert len(self.chosen_motif_positions) < self.motif_permutations, "Ran out of all different motif positions."
        # Choose motif positions.
        motif_positions = self.__raw_next_motif_position()
        # Keep choosing until you choose something new.
        while motif_positions in self.chosen_motif_positions:
            motif_positions = self.__raw_next_motif_position()
        # Add to set of chosen motif positions.
        self.chosen_motif_positions.add(motif_positions)
        # Return.
        return motif_positions

    def __raw_next_motif_position(self):
        return tuple(np.random.choice(range(self.graph_size),
                                                 size=self.motif_size,
                                                 replace=False))


class NoOverlappingVerticesPositionChooser(AbstractMotifPositionChooser):

    """This implementation makes sure that one vertex  is not chosen multiple times.

    This implementation is very similar to UniformDistMotifPositionChooser. The difference is that one vertex is not
    chosen multiple times. Every time you chooe some vertices for a motif, they are removed from the underlying distribution.
    and never returned again. In other words, a single vertex can only participate in one motif.
    """

    def __init__(self, graph_size, motif_size):
        # super class constructor call.
        super(NoOverlappingVerticesPositionChooser, self).__init__(graph_size, motif_size)
        self.possible_motif_positions = range(graph_size)

    def next_motif_position(self):
        assert len(self.possible_motif_positions) > self.motif_size, "Ran out of all different motif positions."
        motif_position = self.__raw_next_motif_position()
        for i in motif_position:
            self.possible_motif_positions.remove(i)
        return motif_position

    def __raw_next_motif_position(self):
        return tuple(np.random.choice(self.possible_motif_positions,
                                                 size=self.motif_size,
                                                 replace=False))


