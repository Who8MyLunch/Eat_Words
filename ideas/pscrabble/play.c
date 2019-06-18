#include <stdlib.h>
#include "scrabble.h"

static void	adjust(Pos p, Ori o);

Bool
findplay(Play *p, Rack *r)
{
	/* Find the best possible play given rack 'r',
	 * store it in 'p', return whether or not one
	 * was found.
	 */
	Word	w;

	wordclear(&w);
	p->score = -1;

	if(firstmove) {
		/* just find the biggest scoring word,
		 * don't worry too much about where to put it.
		 */
		ana(root, &w, r, p);
		p->pos = CENTRE;
	}
	else
		cmove(p,r);

	return p->score >= 0;
}

void
play(Play *play)
{
/* put the pieces on the board,
 * adjust the board data structures.
 */
	int		j;
	Pos		p;
	char	c;

	firstmove = false;

	/* describe the play */
	if(1) {
		print("(%d,%d,%c) %d ",
			play->pos.x, play->pos.y, play->o ? 'V' : 'H', play->score);
		wordprint(&play->word);
		print("\n");
		if(DBG)
			score(&play->word, play->pos, play->o);
	}

	assert(isword(root, &play->word));

	/* place the letters */
	p = play->pos;
	for (j= play->word.n -1; j>= 0; j--) {
		if(!HASLETTER(p)){
			/* place the letter on the board */
			LETTER(p) = play->word.c[j];
			HASLETTER(p)=true;
			SPECIAL(p) = Not;	/* not needed */
			ISANCHOR(p) = false;
			SCORE(p) = play->word.blank[j] ? 0 : points[play->word.c[j]];
			adjust(p,ORTHO(play->o));
		}
		p = PREV(p,play->o);
	}
	p = NEXT(p,play->o);
	adjust(p, play->o);	 /* squares to the sides */
}

static void
findstats(Pos p, Ori o)
{
	/* Recalculate cross assert and score total at 'p'
	 */
	Pos	left, right;
	Word lword, rword;
	Node n;
	Edge e;
	int	s;

	lword.n = rword.n = 0;
	if(EDGE(p))
		return;

	/* find word to the left */
	s = 0;
	for(left=PREV(p,o); HASLETTER(left); left = PREV(left,o))
		;
	left = NEXT(left,o);
	while (HASLETTER(left)) {
		lword.c[lword.n++] = LETTER(left);
		s += SCORE(left);
		left = NEXT(left,o);
	}
	/* find word to the right */
	for(right=NEXT(p,o); HASLETTER(right); right = NEXT(right,o)) {
		rword.c[rword.n++] = LETTER(right);
		s += SCORE(right);
	}
	if(DBG) {
		wordprint(&lword);
		print("X");
		wordprint(&rword);
		print(" [%d] ", s);
	}

	SIDE(p,o) = s;
	ISANCHOR(p) = true;

	/* calculate cross asserts */
	CROSS(p,o) = 0;
	n = traverse(root, &lword, 0);
	assert(n>=0);
	if(n>0)
		do {
			e = dict[n++];
			if ( (rword.n && isword(NODE(e), &rword)) || 
				 (!rword.n && TERM(e)) ) {
				CROSS(p,o) |= 1 << LET(e);
				DPRINT("%c, ", LET(e)+'a');
			}
		} while (!(LAST(e)));
	DPRINT("\n");
}

static void
adjust(Pos p, Ori o)
{
/* Recalculate cross asserts and totals in the given orientation.
 * Find the squares adjoining the block p is part of,
 * find the stats at both of these squares.
 */
	Pos	left,right;

	for(right=p; HASLETTER(right); right = NEXT(right,o))
		;
	for(left=p; HASLETTER(left); left = PREV(left,o))
		;
	findstats(left,o);
	findstats(right,o);
}

char*
valid(Play *play)
{
	/* Return NULL if play is valid, or a reason if the play is invalid.
	 */
	Pos	p;
	Pos	p2;
	int	j;
	char	c;
	static char	buf[LLEN];
	int	n;
	Bool	newletter;	/* uses at least one new letter */
	Bool	crosscentre;	/* crosses the centre square */
	Bool	hasanchor;	/* crosses at least one anchor */

	if(DBG) {
		print("assert (%d,%d,%c)", play->pos.x,
			play->pos.y, play->o == LR ? 'H' : 'V');
		wordprint(&play->word);
	}

	p = play->pos;
	p2 = NEXT(play->pos,play->o);
	if (HASLETTER(p2)){
		return "abuts another word\n";
	}
	if(!isword(root, &play->word)){
		return "not a word";
	}

	newletter = crosscentre = hasanchor = false;

	/* For each letter of the word. */
	for(j= play->word.n - 1; j>=0; j--) {
		if (p.x < 0 || p.y < 0 || p.x > BLEN || p.y > BLEN)
			return "off the edge";

		c = play->word.c[j];

		if (ISANCHOR(p)){
			hasanchor = true;
		}
		if (HASLETTER(p)) {
			if (LETTER(p) != c){
				sprintf(buf,"wanted %c, got %c at (%d,%d)",
					c+'a', LETTER(p)+'a', p.x, p.y);
				return buf;
			}
		} else {
			newletter = true;
			if(!firstmove){
				if(!(CROSS(p,ORTHO(play->o)) & 1 << c)) {
					sprintf(buf,"invalid cross word at (%d,%d)",p.x,p.y);
					return buf;
				}
			}
		}
		if (p.x == 8 && p.y ==8){
			crosscentre = true;
		}
		p = PREV(p,play->o);
	}

	if (firstmove){
		DPRINT("FIRSTMOVE\n");
		if (!crosscentre)
			return ("first move doesn't touch centre square");
	}
	if (!(hasanchor|| firstmove)){
		return ("not attached to another word");
	}	
	if(HASLETTER(p))
		return "abutting another word";

	if (! newletter)
		return "adds no letters";
	return (char*)0;
}
