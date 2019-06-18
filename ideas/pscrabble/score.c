#include "scrabble.h"

#define SCOREDBG 0

int
simplescore(Word *w)
{
	/* Return the total points for the letters in 'w'
	 */
	int		j,total;

	total=0;
	for(j=0;j<w->n;j++)
		total += points[w->c[j]];
	return total;
}

int
score (Word *w, Pos p, Ori o)
{
	/* Return score for placing 'w' at 'p' with orientation 'o'.
	 */
	Pos		start;
	int		mul;
	int		side, tside, letter, score;
	int		j, nletter;
	Special	spec;

	start = p;
	mul = 1;
	score = tside = 0;
	nletter = 0;

	for(j=w->n -1; j>=0; j--) {
		if(HASLETTER(p)) {
			letter = SCORE(p);
			side = 0;
			spec = 0;
		} else {
			nletter++;
			letter = w->blank[j] ? 0 : points[w->c[j]];
			side = SIDE(p,ORTHO(o));
			spec = SPECIAL(p);
		}
		if(spec == Dl)
			letter *= 2;
		else if (spec == Tl)
			letter *= 3;

		if(side)
			side += letter;

		if(spec == Dw) {
			side *= 2;
			mul *= 2;
		} else if (spec == Tw) {
			side *= 3;
			mul *= 3;
		}

		score += letter;
		tside += side;
		p = PREV(p,o);

		if(SCOREDBG) {
			print("%c %d ", w->c[j]+'a', letter);
			if(side)
				print("(%d) ", side);
		}
	}
	score *= mul;
	score += tside;

	if(SCOREDBG)
		print("* %d + %d = %d ", mul, tside, score);

	assert(nletter >0 && nletter < 8);
	if(nletter == 7) {
		score += BONUS;
		if(SCOREDBG)
			print("%s\n", "BONUS");
	}
	return score;
}
