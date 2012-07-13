/* These are used throught the code instead of #ifdefs.  A decent compiler
 * will recognise constants inside conditionals and remove that code.
 */
enum {DBG=0};
#define DPRINT if(0)printf

#define nil 0

/* unix stuff */
#define print printf
#define sprint sprintf
#define exits exit

typedef struct Pos Pos;		/* position on the board */
typedef struct Rack Rack;		/* letters in player's rack */
typedef struct Square Square;	/* on the board */
typedef struct Play Play;
typedef struct Player Player;
typedef struct Word Word;
typedef int	Node;
typedef int	Edge;

typedef enum Bool {false, true } Bool;
typedef enum Special { Not, Dl, Tl, Dw, Tw } Special;

enum {
	BLEN = 17,		/* Board length */
	ONES=0x7ffffff,		/* 27 ones */
	BLANK=26,
	BONUS=50,
	MAXPLAYER=4,
	LLEN = 100,		/* line length */
};

/* position, orientation */
typedef enum Ori { LR, UD } Ori;
struct Pos {
	int	x,y;
};
#define ORTHO(o) (o==LR ? UD : LR )
#define PREV(p,o) ((o == LR) ? (Pos){p.x-1, p.y} : (Pos) {p.x, p.y-1})
#define NEXT(p,o) ((o == LR) ? (Pos){p.x+1, p.y} : (Pos) {p.x, p.y+1})

struct Rack {
	int n;
	int	c[27];
};

struct Square {
	int	cross[2];		/* cross-check bit-mask */
	int	side[2];		/* total score to the side */
	Special	special;		/* double/triple letter/word */
	char	letter;
	Bool	hasletter;
	Bool	isanchor;
	int	score;		/* kept in case of blank */
};
#define CROSS(p,o) board[p.x][p.y].cross[o]
#define SIDE(p,o) board[p.x][p.y].side[o]
#undef SPECIAL
#define SPECIAL(p) board[p.x][p.y].special
#define LETTER(p) board[p.x][p.y].letter
#define HASLETTER(p) board[p.x][p.y].hasletter
#define ISANCHOR(p) board[p.x][p.y].isanchor
#define SCORE(p) board[p.x][p.y].score
#define EDGE(p) (p.x == 0 || p.y == 0 || p.x == 16 || p.y == 16)
#define CENTRE (Pos) {8,8}

struct Word {
	int n;
	char	c[BLEN];
	Bool	blank[BLEN];	/* true if the letter is by a blank */
};

struct Play {
	Word		word;
	Pos		pos;	/* the position of the LAST char of the word */
	Ori		o;
	int		score;
};

struct Player {
	Rack	rack;
	Play	play;
	int	subtotal;
	Bool 	iscomputer;
};

/* dict macros */
#ifdef undef
#define LAST(x) (x>>31&1)
#define TERM(x) ((x>>30)&1)
#endif
/* dictionary entry:
 *	bit		meaning
 *	31		last branch from this node
 *	30		terminating branch
 *	22-29	letter for this branch
 *  0-21	node this branch goes to
 */

#define LAST(x) (x&(1<<31))
#define TERM(x) (x&(1<<30))
#define LET(x) ((x>>22)&0xff)
#define NODE(x) (x&0xfffff)

