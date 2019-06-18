#include "scrabble.h"

struct Init {
	Pos *arr;
	Special special;
} foo[] =
{
	{dletters, Dl},
	{tletters, Tl},
	{dwords, Dw},
	{twords, Tw},
	{nil, 0},
};

void
boardprint(void)
{
/* Print out the current board.
 */
	Pos p;
	int	j;

	print("    ");
	for(j=1;j<16;j++)
		print("%2-x", j);
	print("\n");

	for(p.y=1;p.y<16;p.y++) {
		print("%4-x", p.y);

		for(p.x=1;p.x<16;p.x++)
			if(HASLETTER(p))
				print("%c ",LETTER(p)+'a');
			else
				print("%c ",specialchars[SPECIAL(p)]);

		print("%4-x", p.y);
		print("\n");
	}

	print("    ");
	for(j=1;j<16;j++)
		print("%2-x", j);
	print("\n");
}

void
initboard(void)
{
	int	x,y;
	int	j,k;
	Pos	p;
	Square	s;

	firstmove = true;

	/* initialise normal square */
	s.cross[0]=s.cross[1] = ONES;
	s.side[0]=s.side[1] = 0;
	s.special = 0;
	s.letter = 0;
	s.hasletter = false;
	s.isanchor = false;
	s.score = 0;

	/* normal blank squares */
	for(x=0; x<BLEN; x++)
		for(y=0; y<BLEN; y++)
			board[x][y] = s;

	/* edges (0 cross check) */
	s.cross[0]=s.cross[1] = 0;
	for(j=0;j<BLEN;j++) {
		board[0][j] = s;
		board[j][0] = s;
		board[16][j] = s;
		board[j][16] = s;
	}

	/* special squares */
	for(j=0;foo[j].arr;j++)
		for(k=0;foo[j].arr[k].x;k++)
			SPECIAL(foo[j].arr[k]) = foo[j].special;

	/* use rotational symmetry to fill other quadrants */
	for(j=1;j<9;j++) {
		for(k=1;k<8;k++) {
			board[16-k][j].special = board[j][k].special;
			board[16-j][16-k].special = board[j][k].special;
			board[k][16-j].special = board[j][k].special;
		}
	}
}

