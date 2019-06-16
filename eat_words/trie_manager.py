
import sys
import os
import cPickle as pickle

#
# Helper functions.
#
def _read(fname):
    """Load and return serialized trie from file.
    """
    b, e = os.path.splitext(fname)
    f = b + '.dat'

    with open(f, 'r') as fo:
        val = pickle.load(fo)

    # Done.
    return val


def _write(fname, val):
    """
    Write supplied trie to file.
    """
    b, e = os.path.splitext(fname)
    f = b + '.dat'

    with open(f, 'w') as fo:
        pickle.dump(val, fo)

    # Done.


########################################################

class DawgNode():
    """This class represents a node in the directed acyclic word graph (DAWG). It has a list of edges
    to other nodes. It has functions for testing whether it is equivalent to another node. Nodes are
    equivalent if they have identical edges, and each identical edge leads to identical states. The
    __hash__ and __eq__ functions allow it to be used as a key in a python dictionary.
    """
    NextId = 0

    def __init__(self):
        self.id = DawgNode.NextId

        DawgNode.NextId += 1

        self.final = False
        self.edges = {}


    def __str__(self):
        arr = []
        if self.final:
            arr.append('1')
        else:
            arr.append('0')

        for (label, node) in self.edges.iteritems():
            arr.append( label )
            arr.append( str(node.id) )

        return '_'.join(arr)


    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()



class Dawg(object):
    """DAWG class
    """

    def __init__(self):
        self._edge_count = None

        self.previousWord = ''
        self.root = DawgNode()

        # List of nodes that have not been checked for duplication.
        self.uncheckedNodes = []

        # List of unique nodes that have been checked for duplication.
        self.minimizedNodes = {}

        # Done.



    def insert_words(self, word_list):
        """Insert list of words into DAWG structure.
        Do not expect to add or remove words after this call.
        """
        word_list.sort()

        for w in word_list:
            self._insert(w)

        self.finish()

    def _insert(self, word):
        """Add new word to DAWG structure.
        Raise error if not in alphabetical order versus words already inserted.
        """
        if word < self.previousWord:
            raise Exception('Words must be inserted in alphabetical order: %s, %s' % (self.previousWord, word) )

        # find common prefix between word and previous word.
        commonPrefix = 0
        for i in range( min( len(word), len(self.previousWord) ) ):
            if word[i] != self.previousWord[i]:
                break
            commonPrefix += 1

        # Check the uncheckedNodes for redundant nodes, proceeding from last
        # one down to the common prefix size. Then truncate the list at that point.
        num_redundant = self._minimize(commonPrefix)

        # Add the suffix, starting from the correct node mid-way through the graph.
        if len(self.uncheckedNodes) == 0:
            node = self.root
        else:
            node = self.uncheckedNodes[-1][2]

        for letter in word[commonPrefix:]:
            nextNode = DawgNode()
            node.edges[letter] = nextNode
            self.uncheckedNodes.append( (node, letter, nextNode) )
            node = nextNode

        node.final = True
        self.previousWord = word

        # Done.
        return num_redundant

    def _minimize(self, downTo):
        self._edge_count = None

        # Proceed from the leaf up to a certain point
        num_redundant = 0
        for i in range( len(self.uncheckedNodes) - 1, downTo - 1, -1 ):
            parent, letter, child = self.uncheckedNodes[i]
            if child in self.minimizedNodes:
                # Replace the child with the previously encountered one.
                num_redundant += 1
                parent.edges[letter] = self.minimizedNodes[child]
            else:
                # Add the state to the minimized nodes.
                self.minimizedNodes[child] = child
            self.uncheckedNodes.pop()

        # Done.
        return num_redundant

    def finish(self):
        # Minimize all uncheckedNodes
        num_redundant = self._minimize(0)
        return num_redundant

    def search(self, word):
        """Check to see if word exists in current structure.
        Returns True or False.
        """
        node = self.root
        for letter in word:
            if letter not in node.edges:
                return False
            node = node.edges[letter]

        return node.final

    @property
    def node_count(self):
        return len(self.minimizedNodes)

    @property
    def edge_count(self):
        if not self._edge_count:
            self._edge_count = self._count_edges()
        return self._edge_count

    def _count_edges(self):
        count = 0
        for node in self.minimizedNodes:
            count += len(node.edges)
        return count


