import random
import os
import sys

TILE_BLANK = 0
TILE_DOUBLE_LETTER = 2
TILE_TRIPLE_LETTER = 3
TILE_DOUBLE_WORD = 4
TILE_TRIPLE_WORD = 6
TILE_START = 7

DIRECTION_HORIZONTAL = 0
DIRECTION_VERTICAL = 1

tileScores = [[6,0,0,2,0,0,0,6,0,0,0,2,0,0,6],
              [0,4,0,0,0,3,0,0,0,3,0,0,0,4,0],
              [0,0,4,0,0,0,2,0,2,0,0,0,4,0,0],
              [2,0,0,4,0,0,0,2,0,0,0,4,0,0,2],
              [0,0,0,0,4,0,0,0,0,0,4,0,0,0,0],
              [0,3,0,0,0,3,0,0,0,3,0,0,0,3,0],
              [0,0,2,0,0,0,2,0,2,0,0,0,2,0,0],
              [6,0,0,2,0,0,0,7,0,0,0,2,0,0,6],
              [0,0,2,0,0,0,2,0,2,0,0,0,2,0,0],
              [0,3,0,0,0,3,0,0,0,3,0,0,0,3,0],
              [0,0,0,0,4,0,0,0,0,0,4,0,0,0,0],
              [2,0,0,4,0,0,0,2,0,0,0,4,0,0,2],
              [0,0,4,0,0,0,2,0,2,0,0,0,4,0,0],
              [0,4,0,0,0,3,0,0,0,3,0,0,0,4,0],
              [6,0,0,2,0,0,0,6,0,0,0,2,0,0,6]]

letterScores = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
                'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 
                'q': 10,'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
                'y': 4, 'z': 10}

