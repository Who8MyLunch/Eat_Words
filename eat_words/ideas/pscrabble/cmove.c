#include "scrabble.h"

static void	xplace(Edge , Pos , Ori , Rack *, Word *, Play *pl);
static void	passover(Node , Pos , Ori , Rack *, Word *w, Play *pl);
static void	lr(Node, Pos, int, Ori, Rack *, Word *, Play *);
static void	legal (Word *, Pos, Ori, Play *);
static void	xright(Node, Pos, Ori, Rack *, Word *, Play *);

void
cmove(Play *pl, Rack *r)
{
/* Calculate the best play possible, given rack 'r'.
 * Stores the best possible (defined by 'legal') play in 'pl'.
 * If no legal play is possible, pl->score will be <0.
 */
	Word	w;
	Ori	o;
	Pos	p,left;
	Node	n;
	int	count;	/* of non-anchor squares to the left */

	wordclear(&w);
	pl->score = -1;

	for(p.x=1;p.x<=15;p.x++)
	for(p.y=1;p.y<=15;p.y++)
	for(o=0;o<2;o++)
	/* for every square, every orientation */
	if( ISANCHOR(p) && CROSS(p,ORTHO(o)) )
	{
		w.n=0;
		left=PREV(p,o);
		if(HASLETTER(left)) {
			while(HASLETTER(left))
				left = PREV(left,o);
			left=NEXT(left,o);
			while(HASLETTER(left)) {
				w.c[w.n++] = LETTER(left);
				left = NEXT(left,o);
			}
			n = traverse(root, &w, 0);
			assert(n>=0);
			xright(n, p, o, r, &w, pl);
			continue;
		} else {
			count=0;
			while((CROSS(left,o) == ONES) &&
					(CROSS(left,ORTHO(o)) == ONES)) {
				count++;
				left = PREV(left,o);
			}
			lr(root,p,count,o, r,&w, pl);
		}
	}
}

static void
legal (Word *w, Pos p, Ori o, Play *pl)
{
	/* Called every time we find a legal play.
	 * For now, simply remember the highest scoring word.
	 * Easy optimisation:  penalise words that use useful letters,
	 * to make the computer save those letters.
	 * HARD optimisation: try to avoid leaving opportunities (triples, etc.)
	 * for the other player to exploit.
	 */
	int	s;

	assert(isword(root, w));
	s = score(w,p,o);
	if (pl->score < goodenough){
		if(s > pl->score){
			printf("pl->score %d, s %d, goodenough %d\n", pl->score,s, goodenough);
			*pl = (Play) { *w, p, o, s };
		}
	}
}

/* The tricky algorithmy stuff :-)
 */

static void
lr( Node n, Pos p, int count, Ori o, Rack *r, Word *w, Play *pl)
{
	Edge	e;
	char	c;

	xright(n,p,o,r,w, pl);

	if(count && (r->n > 1) && n)
	do{
		e = dict[n++];
		c=LET(e);
		if(r->c[BLANK]) {
			place(r,w,c,true);
			lr(NODE(e), p, count -1, o, r, w, pl);
			unplace(r,w,c,true);
		}
		if(r->c[c]) {
			place(r,w,c,false);
			lr(NODE(e), p, count -1, o, r, w, pl);
			unplace(r,w,c,false);
		}
	} while(!LAST(e));
}

static void
xright(Node n, Pos p, Ori o, Rack *r, Word *w, Play *pl)
{
/* Extend right, try to place a tile. */

	Edge	e;
	char	c;

	assert(traverse(root,w,0) == n);
	assert(n >= 0);
	assert(!HASLETTER(p));

	if(r->n && n) {
		do {
			e = dict[n++];
			c = LET(e);
			if((CROSS(p,ORTHO(o))) & (1<<c)) {
				if(r->c[BLANK]) {
					place(r,w,c,true);
					xplace(e, p, o, r, w, pl);
					unplace(r,w,c, true);
				}
				if(r->c[c]) {
					place(r,w,c,false);
					xplace(e, p, o, r, w, pl);
					unplace(r,w,c, false);
				}
			}
		} while (!LAST(e));
	}
}

static void
xplace(Edge e, Pos p, Ori o, Rack *r, Word *w, Play *pl)
{
/* We just placed a tile.  If the next square has a letter,
 * handle separately.  If the edge we just used is a terminator,
 * call legal.  Call xright to continue extending.
 */
	Pos		next;
	Node	n;

	next = NEXT(p,o);
	n = NODE(e);
	if(HASLETTER(next)) {
		passover(n, next, o, r, w, pl);
		return;
	}
	if(TERM(e))
		legal(w, p, o, pl);
	xright(NODE(e), NEXT(p,o), o, r, w, pl);
}

static void
passover(Node n, Pos p, Ori o, Rack *r, Word *w, Play *pl)
{
/* Pass over already placed tiles.  If the end is a word,
 * call legal.  Call xright to extend it right further.
 * Finally, remove the letters we've added.
 */
	Word	tmp;
	Bool	found;
	Edge	e;

	tmp.n = 0;
	
	assert(traverse(root,w,0)==n);

	while(HASLETTER(p)) {
		if(!n)
			return;	/* no harm done */
		found = false;
		do {
			e = dict[n++];
			if(LET(e) == LETTER(p)) {
				found = true;
				break;
			}
		} while (!LAST(e));
		if (!found)
			return;	/* dead end, we've disturbed nothing */

		n = NODE(e);
		tmp.c[tmp.n++] = LETTER(p);
		p = NEXT(p,o);
	}

	/* p is the first non-tile square, 
	 * n is current node, e the edge we just traversed,
	 * tmp holds all the letters we covered.
	 */

	wordadd(w,&tmp);
	assert(traverse(root,w,0)>=0);
	if(TERM(e))
		legal(w, PREV(p,o), o, pl);
	xright(n, p, o, r, w, pl);
	wordrm(w,&tmp);
}

void
ana (Node n, Word *w, Rack *r, Play *p)
{
/* Form a simple anagram using the rack.
 */
	int		e;
	char	c;
	int		s;

	if(n)
	do {
		e=dict[n++];
		c=LET(e);
		if(r->c[c]) {
			place(r,w,c,false);
			if(TERM(e)) {
				s = simplescore(w);
				if(s>p->score) {
					p->score = s;
					p->word = *w;
				}
			}
			if(r->n)
				ana(NODE(e), w, r,p);
			unplace(r,w,c,false);
		}
	} while (!LAST(e));
}