#########################################################

class Daggad(Dawg):
    """DAGGAD class

    Represent a given word Z as a union of a prefix X and suffix Y: Z = X + Y

    Prefix X may be empty, but suffix Y may not.

    DAGGAD is a DAWG for Z' = Y + rev(X) for all valid words Z = X + Y.

    Letters normally lowercase, however rev(.) is indicated by letters as all-caps.

    Example: all possible variants of word Z = 'apple':
    0: X = , Y = apple, Z' = apple
    1: X = a, Y = pple, Z' = ppleA
    2: X = ap, Y = ple, Z' = plePA
    3: X = app, Y = le, Z' = lePPA
    4: X = appl, Y = e, Z' = eLPPA
    """

    def __init__(self):
       super(Daggad, self).__init__()

    def variants(self, word):
        """Generator that yields all DADDAG variants of a word.
        """
        num_letters = len(word)
        for a_ix in range(num_letters):
            yield self.split_at_anchor(word, a_ix)

    def split_at_anchor(self, word, anchor):
        """Represent word Z = X + Y as Z' = Y + rev(X).
        """
        word = word.lower()

        prefix = word[:anchor]
        suffix = word[anchor:]

        variant = suffix + prefix[::-1].upper()

        return variant

    def insert_words(self, words):
        """Insert list of words into DAGGAD structure.
        Do not expect to add or remove words after this call.
        """

        # Create all words' possible anchor points.
        word_variants = []
        for w in words:
            for v in self.variants(w):
                word_variants.append(v)

        word_variants.sort()

        for w in word_variants:
            self._insert(w)

        self.finish()

        # Done.


# Another helper.
def load_daggad_dictionary(fname_words):

    fname_binary = os.path.splitext(fname_words)[0] + '.daggad.dat'

    if os.path.isfile(fname_binary):
        # Load from already-created serialized class.
        daggad = _read(fname_binary)

    else:
        # Load words into list of strings.
        with open(fname_words) as fo:
            words = fo.readlines()

        words = [w.strip().lower() for w in words]

        # Create Daggad trie.
        daggad = Daggad()
        daggad.insert_words(words)

        # Save to serialized file.
        _write(fname_binary, daggad)

    # Done.
    return daggad


###############################################################
# Testing.

if __name__ == '__main__':

    from timer import Timer

    path_module = os.path.dirname(os.path.abspath(__file__))
    path_words = os.path.join(path_module, 'data', 'words and letters')

    fname_words = 'words_zynga.txt'

    # Load words into list of strings.
    f = os.path.join(path_words, fname_words)
    with open(f) as fo:
        words = fo.readlines()

    words = [w.strip().lower() for w in words]
    # words = [words[ix] for ix in range(0, len(words), 10)]
    # words[0] = 'apple'

    print('Words loaded: %d' % len(words))


    # with Timer('Create DAWG  '):
        # dawg = Dawg()
        # dawg.insert_words(words)

    # with Timer('Create DAGGAD'):
        # daggad = Daggad()
        # daggad.insert_words(words)

    with Timer('Read DAWG'):
        f = 'trie_dawg'
        dawg = read(f)

    with Timer('Read DAGGAD'):
        f = 'trie_daggad'
        daggad = read(f)


    words_check = words
    with Timer('Search DAWG  '):
        for w in words_check:
            val = dawg.search(w)
            if not val:
                raise Exception('Unable to find word: %s' % w)

    with Timer('Search DAGGAD'):
        for w in words_check:
            val = daggad.search(w)
            if not val:
                raise Exception('Unable to find word: %s' % w)

    w = 'aasdsadsa'
    val = dawg.search(w)
    assert(not val)


    w = 'apple'
    val = dawg.search(w)
    assert(val)
    val = daggad.search(w)
    assert(val)

    w = 'plePA'
    val = daggad.search(w)
    assert(val)