letterDistributions = {'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12,'f': 2, 'g': 3,
                       'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2, 'n': 6,
                       'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6, 'u': 4,
                       'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1}

class Game:
    __letterBag = None
    __currentPlayer = None
    __players = None
    __board = None
    __dictionary = None
    __isNewGame = True


    def getIsNewGame(self):
        """Get the new game status."""
        return self.__isNewGame

    def setIsNewGame(self, value):
        """Set the new game status."""
        self.__isNewGame = value

    isNewGame = property(getIsNewGame, setIsNewGame)


    def getBoard(self):
        """Get a reference to the game board."""
        return self.__board

    def setBoard(self, value):
        """Set the game board reference."""
        self.__board = value

    board = property(getBoard, setBoard)


    def getLetterBag(self):
        """Get a reference to the letter bag."""
        return self.__letterBag

    def setLetterBag(self, value):
        """Set the letter bag reference."""
        self.__letterBag = value

    letterBag = property(getLetterBag, setLetterBag)


    def getPlayers(self):
        """Get a reference to the list of players."""
        return self.__players

    def setPlayers(self, value):
        """Set the list of players reference."""
        self.__players = value

    players = property(getPlayers, setPlayers)


    def getCurrentPlayer(self):
        """Get the current player index.  Index is 0-based."""
        return self.__currentPlayer

    def setCurrentPlayer(self, value):
        """Set the current player index."""
        self.__currentPlayer = value

    currentPlayer = property(getCurrentPlayer, setCurrentPlayer)


    def getDictionary(self):
        """Get a reference to the word dictionary."""
        return self.__dictionary

    def setdictionary(self, value):
        """Set the word dictionary reference."""
        self.__dictionary = value

    dictionary = property(getDictionary, setdictionary)


    def __init__(self, playerCount):
        """Set up default game state."""
        self.__board = Board()
        self.__letterBag = LetterBag()
        self.__players = [Player(self) for i in range(0, playerCount)]
        self.__currentPlayer = playerCount - 2
        self.__dictionary = WordDictionary()


    def nextMove(self):
        """Select the next player and create a move for that player."""

        # Wrap-around the player index if necessary
        if self.__currentPlayer == len(self.__players) - 1:
            self.__currentPlayer = 0
        else:
            self.__currentPlayer += 1

        print("Creating move for player " + str(self.__currentPlayer))

        return Move(self, self.__players[self.__currentPlayer])


class LetterBag:
    __letters = None


    def __init__(self):
        # Get a copy of the letter distribution dictionary
        self.__lettersRemaining = {}

        for letter in letterDistributions:
            self.__lettersRemaining[letter] = letterDistributions[letter]


    def getRemainingLetterCount(self):
        """Get the number of letters left in the bag."""
        remaining = 0

        for letter in self.__lettersRemaining:
            remaining += self.__lettersRemaining[letter]

        return remaining


    def takeRandomLetter(self):
        """Get a random letter from the letter bag and reduce that letter's
        remaining count by 1."""

        # Create a string containing a list of all characters that have at least
        # one letter remaining
        choices = ""

        for letter in self.__lettersRemaining:
            if self.__lettersRemaining[letter] > 0:
                choices = choices + letter

        # Choose random letter from the list of choices
        letter = random.choice(choices)

        self.__lettersRemaining[letter] = self.__lettersRemaining[letter] - 1
        return letter


class WordDictionary:
    __words = None


    def __init__(self):
        """"Loads the dictionary file."""
        file = open(os.path.dirname(sys.argv[0]) + "\\dictionary.txt", "r")
        self.__words = file.readlines()


    def isWord(self, word):
        """Check if the supplied word exists in the dictionary."""
        for i in self.__words:
            if i.replace('\n', '') == word:
                print("Word '" + word + "' is valid")
                return True

        print("Word '" + word + "' is not valid.")
        return False


class Board:
    __tiles = None
    __tileScores = None


    def getTiles(self):
        return self.__tiles

    def setTiles(self, value):
        self.__tiles = value

    tiles = property(getTiles, setTiles)


    def __init__(self):
        # Initialise tile array
        self.__tiles = [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

        # Copy tile scores
        self.__tileScores = []

        for row in tileScores:
            self.__tileScores.append([i for i in row])


    def kprint(self):
        """Print out the current board state in a vaguely user-friendly format.

        Empty tiles are represented by '.'.  Tiles with letters are represented
        by the letter.  Tiles with bonuses that have not been claimed are
        represented by the number of the bonus given in the relevant constants
        at the top of the script.
        """

        output = ""

        for y in range(0, len(self.__tiles)):
            for x in range(0, len(self.__tiles[y])):
                # Get the letter at the current co-ordinates
                item = self.__tiles[y][x]

                if item == ' ':
                    # Try getting a tile score as there is no letter placed
                    item = str(self.__tileScores[y][x])

                    if item == '0': item = '.'

                output += item
            output += '\n'

        print(output)


    def getLetter(self, x, y):
        """Get the letter at the specified co-ordinates."""

        # Ensure that the co-ordinates fit in the grid
        if len(self.__tiles) < y:
            raise ValueError("Read outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Read outside vertical grid at x co-ord " + str(x))

        return(self.__tiles[y][x])


    def placeLetter(self, letter, x, y):
        """Place the supplied letter at the specified co-ordinates."""

        # Ensure that the letter fits in the grid
        if len(self.__tiles) < y:
            raise ValueError("Letter outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Letter outside vertical grid at x co-ord " + str(x))
        if self.__tiles[y][x] != ' ':
            raise ValueError("Grid not empty at co-ords " + str(x) + "," + str(y))

        # Update the grid
        self.__tiles[y][x] = letter


    def clearLetter(self, x, y):
        """Blank the tile at the specified co-ordinates."""

        # Ensure that the letter fits in the grid
        if len(self.__tiles) < y:
            raise ValueError("Letter outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Letter outside vertical grid at x co-ord " + str(x))

        self.__tiles[y][x] = ' '


    def clearTileScore(self, x, y):
        """Remove the tile score at the specified co-ordinates so that it does
        not alter future scores."""
        self.__tileScores[y][x] = 0


    def getTileScore(self, x, y):
        """Get the tile score at the specified co-ordinates."""
        return self.__tileScores[y][x]


    def getHorizontalWordLength(self, x, y):
        """Get the length of the word starting at x,y."""

        length = 0

        while x < len(self.__tiles[y]) and self.__tiles[y][x] != ' ':
            x += 1
            length += 1

        return(length)


    def getVerticalWordLength(self, x, y):
        """Get the length of the word starting at x,y."""

        length = 0

        while y < len(self.__tiles) and self.__tiles[y][x] != ' ':
            y += 1
            length += 1

        return(length)


    def getHorizontalWordStart(self, x, y):
        """Get the co-ords of the first letter in the word that contains the
        given co-ordinates."""

        while x > 0 and self.__tiles[y][x - 1] != ' ':
            x -= 1

        return({'x': x, 'y': y})


    def getVerticalWordStart(self, x, y):
        """Get the co-ords of the first letter in the word that contains the
        given co-ordinates."""

        while x > 0 and self.__tiles[y - 1][x] != ' ':
            y -= 1

        return({'x': x, 'y': y})


    def getHorizontalWord(self, x, y, length):
        """Get the horizontal word starting at x,y of length 'length'."""
        word = ""
        for i in range(x, x + length):
            word = word + self.getLetter(i, y)

        return word


    def getVerticalWord(self, x, y, length):
        """Get the vertical word starting at x,y of length 'length'."""
        word = ""
        for i in range(y, y + length):
            word = word + self.getLetter(x, i)

        return word


    def scoreHorizontalWord(self, x, y, length):
        """Score the horizontal word starting at x,y of length 'length'."""

        # If the length of the word is 1, the score is 0
        if length == 1:
            return 0

        # Score the word
        isDoubleWord = False
        isTripleWord = False
        isStart = False
        score = 0

        # Score individual letters
        for i in range(x, x + length):
            tileScore = self.scoreTile(i, y)
            score += tileScore['score']

            isDoubleWord = isDoubleWord or tileScore['isDoubleWord']
            isTripleWord = isTripleWord or tileScore['isTripleWord']
            isStart = isStart or tileScore['isStart']

        # Multiply any word scores
        if isDoubleWord:
            score *= 2
        if isTripleWord:
            score *= 3
        if isStart:
            score *= 2

        return(score)


    def scoreVerticalWord(self, x, y, length):
        """Score the vertical word starting at x,y of length 'length'."""

        # If the length of the word is 1, the score is 0
        if length == 1:
            return 0

        # Score the word
        isDoubleWord = False
        isTripleWord = False
        isStart = False
        score = 0

        # Score individual letters
        for i in range(y, y + length):
            tileScore = self.scoreTile(x, i)
            score += tileScore['score']

            isDoubleWord = isDoubleWord or tileScore['isDoubleWord']
            isTripleWord = isTripleWord or tileScore['isTripleWord']
            isStart = isStart or tileScore['isStart']

        # Multiply any word scores
        if isDoubleWord:
            score *= 2
        if isTripleWord:
            score *= 3
        if isStart:
            score *= 2

        return(score)


    def scoreTile(self, x, y):
        """Get the score represented by the tile at the given co-ordinates.

        Should be called after the letter has been placed but before the bonuses
        have been wiped from the board in order to allow bonuses to be
        calculated.

        Returns a dictionary containing the keys 'score' (score for the tile),
        'isDoubleWord' (indicates that the tile contains a double-word score),
        'isTripleWord' (indicates that the tile contains a triple-word score)
        and 'isStart' (indicates that the tile is the starting tile).
        """

        isDoubleWord = False
        isTripleWord = False
        isStart = False

        # Get the score for the letter
        score = letterScores[self.getLetter(x, y)]

        # Does the tile have a bonus?
        tile = self.__tileScores[y][x]
        if tile == TILE_DOUBLE_LETTER:
            score *= 2
        elif tile == TILE_TRIPLE_LETTER:
            score *= 3
        elif tile == TILE_DOUBLE_WORD:
            isDoubleWord = True
        elif tile == TILE_TRIPLE_WORD:
            isTripleWord = True
        elif tile == TILE_START:
            isStart = True

        val = {'score': score,
               'isDoubleWord': isDoubleWord,
               'isTripleWord': isTripleWord,
               'isStart': isStart}
               
        return(val)


class Player:
    __score = 0
    __tiles = None
    __game = None


    def __init__(self, game):
        """Initial setup.  Populates player's rack with random letters."""

        self.__game = game

        # Populate tiles with random letters
        self.__tiles = [game.letterBag.takeRandomLetter() for i in range(0, 7)]

        # TODO: REMOVE THIS
        self.__tiles.extend(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                             'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                             'y', 'z'])


    def getTiles(self):
        return self.__tiles

    def setTiles(self, value):
        self.__tiles = value

    tiles = property(getTiles, setTiles)


    def getScore(self):
        return self.__score

    def setScore(self, value):
        self.__score = value

    score = property(getScore, setScore)


    def addScore(self, score):
        """Adds the supplied score to the player's score."""
        self.__score += score


class Move:
    __game = None
    __player = None
    __score = 0
    __placements = None
    __viableLetters = None


    def getScore(self):
        return self.__score

    def setScore(self, value):
        self.__score = value

    score = property(getScore, setScore)


    def __init__(self, game, player):
        self.__game = game
        self.__player = player
        self.__placements = []
        self.__viableLetters = []

        for i in player.tiles:
            self.__viableLetters.append(i)


    def placeLetter(self, letter, x, y):
        """Places a letter from the player's rack into the grid.

        The player's rack is not altered until the move is committed.  However,
        the board is changed and placed into an indeterminate state until either
        commit() or rollback() is called.
        """

        # Ensure that the letter is in the list of viable letters and, if so, remove it
        try: self.__viableLetters.remove(letter)
        except ValueError:
            raise ValueError("Player does not possess letter '" + letter + "'")

        # Update the grid
        self.__game.board.placeLetter(letter, x, y)

        # Remember the placement
        self.__placements.append({'letter': letter, 'x': x, 'y': y})


    def commit(self):
        """Try to commit the move to the game."""

        words = self.collateWords()

        # Check that the move is valid
        try:
            self.validate(words)
        except ValueError:
            self.rollback()
            raise

        # Calculate the score of the move and add it to the player's score
        self.__score = self.getScore(words)
        self.__player.addScore(self.__score)

        self.clearTileScores()
        self.updateRack()

        # Remember that we are no longer on the first move
        self.__game.isNewGame = False


    def rollback(self):
        """Restores the grid to its previous state by removing all letters
        placed in this move.

        Restores the viable letters from the placements.
        """

        for i in self.__placements:
            self.__game.board.clearLetter(i['x'], i['y'])
            self.__viableLetters.append(i['letter'])


    def updateRack(self):
        """Updates the player's rack by removing all placed letters."""
        for i in self.__placements:
            self.__player.tiles.remove(i['letter'])


    def clearTileScores(self):
        """Clears the scores for all board positions involved in this move to
        ensure that they are not counted in future moves."""
        for i in self.__placements:
            self.__game.board.clearTileScore(i['x'], i['y'])


    def collateWords(self):
        """Collate a list of all words created by this move.

        Returns a dictionary containing the words as keys and a second
        dictionary as each value.

        The second dictionary contains the keys 'length' (the length of the
        word), 'x' (the x co-ordinate of the start of the word), 'y' (the y
        co-ordinate of the start of the word) and 'direction' (either
        DIRECTION_HORIZONTAL or DIRECTION_VERTICAL).
        """

        words = {}

        for i in self.__placements:

            # Get horizontal word from this placement
            coords = self.__game.board.getHorizontalWordStart(i['x'], i['y'])
            x = coords['x']
            y = coords['y']

            length = self.__game.board.getHorizontalWordLength(x, y)
            word = self.__game.board.getHorizontalWord(x, y, length)

            if length > 1:
                words[word] = {'length': length,
                               'x': x,
                               'y': y,
                               'direction': DIRECTION_HORIZONTAL}

            # Get vertical word from this placement
            coords = self.__game.board.getVerticalWordStart(i['x'], i['y'])
            x = coords['x']
            y = coords['y']

            length = self.__game.board.getVerticalWordLength(x, y)
            word = self.__game.board.getVerticalWord(x, y, length)

            if length > 1:
                words[word] = {'length': length,
                               'x': x,
                               'y': y,
                               'direction': DIRECTION_VERTICAL}

        return words


    def validate(self, words):
        """Ensure that all words created by this move are valid."""
        self.validatePlacements()

        for word in words:
            if not self.__game.dictionary.isWord(word):
                raise ValueError("Word '" + word + "' is not valid.")

        return True


    def validatePlacements(self):
        """Check that all placements are in a row, are contiguous, and are
        somehow connected to the existing body of tiles."""

        # Special case for single placements
        if len(self.__placements) == 1:

            # Check that tile connects to a populated tile on at least one side
            x = self.__placements[0]['x']
            y = self.__placements[0]['y']

            if x > 0 and self.__game.board.getLetter(x - 1, y) != ' ':
                return
            elif x < len(self.__game.board.tiles[y]) and self.__game.board.getLetter(x + 1, y) != ' ':
                return
            elif y > 1 and self.__game.board.getLetter(x, y - 1) != ' ':
                return
            elif y < len(self.__game.board.tiles) and self.__game.board.getLetter(x, y + 1) != ' ':
                return

            raise ValueError("Placements do not connect with the existing letters.")

        # If this is the first move, ensure that tiles cross the start point
        if self.__game.isNewGame:
            startTileCheck = False
            for i in self.__placements:
                if self.__game.board.getTileScore(i['x'], i['y']) == TILE_START:
                    startTileCheck = True
                    break
            if not startTileCheck:
                raise ValueError("Tiles not placed across start tile.")

        # Check if placements are on a straight line
        xTotal = 0
        yTotal = 0
        direction = DIRECTION_HORIZONTAL

        for i in self.__placements:
            xTotal += i['x']
            yTotal += i['y']

        if xTotal == self.__placements[0]['x'] * len(self.__placements):
            direction = DIRECTION_VERTICAL
        elif yTotal == self.__placements[0]['y'] * len(self.__placements):
            direction = DIRECTION_HORIZONTAL
        else:
            raise ValueError("Tiles not placed in straight line.")

        # Check that there are no gaps between the tiles
        sortedPlacements = []

        if direction == DIRECTION_HORIZONTAL:

            # Sort the placements so that we know the left and right edges of
            # the word.  Scan for gaps in any tiles between
            y = self.__placements[0]['y']

            for i in self.__placements:
                sortedPlacements.append(i['x'])

            sortedPlacements.sort()

            for i in range(sortedPlacements[0], sortedPlacements[len(sortedPlacements) - 1]):
                if self.__game.board.getLetter(i, y) == ' ':
                    raise ValueError("Placed word contains gaps.")
        else:

            # Sort the placements so that we know the top and bottom edges of
            # the word.  Scan for gaps in any tiles between
            x = self.__placements[0]['x']
            for i in self.__placements:
                sortedPlacements.append(i['y'])

            sortedPlacements.sort()

            for i in range(sortedPlacements[0], sortedPlacements[len(sortedPlacements) - 1]):
                if self.__game.board.getLetter(x, i) == ' ':
                    raise ValueError("Placed word contains gaps.")

        # Stop processing if this is the first move
        if self.__game.isNewGame:
            return

        # Check that the placed tiles connect to the existing tiles
        placementIndex = 0
        connected = False

        if direction == DIRECTION_HORIZONTAL:
            y = self.__placements[0]['y']

            for x in sortedPlacements:
                if y > 0 and self.__game.board.getLetter(x, y - 1) != ' ':
                    # There is a connection to a letter above the word
                    connected = True
                    break
                elif y < len(self.__game.board.tiles) - 1 and self.__game.board.getLetter(x, y + 1) != ' ':
                    # There is a connection to a letter below the word
                    connected = True
                    break

                if x > 0 and self.__game.board.getLetter(x - 1, y) != ' ':
                    # There is a connection on the left of this letter
                    if placementIndex == 0 or sortedPlacements[placementIndex - 1] + 1 != x:
                        # The connection on the left is not the result of a
                        # connection within the new placements
                        connected = True
                        break

                if x < len(self.__game.board.tiles[y]) - 1 and self.__game.board.getLetter(x + 1, y) != ' ':
                    # There is a connection of the right of this letter
                    if placementIndex == len(sortedPlacements) - 1 or sortedPlacements[placementIndex + 1] - 1 != x:
                        # The connection on the right is not the result of a
                        # connection within the new placements
                        connected = True
                        break

                placementIndex += 1

            if not connected:
                raise ValueError("Placements do not connect with the existing letters.")
        else:
            x = self.__placements[0]['x']

            for y in sortedPlacements:
                if x > 0 and self.__game.board.getLetter(x - 1, y) != ' ':
                    # There is a connection to a letter on the left of the word
                    connected = True
                    break
                elif x < len(self.__game.board.tiles[y]) - 1 and self.__game.board.getLetter(x + 1, y) != ' ':
                    # There is a connection to a letter on the right of the word
                    connected = True
                    break

                if y > 0 and self.__game.board.getLetter(x, y - 1) != ' ':
                    # There is a connection above this letter
                    if placementIndex == 0 or sortedPlacements[placementIndex - 1] + 1 != y:
                        # The connection above is not the result of a connection
                        # within the new placements
                        connected = True
                        break

                if y < len(self.__game.board.tiles) - 1 and self.__game.board.getLetter(x, y + 1) != ' ':
                    # There is a connection below this letter
                    if placementIndex == len(sortedPlacements) - 1 or sortedPlacements[placementIndex + 1] - 1 != y:
                        # The connection below is not the result of a connection
                        # within the new placements
                        connected = True
                        break

                placementIndex += 1

            if not connected:
                raise ValueError("Placements do not connect with the existing letters.")


    def getScore(self, words):
        """Calculate the total score represented by the words dictionary."""
        score = 0

        for word in words:
            if words[word]['direction'] == DIRECTION_HORIZONTAL:

                # Score horizontal word
                score += self.__game.board.scoreHorizontalWord(words[word]['x'], words[word]['y'], words[word]['length'])
            else:

                # Score vertical word
                score += self.__game.board.scoreVerticalWord(words[word]['x'], words[word]['y'], words[word]['length'])

        return(score)


# Test match
game = Game(2)


#print(game.getRemainingLetterCount())
#print(game.players[0].playWordHorizontal("cheese", 9, 11))
#print(game.players[0].playWordHorizontal("cheese", 9, 10))

print('Initial tiles')
print('Player 1: %s' % game.players[0].tiles)

print('Player 2: %s' % game.players[1].tiles)


move = game.nextMove()
print("Player " + str(game.currentPlayer) + " places 'bin'")
move.placeLetter('b', 7, 7)
move.placeLetter('i', 7, 8)
move.placeLetter('n', 7, 9)
move.commit()
print("Score: " + str(move.score))

print("Board state:")
game.board.kprint()


move = game.nextMove()
print("Player " + str(game.currentPlayer) + " places 'chip'")
move.placeLetter('c', 5, 8)
move.placeLetter('h', 6, 8)
move.placeLetter('p', 8, 8)
move.commit()
print("Score: " + str(move.score))

print("Board state:")
game.board.kprint()


move = game.nextMove()
print("Player " + str(game.currentPlayer) + " places 'chips'")
move.placeLetter('s', 9, 8)
move.commit()
print("Score: " + str(move.score))

print("Board state:")
game.board.kprint()


move = game.nextMove()
print("Player " + str(game.currentPlayer) + " places 'bound'")
move.placeLetter('o', 8, 7)
move.placeLetter('u', 9, 7)
move.placeLetter('n', 10, 7)
move.placeLetter('d', 11, 7)
move.commit()
print("Score: " + str(move.score))

print("Board state:")
game.board.kprint()


print("Scores:")
for i in range(0, len(game.players)):
    print("Player " + str(i) + ": " + str(game.players[i].score))
