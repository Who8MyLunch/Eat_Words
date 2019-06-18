#include <varargs.h>
#include <stdio.h>
#include <assert.h>
#include "scrabble.h"

Ori
c2ori(char c)
{
	assert(c == 'h' || c == 'v');
	return (c == 'h') ? LR : UD;
}

char
ori2c(Ori o)
{
	return (o == LR) ? 'h' : 'v';
}

void
str2rack(char *s,Rack *r)
{
	char	c;
	int	index;
	int	j;

	r->n = 0;
	for(j=0; j<27;j++)
		r->c[j] = 0;

	while (c = *s++){
		if (c >= 'a' && c <= 'z') {
			index = c-'a';
		} else {
			assert(c == '_');
			index = BLANK;
		}
		r->c[index]++;
		r->n++;
	}
}

void
word2str(Word *w, char *buf)
{
	int	j,k;

	for(j=0,k=0; j<w->n; j++,k++){
		buf[k] = w->c[j] + 'a';
		if(w->blank[j]){
			k++;
			buf[k] = '_';
		}
	}
	buf[k] = '\0';
}

void
str2word(char *s, Word *w)
{
	int	j;

	char	c;

	for(j=0; s[0]; j++, s++) {
		assert(s[0] >='a' && s[0] <= 'z');
		w->c[j] = s[0]-'a';
		if(s[1] == '_') {
			s++;
			w->blank[j] = true;
		} else {
			w->blank[j] = false;
		}
	}
	w->n = j;
}

void
initplay(Play *p, int x, int y, Ori o, char *s)
{
	p->pos.x = x;
	p->pos.y = y;
	p->o = o;
	str2word(s, &p->word);	
}

void
error(va_alist)
va_dcl
{
	va_list	ap;
	char	*fmt;
	
	va_start(ap);
	fmt = va_arg(ap, char*);
	vfprintf(stderr, fmt, ap);
	va_end(ap);
	exit(1);
}


void
rackprint(Rack *r)
{
	int	j,k;

	assert(r->n <8);
	print("[");
	for(j=0;j<26;j++){
		assert(r->c[j]<8);
		for(k=0;k<r->c[j];k++)
			print("%c", j+'a');
	}
	for(k=0;k<r->c[26];k++)
		print("BLANK ");
	print("]\n");
}

Node
traverse(Node n, Word *w, int count)
{
	Edge	e;

	if(count == w->n)
		return n;
	if(n==0)
		return -1; /* end of the line */
	do {
		e = dict [n++];
		if(LET(e) == w->c[count]) {
			return (traverse(NODE(e), w, count+1));
		}
	} while (!LAST(e));
	return -1; /* missed it */
}

Bool
isword(Node start, Word *w)
{
	Edge	e;
	Node	n;
	Bool	found;
	int		j;

	n = start;
	for (j=0; j<w->n; j++) {
		found = false;
		do {
			e = dict[n++];
			if(LET(e) == w->c[j]) {
				found = true;
				break;
			}
		} while (!LAST(e));

		if(!found)
			return false;

		n = NODE(e);
	}
	if(TERM(e))
		return true;
	else
		return false;
}

void
wordprint(Word *w)
{
	int	j;

	for(j=0;j<w->n;j++)
		print("%c",w->c[j] + 'a');
}

void
wordclear(Word *w)
{
	int	j;

	for(j=0;j<BLEN;j++)
		w->blank[j]=false;
	w->n = 0;
}

void
wordadd(Word *w, Word *add)
{
	int	j;
	for(j=0; j<add->n; j++)
		w->c[w->n++] = add->c[j];
}

void
wordrm(Word *w, Word *add)
{
	int	j;
	w->n -= add->n;
}

void
place(Rack *r, Word *w, char c, Bool isblank)
{
	/* move 'c' from 'w' to 'r'
	 */
	r->c[isblank ? BLANK : c]--;
	r->n--;
	w->c[w->n] = c;
	w->blank[w->n] = isblank;
	w->n++;
}

void
unplace(Rack *r, Word *w, char c,Bool isblank)
{
	r->c[isblank ? BLANK : c]++;
	r->n++;
	w->n--;
	if(isblank)
		w->blank[w->n] = false;
}
