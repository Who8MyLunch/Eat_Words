#include <stdlib.h>
#include "scrabble.h"

Node	*dict;		/* the dictionary */
int	root,total;
Square	board[BLEN][BLEN];
char	*argv0;
char	*dictname = "min.42k";
Bool	firstmove = true;	/* first move of the game? */

/* Positions for
 * double letter, triple letter, double word, triple word
 * scores respectively.
 */
Pos dletters[]=	{ {1,4}, {4,1}, {3,7}, {7,3}, {8,4}, {7,7}, {0,0} };
Pos tletters[]=	{ {2,6}, {6,2}, {6,6}, {0,0} };
Pos dwords[] =	{ {8,8}, {2,2}, {3,3}, {4,4}, {5,5} ,{0,0}};
Pos twords[] =	{ {1,1}, {8,1}, {0,0} };

char specialchars[] = { '.', 'd', 't', 'D', 'T' };
int points[] = {	/* points for each letter: A=1,B=3... */
    1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1,
	1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0
};
int distrib[] = {	/* number of letters in bag: 9*A, 2*B...2*Blank */
	9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6,
	8, 2, 1, 6, 4,  6, 4, 2, 2, 1, 2, 1, 2
};
int goodenough = 2000;	/* a move that is good enough */
