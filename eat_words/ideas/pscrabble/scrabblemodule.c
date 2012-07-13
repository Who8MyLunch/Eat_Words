#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "scrabble.h"

#include <Python.h>

#define DICTNAME "min.42k"
#define NONE Py_BuildValue("")

static PyObject *
scrabble_findmove(PyObject *self, PyObject *args)
{
	/* Given a string representing a rack,
	 * return the recommended play.
	 */

	char	*s;
	Play	play;
	Rack	rack;
	Word	word;
	char	buf[BLEN+3];

	if (!PyArg_ParseTuple(args, "s", &s))
		return NULL;

	DPRINT("got args\n");
	str2rack(s,&rack);
	rackprint(&rack);
	DPRINT("rack printed\n");

	if(findplay(&play, &rack)) {
		word2str(&play.word, buf);
		DPRINT("m %d %d %c %s\n",
			play.pos.x, play.pos.y, ori2c(play.o), buf);
	} else {
		DPRINT("no word can be found\n");
		PyErr_SetString(PyExc_ValueError, "no move possible");
		return NULL;
	}

	DPRINT("done move\n");

	word2str(&play.word, buf);
	return (Py_BuildValue("(llcs)",
		play.pos.x, play.pos.y, ori2c(play.o), buf));	
}

static PyObject *
scrabble_makemove(PyObject *self, PyObject *args)
{
	/* Given a play, make the play (change our board)
	 */
	char	*s;
	long	x,y;
	Play	p;
	Ori	o;
	char	*err;
	char	c;

	if (!PyArg_ParseTuple(args, "llcs", &x, &y, &c, &s))
		return NULL;
	o = c2ori(c);
	initplay(&p, x, y, o, s);
	if(err = valid(&p)) {
		PyErr_SetString(PyExc_ValueError, err );
		return NULL;
	}
	play(&p);
	return NONE;
}

static PyObject *
scrabble_scoremove(PyObject *self, PyObject *args)
{
	/* Given a play, return the score.  Raise an exception
	 * if the move isn't valid.
	 */
	char	*s;
	long	x,y;
	long	res;
	char	*foom;
	Play	p;
	Rack	rack;
	Ori	o;
	char	c;

	if (!PyArg_ParseTuple(args, "llcs", &x, &y, &c, &s))
		return NULL;
	o = c2ori(c);

	initplay(&p, x, y, o, s);
	if(foom = valid(&p)) {
		DPRINT("play not valid %s\n", foom);
		PyErr_SetString(PyExc_ValueError, foom);
		return NULL;
	}
	return Py_BuildValue("i", score(&p.word, p.pos, p.o));
}

static PyObject *
scrabble_printboard(PyObject *self, PyObject *args)
{
	boardprint();
	return NONE;
}

static PyObject *
scrabble_goodenough(PyObject *self, PyObject *args)
{
	int	i;

	if (!PyArg_ParseTuple(args, "i", &i))
		return NULL;

	goodenough = i;
	return NONE;
}
static PyObject *
scrabble_reset(PyObject *self, PyObject *args)
{
	initboard();
	return NONE;
}

static PyMethodDef scrabble_methods[] = {
	{"findmove",		scrabble_findmove, 1},
	{"makemove",		scrabble_makemove, 1},
	{"scoremove",		scrabble_scoremove, 1},
	{"board",		scrabble_printboard, 1},
	{"reset",		scrabble_reset, 1},
	{"goodenough",		scrabble_goodenough, 1},
	{NULL,		NULL}		/* sentinel */
};

/* Initialization function for the module (*must* be called initscrabble) */

void
initscrabble()
{
	initdict(DICTNAME);
	initboard();
	(void) Py_InitModule("scrabble", scrabble_methods);
}
