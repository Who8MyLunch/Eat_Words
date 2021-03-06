#include <stdlib.h>
#include <stdio.h>
#include "scrabble.h"

enum {MAXLINE=200};

static void
usage(void)
{
	print("%s [-p] [-s] [-b] [dictdfa]\n", argv0);
 	exits(0);
}

static void
help(void)
{
	printf("help\n");
	printf("f rack\n");
	printf("m x y o word\n");
	printf("s x y o word\n");
	printf("p\n");
}

static void
game_findmove(char*s)
{
	char	buf[MAXLINE];
	Rack	rack;
	Play	play;
	char	c;

	sscanf(s, "%s\n", buf);
	printf("findmove [%s]\n", buf);
	str2rack(buf,&rack);
	rackprint(&rack);
	if(findplay(&play, &rack)) {
		word2str(&play.word, buf);
		printf("m %d %d %c %s\n",
			play.pos.x, play.pos.y, ori2c(play.o), buf);
	} else {
		printf("no word can be found\n");
	}
}

static void
game_makemove(char*s)
{
	char	buf[MAXLINE];
	int	x,y;
	Ori	o;
	char	c;
	Play	p;

	sscanf(s, "%d %d %c %s\n", &x, &y, &c, buf);
	o = c2ori(c);
	printf("makemove [%d %d %c %s]\n", x,y,c, buf);
	initplay(&p, x, y, o, buf);
	wordprint(&p.word);

	if(!valid(&p)) {
		printf("play not valid\n");
		return;
	}
	play(&p);
	boardprint();
}

static void
game_scoremove(char*s)
{
	char	buf[MAXLINE];
	int	x,y;
	Ori	o;
	Play	p;
	char	c;

	sscanf(s, "%d %d %c %s\n", &x, &y, &c, buf);
	o = c2ori(c);
	printf("scoremove [%d %d %c %s]\n", x,y,c, buf);
	initplay(&p, x, y, o, buf);
	if(!valid(&p)) {
		printf("play not valid\n");
		return;
	}
	printf("score %d\n", score(&p.word, p.pos, p.o));
}

static void
gameplay(void)
{
	char	buf[MAXLINE];

	while(fgets(buf, MAXLINE, stdin)){
		switch(buf[0]){
		default: help(); break;
		case 'f': game_findmove(buf+1); break;
		case 'm': game_makemove(buf+1); break;
		case 's': game_scoremove(buf+1); break;
		case 'p': boardprint(); break;
		}
	}
}
void
main(int argc, char **argv)
{
	Bool	printout = false;
	Bool	binary = false;
	Bool	convert = false;
	int	opt;
	extern int	optind;

	argv0 = argv[0];
	while((opt = getopt(argc, argv, "cbp")) != EOF) {
		switch(opt) {
		case 'c':	convert = true; break;
		case 'b':	binary = true; break;
		case 'p':	printout = true; break;
		default:	usage();
		}
	}

	if(binary && convert)
		error("what the hey?");

	if (optind < argc)
		dictname = argv[optind];

	print("dict...");
	if(binary)
		initbinary(dictname);
	else
		initdict(dictname);
	if(convert)
		outbinary(dictname);

	if(printout) {
		printdict(root,0);
		exits(0);
	}

	print("board...");
	initboard();
	print("ready\n");

	gameplay();
}

