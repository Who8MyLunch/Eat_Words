/* board.c */
void	boardprint(void);
void	initboard(void);

/* cmove.c */
void	ana (Node, Word *, Rack *, Play *);
void	cmove(Play *, Rack *);

/* dict.c */
void	printdict(int, int);
void	initdict(char *);
void	initbinary(char *);
void	outbinary(char *);

/* play.c */
Bool	findplay(Play *p, Rack *r);
void	play(Play *play);
char*	valid(Play *play);

/* score.c */
int	simplescore(Word *);
int	score (Word *, Pos, Ori);

/* util.c */
void	str2rack(char *s,Rack *r);
void	word2str(Word *w, char *buf);
void	str2word(char *s, Word *w);
void	initplay(Play *, int, int, Ori, char *);
void	error();
void	rackclear(Rack *);
void	rackprint(Rack *);
Node	traverse(Node, Word *, int);
Bool	isword(Node, Word *);
void	wordprint(Word *);
void	wordclear(Word *);
void	wordadd(Word *, Word *);
void	wordrm(Word *, Word *);
void	place(Rack *, Word *, char, Bool);
void	unplace(Rack *, Word *, char,Bool);
Ori	c2ori(char);
char	ori2c(Ori);
