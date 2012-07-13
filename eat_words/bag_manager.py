
from __future__ import division, print_function, unicode_literals

import random
import collections

import data_io as io

# Static variables.
alphabet = ['a', 'b', 'c', 'd', 'e',
            'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y',
            'z', '_']


##################################################

class Bag(object):
    """
    A bag of scrabble letters.
        
    http://www.doughellmann.com/PyMOTW/collections/counter.html
    
    """

    def __init__(self, fname_definition):
        """
        Create a new Bag instance.
        Definition file includes letter frequency and points.
        """

        # Load definition.
        definition = io.read(fname_definition)

        self.letters_inside = collections.Counter()
        self.letters_removed = collections.Counter()
        self.letter_points = {}

        for L in alphabet:
            self.letters_inside[L] = definition['frequency'][L]
            self.letters_removed[L] = 0
            # self.point_value[L] = definition['points'][L]

            
        self._count_total = sum(self.letters_inside.values())

        
    @property
    def count_total(self):
        """
        Total number of letters, inside the bag plus any removed.
        """
        return self._count_total
        

    @property
    def count_inside(self):
        """
        Number of letters remaining inside the bag.
        """            
        return sum(self.letters_inside.values())
        
        
    @property
    def count_outside(self):
        """
        Number of letters removed from the bag.
        """            
        return sum(self.letters_removed.values())


    ####################################
    
    def pick_letters(self, number=1):
        """
        Remove letters at random from among those remaining in the bag.
        Count them as "removed from the bag".
        """

        if self.count_inside == 0:
            return []

        if number > self.count_inside:
            number = self.count_inside

        letters = []
        for k in range(number):
            L = self._random_letter()
            
            if not L:
                break
                
            letters.append(L)
            self.letters_inside[L] -= 1
            self.letters_removed[L] += 1
            
        # Done.
        return letters



    def _random_letter(self):
        """
        Select random letter from those available.
        """

        if self.count_inside == 0:
            return None
            
        num_rand = random.randint(1, self.count_inside)

        count = 0
        for L in self.letters_inside.elements():
            count += 1
            if count >= num_rand:
                return L

        # Should never get here??
        raise Exception('Shound never get here?')
        
        # Done.


    ###########################################
    
    def replace_letters(self, letters):
        """
        Replace one or more previously-removed letters back to the bag.
        Returned value is the count of how many letters returned to the bag.
        """

        count = 0
        for L in letters:
            # Sanity check.
            if self.letters_removed[L] == 0:
                raise Exception('Accounting error.  All letters of type "%s" should already be in the bag.' % L)

            # Decrement removal count.
            self.letters_inside[L] += 1
            self.letters_removed[L] -= 1
            count += 1


        # Done
        return count



if __name__ == '__main__':

    f = './data/words and letters/letters_zynga.yml'
    bag = Bag(f)


    print('count_inside: %d' % bag.count_inside)


    print('pick many:')
    num = 100
    letters_a = bag.pick_letters(num)
    print(len(letters_a))

    print('pick many:')
    num = 100
    letters_b = bag.pick_letters(num)
    print(len(letters_b))

    print('count_inside: %d' % bag.count_inside)


    bag.replace_letters('aaaa')
    print('count_inside: %d' % bag.count_inside)

    print(bag.pick_letters(5))
    print('count_inside: %d' % bag.count_inside)

