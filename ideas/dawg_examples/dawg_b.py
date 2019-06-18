# -*- coding: iso-8859-1 -*-
# vim: set ft=python ts=3 sw=3 expandtab:
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Copyright (c) 2003-2006 Kenneth J. Pronovici.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# Version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Copies of the GNU General Public License are available from
# the Free Software Foundation website, http://www.gnu.org/.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Author   : Kenneth J. Pronovici <pronovic@ieee.org>
# Language : Python (>= 2.3)
# Project  : WordUtils
# Revision : $Id: dawg.py,v 1.35 2003/07/16 05:32:19 pronovic Exp $
# Purpose  : Implementation of directed acyclic word graph (dawg).
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

########################################################################
# Module documentation
########################################################################

"""
Implementation of a DAWG and associated trie.

What is a DAWG?
===============

   What is a DAWG?  The acronym DAWG stands for "Directed Acyclic Word Graph."
   Some searching on USENET yields this explanation::

      [A t]rie is a tree based data structure for compact storage of a
      dictionary. Words that start with the same letters share a path in the
      Trie. For example, a Trie containing SIN, SINE, SING, PIN, PINE and PING
      looks like this:

                    *
                   / \\
                  P   S
                 /     \\
                I       I
               /         \\
              N           N
             / \         / \\
            E   G       E   G

      A leaf denotes the end of a word, but there are also word ends at inner
      nodes; usually a word end is represented with an extra flag in every node.

      A lot of space can be saved by merging identical subtrees, like this:

                    *
                   / \\
                  P   S
                   \ /  
                    I
                    |
                    N
                   / \\
                  E   G

      The resulting data structure is sometimes called a DAWG (directed
      acyclic word graph). Note that this merging step doesn't affect the
      algorithms on the tree at all, since there is no pointer to the
      parent of a node.

   Each node in a trie has a value, and a list of other nodes that come after it.
   One can determine whether a word is in the trie by searching down the tree
   structure.  If the word has been built and the current node is marked as an
   endpoint or is a leaf, then the word is in the trie.


Implementation Notes
====================

   The method used below to compress a trie into a dawg is fairly much home-grown.
   "Hints" on the web have discussed working upwards from the bottom of the tree,
   and what we've come up with works off that.  Check the documentation
   for the L{Dawg.compress} method for more details.  Many thanks to Dave Lofquist for
   help with the algorithm.

   Most of the public methods in the Dawg object are implemented in what I think
   of as hierarchical fashion.  What this means is, a public method will be
   implemented almost entirely in terms of other, private methods.  Since the
   Dawg object supports both on-disk and in-memory trees, for instance, most 
   of the public methods are implemented in terms of two different private
   methods, where the public method doesn't do much except choose between them.

   I think the method naming convention should be obvious, but I'll spell it
   out anyway.  Single-word methods are lower-case only, i.e. C{lower()}.
   Multiple-word methods are C{lowerUpper()}.  The in-memory variant of a
   method starts with C{_mem}, i.e. C{_mem_lowerUpper()}, while the on-disk
   variant starts with C{_disk}, i.e. C{_disk_lowerUpper()}.  A recursively
   called method ends with C{_r}, i.e. C{_mem_lowerUpper_r()}.  For the most
   part, any sub-methods associated with a public method are grouped with it,
   unless they stand on their own.

   Note that C{ON_DISK} dawgs are inherently read-only (i.e., you cannot insert
   new words into or remove words from C{ON_DISK} dawgs).  They're also not
   going to be as fast as C{IN_MEMORY} dawgs.  Use them when you want to
   conserve memory and when performance isn't your top priority.  


Database Format
===============

   The L{Dawg.save} method provides the option to store the a dawg on disk in
   either a wordlist or "database" format.  The "database" format is
   essentially an on-disk representation of the in-memory dawg, using file
   pointers instead of object references.  Once a database has been saved, you
   have the option of using it to load an in-memory dawg, or instead accessing
   the database directly from disk, using very little memory in the process.

   If you spend the time to compress a dawg generated from a large wordlist,
   you will definitely want to save it in database format, to avoid having to
   recompress the dawg every time you create it.

   The database file format is not intended to be human readable.  However, it
   should be portable across operating systems, since I use the Python marshal
   module to write the data to disk.  As of now, I have not done extensive
   testing on platforms other than Linux.


Documentation Notes
===================

   In the docstrings below, I tend to use 'trie' and 'dawg' interchangeably.
   Technically speaking, they're not really the same thing, although I think
   it's fair to say that a dawg is a trie, but not vice-versa.  In this code,
   the only difference is that a dawg is compressed, so a brand new Dawg 
   object is really a trie.

   I only provide docstrings for public interface methods.  I figure that the
   arguments to the private methods should be fairly obvious given the
   documentation for the public methods.  

   Keep in mind that any backslash characters in Epydoc markup must be escaped,
   so in the markup you'll always see two of them together.  This is sometimes
   a bit confusing.

@author: Kenneth J. Pronovici <pronovic@ieee.org>
"""


########################################################################
# Imported modules
########################################################################

import sys
import os
import marshal
import shutil


#######################################################################
# Module-wide configuration and constants
#######################################################################

# Definitions for the type of dawg we're working with
IN_MEMORY = 0
ON_DISK   = 1


#######################################################################
# Classes
#######################################################################

##################
# DawgError class
##################

class DawgError(Exception):
   """General exception class for this module."""
   def __init__(self, value):
      Exception.__init__(self, value)
      self.value = value
   def __str__(self):
      return self.value 


#############
# Node class
#############

class Node(object):

   ######################
   # Class documentation
   ######################

   """
   Class representing a node in an in-memory trie or dawg.
   """


   ##############
   # Constructor
   ##############

   def __init__(self, key=None):
      """
      Default constructor.
      @param key: key to be used to construct this node
      @type key: single-character string 
      """
      self._value = None
      self._endpoint = False
      self._children = { }
      if key is not None: 
         self._value = key[0].lower()
      else:
         self._value = None


   #############
   # Properties
   #############

   def _setValue(self, value):
      """
      Property target used to set value.
      """
      self._value = value

   def _getValue(self):
      """
      Property target used to get value.
      """
      return self._value

   def _setEndpoint(self, value):
      """
      Property target used to set endpoint.
      We normalize the value to C{True} or C{False}.
      """
      if value:
         self._endpoint = True
      else:
         self._endpoint = False

   def _getEndpoint(self):
      """
      Property target used to get endpoint.
      """
      return self._endpoint

   def _setChildren(self, value):
      """
      Property target used to set children.
      """
      self._children = value

   def _getChildren(self):
      """
      Property target used to get children.
      """
      return self._children

   value = property(_getValue, _setValue, None, "Value of the node.")
   endpoint = property(_getEndpoint, _setEndpoint, None, "Indicates whether node is a word endpoint.")
   children = property(_getChildren, _setChildren, None, "Children of this node.")


   ####################
   # hasChild() method
   ####################

   def hasChild(self, key):
      """
      Indicates whether node has a child with the indicated key.
      @param key: key used to search for a child.
      @type key: single-character string 
      @return: boolean True/False
      """
      value = key[0].lower()
      for child in self.children.keys():
         if child.value == value:
            return True
      return False


   ####################
   # getChild() method
   ####################

   def getChild(self, key):
      """
      Returns the child (if any) having the indicated key.
      @param key: key used to search for a child.
      @type key: single-character string 
      @return: child as L{Node} instance or C{None} if no child has the indicated key
      """
      value = key[0].lower()
      for child in self.children.keys():
         if child.value == value:
            return child
      return None


   ##########################
   # getChildValues() method
   ##########################

   def getChildValues(self):
      """
      Returns the values of this node's children.
      @return: list of children as L{Node} instances
      """
      values = []
      for child in self.children.keys():
         values.append(child.value)
      return values


   ####################
   # addChild() method
   ####################

   def addChild(self, key):
      """
      Adds a child with the given key, or return existing child with same key.
      @param key: key to be used to construct this node
      @type key: single-character string 
      @return: the new or existing child as an L{Node} instance
      """
      value = key[0].lower()
      for child in self.children.keys():
         if child.value == value:
            return child
      child = Node(key[0])
      self.children[child] = child
      return child


   ########################
   # commonValues() method
   ########################

   def commonValues(node1, node2):
      """
      Return a list of the values that two nodes have in common in their
      children.

      Note: this is a static method.
      
      @param node1: first node
      @type node1: L{Node} instance

      @param node2: second node
      @type node2: L{Node} instance

      @return: list of string values
      """
      node1_values = node1.getChildValues()
      node2_values = node2.getChildValues()
      common =  filter( lambda x: x in node1_values, node2_values )
      common.sort()
      return common
   commonValues = staticmethod(commonValues)


   #################
   # merge() method
   #################

   def merge(fromnode, tonode):
      """
      Merge one node (C{fromnode}) into another (C{tonode}).  The fromnode is
      not modified.

      Note: this is a static method.

      @param fromnode: node to merge from
      @type fromnode: L{Node} instance

      @param tonode: node to merge to
      @type tonode: L{Node} instance

      @return: List of L{Node} instances
      """
      for parent in fromnode.parents.keys():
         del fromnode.parents[parent]
         del parent.children[fromnode]
         parent.children[tonode] = tonode
         tonode.parents[parent] = parent
   merge = staticmethod(merge)


   ###################
   # compare() method
   ###################

   def compare(node1, node2):
      """
      Compare two nodes.

      The comparison checks whether the two nodes are identical, i.e.  have the
      exact same value, endpoint flag and children (not children with the same
      values).
   
      Note: this is a static method.

      @param node1: first node
      @type node1: L{Node} instance

      @param node2: second node
      @type node2: L{Node} instance

      @return: Boolean True/False indicating whether the two nodes are identical.
      """
      if node1.value != node2.value:
         return False
      if bool(node1.endpoint) != bool(node2.endpoint):
         return False
      if node1.children != node2.children:
         return False
      return True
   compare = staticmethod(compare)


#############
# Dawg class
#############

class Dawg(object):


   ######################
   # Class documentation
   ######################

   """
   Class representing a Directed Acyclic Word Graph, or DAWG.
   """


   ##############
   # Constructor
   ##############

   def __init__(self, type=IN_MEMORY, db=None, wl=None):
      """
      Default constructor.

      See the L{loadFile} method for details on how the C{db} and
      C{wl} arguments are used.

      @param type: type of dawg to be created
      @type type: one of C{[IN_MEMORY, ON_DISK]}

      @param db: database on disk to be used to create dawg
      @type db: valid filesytem path as a string

      @param wl: wordlist on disk to be used to create dawg
      @type wl: valid filesystem path as a string

      @raise DawgError: under exception circumstances
      """

      if type not in [IN_MEMORY, ON_DISK]:
         raise DawgError("Dawg type must be either IN_MEMORY or ON_DISK.")
      self._root = None
      self._type = type
      self._db = None
      self._wl = None
      self._indexed = False
      self.loadFile(db, wl)


   #############
   # Properties
   #############

   def _getRoot(self):
      """
      Property target used to get root.
      """
      return self._root

   def _getType(self):
      """
      Property target used to get type.
      """
      return self._type

   def _getDb(self):
      """
      Property target used to get db.
      """
      return self._db

   def _getWl(self):
      """
      Property target used to get wl.
      """
      return self._wl

   def _setIndexed(self, value):
      """
      Property target used to set indexed.
      We normalize the value to C{True} or C{False}.
      """
      if value:
         self._indexed = True
      else:
         self._indexed = False

   def _getIndexed(self):
      """
      Property target used to get indexed.
      """
      return self._indexed

   root = property(_getRoot, None, None, "Root node of trie/dawg.")
   type = property(_getType, None, None, "Dawg type (IN_MEMORY or ON_DISK).")
   db = property(_getDb, None, None, "Location of database on disk.")
   wl = property(_getWl, None, None, "Location of wordlist on disk.")
   indexed = property(_getIndexed, None, None, "Indicates whether the dawg has been indexed.")


   ####################
   # loadFile() method
   ####################

   def loadFile(self, db=None, wl=None):
      """
      Reads a wordlist or database file into a dawg.  

      Either a database or a wordlist may be used, but not both.  If a wordlist
      is used, it is assumed to be properly sorted on disk (i.e. the words must
      be in alphabetical order).  Neither file will ever be written to.

      Calling this function on a dawg that has been previously initialized will
      overwrite the contents of that dawg.

      You may not choose to load a wordlist into an C{ON_DISK} dawg.  First,
      create an C{IN_MEMORY} dawg using the wordlist.  Then, save the
      C{IN_MEMORY} dawg as a database.  Then, you can load use the database on
      disk as the source for your C{ON_DISK} dawg.

      @param db: database on disk to be used to initialize dawg
      @type db: valid filesytem path as a string

      @param wl: wordlist on disk to be used to initialize dawg
      @type wl: valid filesystem path as a string

      @raise DawgError: under exception circumstances
      """
      if db is not None and wl is not None:
         raise DawgError("Object may be initialized with either database or wordlist, not both.")
      elif db is not None or wl is not None:
         oldroot = self._root
         olddb = self._db
         oldwl = self._wl
         self._root = None
         self._db = None
         self._wl = None
         try:
            if self._type == IN_MEMORY:
               if db is not None:
                  self._db = db
                  self._root = self._mem_loadFileDatabase(self._db)
               else:
                  self._wl = wl
                  self._root = self._mem_loadFileWordlist(self._wl)
            elif self._type == ON_DISK:
               if db is not None:
                  if not os.path.exists(db):
                     raise IOError("Database [%s] does not exist on disk." % db)
                  self._db = db
               else:
                  raise DawgError("On-disk dawg must be loaded from database.")
         except Exception, detail:
            # If this process fails, make sure to reset the state
            self._root = oldroot
            self._db = olddb
            self._wl = oldwl
            raise DawgError("%s" % detail)

   def _mem_loadFileWordlist(self, wl):
      root = None
      for line in file(wl).xreadlines():
         root = self._insert(root, line[:-1].lower())
      return root

   def _mem_loadFileDatabase(self, db):
      f = open(db, "r+b")
      try:
         root = marshal.load(f)
         return self._mem_loadFileDatabase_r(f, root)
      except ValueError, detail:
         raise DawgError("Unable to load (%s): %s - maybe not a database?" % (db, detail))

   def _mem_loadFileDatabase_r(self, f, fp):
      node = None
      if fp != -1:
         node = Node()
         f.seek(fp)
         value = marshal.load(f)
         if value == -1:
            node.value = None
         else:
            node.value = chr(value)
         endpoint = marshal.load(f)
         if endpoint == 0:
            node.endpoint = False
         else:
            node.endpoint = True
         count = marshal.load(f)
         childfps = []
         for i in range(0, count):
            childfps.append(marshal.load(f))
         node.children = { }
         for childfp in childfps:
            child = self._mem_loadFileDatabase_r(f, childfp)
            node.children[child] = child
      return node


   ####################
   # loadList() method
   ####################

   def loadList(self, list):
      """
      Reads a Python list into a dawg.

      Calling this function on a dawg that has been previously initialized will
      overwrite the contents of that dawg.

      You may only load a list into an C{IN_MEMORY} dawg.  If you need the list
      in an on-disk dawg, create an C{IN_MEMORY} dawg using the list.  Then,
      save the C{IN_MEMORY} dawg as a database.  Then, you can load the database
      on disk as the source for your C{ON_DISK} dawg.

      @param list: Python list to be used to initialize dawg
      @type list: list of strings

      @raise DawgError: under exception circumstances
      """
      oldroot = self._root
      olddb = self._db
      oldwl = self._wl
      self._root = None
      self._db = None
      self._wl = None
      try:
         if self._type == IN_MEMORY:
            self._root = self._mem_loadList(list)
         elif self._type == ON_DISK:
            raise DawgError("On-disk dawg must be loaded from database.")
      except Exception, detail:
         # If this process fails, make sure to reset the state
         self._root = oldroot
         self._db = olddb
         self._wl = oldwl
         raise DawgError("%s" % detail)

   def _mem_loadList(self, list):
      root = None
      for word in list:
         root = self._insert(root, word.lower())
      return root


   ################
   # list() method
   ################

   def list(self):
      """
      Returns a sorted list representation of the trie/dawg.
      @return: sorted list of words in the dawg
      @raise DawgError: under exception circumstances
      """
      list = []
      func = lambda x: list.append(x)
      self.traverse(func)
      list.sort()
      return list


   #################
   # clone() method
   #################

   def clone(self, node):
      """
      Creates a new trie object, which is a clone of the trie starting at the
      given node.

      Note that the cloned trie will not be the "same" trie from the
      perspective of the L{Node.compare} method, since the actual nodes will be
      duplicated.

      This method can only be used for C{IN_MEMORY} dawgs.
      
      @param node: Node to clone from
      @type node: L{Node} instance

      @return: head of cloned trie as a L{Node} instance

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("Clone functionality is not yet implemented for on-disk dawgs.")
      clone = Dawg()
      clone._root = self._mem_clone(node)
      return clone

   def _mem_clone(self, node):
      if node is not None:
         target = Node()
         target.value = node.value
         target.endpoint = node.endpoint
         target.children = { }
         for child in node.children.keys():
            newchild = self._mem_clone(child)
            target.children[newchild] = newchild
         return target
      return None


   ################
   # size() method
   ################

   def size(self):
      """
      Returns the dawg's size in terms of nodes.

      This method works by creating a dictionary containing an entry for each
      unique node.  It's rather inefficient, and you may not want to use it
      in production code.

      This method can only be used for C{IN_MEMORY} dawgs.

      @return: tuple of C{(unique nodes, node references)}

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("Size functionality is not yet implemented for on-disk dawgs.")
      d = { }
      self._mem_size(self._root, d)
      unique = len(d.keys())
      references = 0
      for key in d.keys():
         references += d[key]
      return(unique, references)

   def _mem_size(self, node, d):
      if node is not None:
         try:
            d[node] += 1
         except:
            d[node] = 1
         for child in node.children.keys():
            self._mem_size(child, d)


   #######################
   # buildIndex() methods
   #######################

   def buildIndex(self):
      """
      Creates indexing for a DAWG.

      This method generates excess indexing information for each node.
      Included in the indexing information is a list of the node's parents, and
      an indication of the node's depth from the top of the trie.  This
      information is mostly used by the L{compress} method, but the method to
      generate it has been made public since it could conceivably be useful to
      clients under some special circumstances.

      This method can only be used for C{IN_MEMORY} dawgs.

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("Indexing functionality is not yet implemented for on-disk dawgs.")
      self.clearIndex()
      self._depths = { }
      self._mem_buildIndex(self._root, None, self._depths, 0)
      self._indexed = True

   def _mem_buildIndex(self, node, parent, d, depth):
      if node is not None:
         if parent is None:
            node.parents = { }
         else:
            try:
               node.parents[parent] = parent
            except:
               node.parents = { }
               node.parents[parent] = parent
         node.depth = depth
         node.orphan = False
         try:
            d[depth].append(node)
         except:
            d[depth] = [ node ]
         for child in node.children.keys():
            self._mem_buildIndex(child, node, d, depth+1)


   ######################
   # clearIndex() method
   ######################

   def clearIndex(self):
      """
      Clears indexing for a DAWG.

      This method can only be used for C{IN_MEMORY} dawgs.

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("Indexing functionality is not yet implemented for on-disk dawgs.")
      try:
         del self._depths
      except: pass
      self._mem_clearIndex(self._root)
      self._indexed = False

   def _mem_clearIndex(self, node):
      if node is not None:
         try:
            del node.parents
            del node.depth
            del node.orphan
         except: pass
         for child in node.children.keys():
           self._mem_clearIndex(child)


   ####################
   # compress() method
   ####################

   def compress(self, ratio=False):
      """
      Compresses a trie into a dawg, optionally returning compression ratio.

      The compression method is fairly simple.  It may not be ideal in terms
      of performance, but it should yield correct results.  

      Before doing anything else, we index the trie using the L{buildIndex}
      method.  The indexing process provides each node with information about
      who its parents are.  This information isn't needed for anything other
      than compression, so it isn't kept around most of the time.

      When indexing is complete, the first pass at at compression can begin.
      The main purpose of the first pass is to merge identical leaves.  We
      build a list of leaves, and merge any leaves that have the same value.
      All leaves are by definition endpoints, and can have no children, so
      there's no need to do any comparisons against anything other than value.

      After all of the leaves have been merged, we move onto the second pass at
      compression.  This pass always looks one "level" up from the current
      level.  For instance, the first time through, it looks at the parents of
      the leaves.  We'll compare each of the nodes, and if any two are identical
      [1], we'll merge them.  When this process is complete, we'll construct a
      new list, up one level (i.e.  parents of the nodes we just operated on,
      which the first time through would be the parents of the parents of the
      leaves) and start all over again.  The whole thing continues until the
      new list of parents contains just one node, the top node.  There is no
      other valid exit condition, since the trie does not necessarily have a
      constant depth (because our input words may vary in length).

      [1] It is important to note that for the second pass, two nodes can only be
      considered identical if they have the same value, the same endpoint flag
      and I{exactly the same set of children} - not children with the same
      values, but the I{exact same children}.  Since we work from the bottom
      to the top, any two nodes that meet these conditions must represent
      subtries that are recursively identical, all of the way down to the
      bottom of the trie.  Such nodes can then safely be merged without
      losing any information.

      On large wordlists, a large portion of the nodes in the resulting trie
      will be leaves, so a large space savings can be achieved just by merging
      down to the ideal 26 leaves (one for each letter).  The remainder of the
      processing trims even more space.  The compressed dawg often contains
      only 25% as many unique nodes as the original uncompressed trie did.  The
      algorithm appears to yield databases on disk that are 1-2 times as large
      as the original wordlist used to construct the dawg, which makes it
      feasible for a program using this dawg to distribute databases, not
      wordlists.

      The algorithm is reasonably fast for moderate-sized lists of words (a few
      minutes for 80k words on my Duron 850 with 800 MB of RAM).  However, as
      the list grows larger, things slow down considerably.  

      I have already eliminated most of the obvious bottlenecks.  For instance,
      instead of using lists that must be appended to, I use dictionaries when
      I can, and then generate the lists on the fly as I need them.  This got
      me an order of magnitude improvement in processing time (that 80k list
      used to take most of five hours to complete).  More time spent with the
      Python profiler has helped me eliminate a few other silly sources of
      inefficiency.  However, I'm now at the point where I can't find anything
      else obvious with the profiler.  I think that for this to get any faster,
      it's going to take a major algorithmic change, rather than a tweak.  I
      would be happy if someone were to prove me wrong. :-)

      This method may only be used on C{IN_MEMORY} trees.

      @param ratio: indicates whether to return compression ratio information
      @type ratio: boolean C{True}/C{False}

      @return: 
         - compression relative to original, as a percentage, if C{ratio} is True
         - C{None} if C{ratio} is False

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("On-disk dawgs may not be compressed. To compress, create in-memory database from db file.")
      if ratio:
         (original, references) = self.size()
      self._mem_compress()
      if ratio:
         (compressed, references) = self.size()
         if original > 0:
            return 100.0 - ((float(compressed)//float(original)) * 100.0)
         else:
            return 0
      return None

   def _mem_compress(self):
      if not self._indexed:
         self.buildIndex()
      leaves = self._mem_mergeLeaves()
      self._mem_mergeNonLeaves(leaves)
      self.clearIndex()

   def _mem_mergeLeaves(self):
      leaves = self.leaves()
      (values, keys) = self._mem_partitionNodeSet(leaves)
      merged = { }
      for value in keys:      # loop for each set of nodes with a given value
         target = values[value][0]
         merged[target] = target
         for leaf in values[value][1:]:
            Node.merge(leaf, target)
      return merged.keys()

   def _mem_mergeNonLeaves(self, nodes):
      if len(nodes) == 1 and nodes[0].value is None:
         return
      for node in nodes:
         (values, keys) = self._mem_partitionNodeSet(node.parents.keys())
         for value in keys:   # loop for each set of parents with a given value
            for outer in values[value]:
               if not outer.orphan:
                  for inner in values[value]:
                     if not inner.orphan:
                        if outer != inner and Node.compare(outer, inner):
                           Node.merge(inner, outer)
                           inner.orphan = True
                           del node.parents[inner]
      parents = self._mem_getNodeSetParents(nodes)
      self._mem_mergeNonLeaves(parents)

   def _mem_partitionNodeSet(self, nodeset):
      values = { }
      for node in nodeset:
         try:
            values[node.value].append(node)
         except:
            values[node.value] = [ node ]
      return(values, values.keys())

   def _mem_getNodeSetParents(self, nodeset):
      parents = { }
      for node in nodeset:
         for parent in node.parents.keys():
            parents[parent] = parent
      return parents.keys()


   ##################
   # leaves() method
   ##################

   def leaves(self):
      """
      Builds a list of leaf nodes (nodes with no children) in the trie.
      @return: list of leaves at L{Node} instances
      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("The leaves() method has not yet been implemented for on-disk dawgs.")
      d = { }
      self._mem_leaves(self._root, d)
      return d.keys()

   def _mem_leaves(self, node, d):
      if node is not None:
         keys = node.children.keys()
         if len(keys) == 0:
            d[node] = node
         else:
            for child in keys:
               self._mem_leaves(child, d)


   #################
   # level() method
   #################

   def level(self, level=0):
      """
      Builds a list of nodes that are a certain level above the bottom of a
      trie.

      We start at the leaves, and then move up a certain number of levels up
      from the leaves.  For instance, level 0 is the leaves themselves, level 1
      is the set of the parents of all of the leaves, level 2 is the parents of
      that set, etc.  We can only do this if the DAWG has been indexed, so if
      it hasn't been yet, we do it here.   

      Note: the results from this method are probably only useful when the
      method is called against an entirely uncompressed trie, since a given
      node might be at more than one level in a compressed dawg.  This is
      mostly a debugging method.  Also, bear in mind that the "level" in this
      method is not the same as the depth value generated by the L{buildIndex}
      method.

      @return: list of nodes as L{Node} instances

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("The level() method has not yet been implemented for on-disk dawgs.")
      l = self._mem_level(level)
      return l

   def _mem_level(self, level):
      if not self._indexed:
         self.buildIndex()
      nodes = self.leaves()
      for i in range(0, level):
         parents = { }
         for node in nodes:
            if node is not None:
               for parent in node.parents:
                  parents[parent] = parent
         nodes = parents.keys()
      return nodes


   ####################
   # traverse() method
   ####################

   def traverse(self, func=None):
      """
      Traverses a dawg and executes C{func(word)} for each word.

      If no function is provided, then the default function is::

         lambda x: sys.stdout.write("%s\\n" % x)

      which will print out each word on its own line (the words will be
      unordered).

      @param func: function to be called when an endpoint is reached
      @type func: reference to a function which takes one argument, a word

      @raise DawgError: under exception circumstances
      """
      if func is None:
         func = lambda x: sys.stdout.write("%s\n" % x)
      if self._type == IN_MEMORY:
         self._mem_traverse(self._root, "", func)
      else:
         self._disk_traverse(self._db, "", func)

   def _mem_traverse(self, node, word, func):
      if node is not None:
         if node.value is not None:
            word += node.value
         if node.endpoint:
            func(word)
         for child in node.children.keys():
            self._mem_traverse(child, word, func)

   def _disk_traverse(self, filepath, word, func):
      if filepath is not None:
         if os.path.exists(filepath) and os.stat(filepath)[6] > 0:
            f = open(filepath, "r+b")
            f.seek(0)
            try:
               root = marshal.load(f)
               self._disk_traverse_r(f, root, word, func)
            except ValueError, detail:
               raise DawgError("Unable to load (%s): %s - maybe not a database?" % (filepath, detail))

   def _disk_traverse_r(self, f, fp, word, func):
      if fp != -1:
         f.seek(fp)
         value = marshal.load(f)
         if value != -1:
            word += chr(value)
         if marshal.load(f) != 0:
            func(word)
         count = marshal.load(f)
         childfps = []
         for i in range(0, count):
            childfps.append(marshal.load(f))
         for childfp in childfps:
            self._disk_traverse_r(f, childfp, word, func)


   ################
   # save() method
   ################

   def save(self, db=None, wl=None, overwrite=False):
      """
      Writes a dawg to disk as a wordlist and/or a portable "database"
      format.

      Both the C{wl} and C{db} arguments may be provided.  This will
      cause the method to write both a wordlist and a database to disk.

      Note: if the dawg was created as C{ON_DISK}, then this method cannot be
      used to overwrite the in-use database on disk.

      @param db: database to be written to on disk
      @type db: valid filesytem path as a string

      @param wl: wordlist to be written to on disk
      @type wl: valid filesystem path as a string

      @param overwrite: indicates whether to overwrite an existing file on disk
      @type overwrite: boolean C{True}/C{False}

      @raise DawgError: under exception circumstances
      """
      if wl is not None:
         self._saveWordlist(wl, overwrite)
      if db is not None:
         self._saveDatabase(self._root, self._db, db, overwrite)
      
   def _saveWordlist(self, newwl, overwrite):
      if os.path.exists(newwl) and not overwrite:
         raise DawgError("Wordlist file (%s) exists but overwrite not specified." % newwl)
      if len(self.list()) == 0:
         open(newwl, "w").write("")
      else:
         fp = open(newwl, "w")
         for word in self.list():
            fp.write("%s\n" % word)

   def _saveDatabase(self, root, db, newdb, overwrite):
      if db == newdb:
         raise DawgError("Object's current database (%s) may not be overwritten by save." % db)
      if os.path.exists(newdb) and not overwrite:
         raise DawgError("Database file (%s) exists but overwrite not specified." % newdb)
      if self._type == IN_MEMORY:
         self._mem_saveDatabase(root, newdb)
      else:
         self._disk_saveDatabase(db, newdb)

   def _mem_saveDatabase(self, node, newdb):
      fps = { }
      f = open(newdb, "w+b")
      marshal.dump(int(0), f)
      root = self._mem_saveDatabase_r(node, f, fps)
      f.seek(0)
      marshal.dump(int(root), f)

   def _mem_saveDatabase_r(self, node, f, fps):
      node_fp = -1
      if node is not None:
         try:
            node_fp = fps[node]
         except KeyError:
            childfps = []
            for child in node.children.keys():
               childfps.append(self._mem_saveDatabase_r(child, f, fps))
            node_fp = f.tell()
            fps[node] = node_fp
            if node.value is None:
               marshal.dump(int(-1), f)
            else:
               marshal.dump(int(ord(node.value)), f)
            marshal.dump(int(node.endpoint), f)
            marshal.dump(int(len(childfps)), f)
            for childfp in childfps:
               marshal.dump(int(childfp), f)
      return node_fp

   def _disk_saveDatabase(self, db, newdb):
      if db is None:
         self._mem_saveDatabase(None, newdb)
      else:
         shutil.copyfile(db, newdb)


   ##################
   # search() method
   ##################

   def search(self, key):
      """
      Searches for a complete string in a trie/dawg.

      @param key: string to search for
      @type key: string, of any length

      @return: boolean indicating whether the key was found in the trie/dawg

      @raise DawgError: under exception circumstances
      """
      if self._type == IN_MEMORY:
         return self._mem_search(self._root, key.lower())
      else:
         return self._disk_search(self._db, key.lower())
   
   def _mem_search(self, node, key):
      if node is not None:
         if len(key) == 1:
            return node.hasChild(key[0]) and node.getChild(key[0]).endpoint
         if node.hasChild(key[0]):
            return self._mem_search(node.getChild(key[0]), key[1:])
      return False

   def _disk_search(self, filepath, key):
      if filepath is not None:
         if os.path.exists(filepath) and os.stat(filepath)[6] > 0:
            f = open(filepath, "r+b")
            f.seek(0)
            try:
               root = marshal.load(f)
               return self._disk_search_r(f, root, key)
            except ValueError, detail:
               raise DawgError("Unable to load (%s): %s - maybe not a database?" % (filepath, detail))

   def _disk_search_r(self, f, fp, key):
      if fp != -1:
         f.seek(fp)
         marshal.load(f)      # value
         marshal.load(f)      # endpoint
         count = marshal.load(f)
         childfps = []
         for i in range(0, count):
            childfps.append(marshal.load(f))
         if len(key) == 1:
            for childfp in childfps:
               f.seek(childfp)
               value = marshal.load(f)
               endpoint = marshal.load(f) 
               if value != -1 and chr(value) == key[0]:
                  if endpoint != 0:
                     return True
            return False
         for childfp in childfps:
            f.seek(childfp)
            value = marshal.load(f)
            if value != -1 and chr(value) == key[0]:
               return self._disk_search_r(f, childfp, key[1:])
      return False


   #########################
   # patternSearch() method
   #########################
      
   def patternSearch(self, pattern):
      """
      Searches for a pattern in a trie/dawg.

      A pattern uses the C{.} (period) character to represent a wildcard.  So,
      for instance, the pattern C{'.ai.'} would match the words C{'rail'},
      C{'hail'}, C{'mail'}, etc. if those words were in the trie/dawg.

      @return: list of words in the trie/dawg which match the pattern

      @raise DawgError: under exception circumstances
      """
      if self._type == IN_MEMORY:
         results = self._mem_patternSearch(self._root, pattern, "")
      else:
         results = self._disk_patternSearch(self._db, pattern, "")
      results.sort()
      return results
      
   def _mem_patternSearch(self, node, pattern, word):
      results = []
      if node is not None:
         if node.value is not None:
            word += node.value
         if pattern[0] == ".":
            if len(pattern) == 1:
               for child in node.children.keys():
                  if child.endpoint:
                     results.append("%s%s" % (word, child.value))
               return results
            for child in node.children.keys():
               results += self._mem_patternSearch(child, pattern[1:], word)
         else:
            if len(pattern) == 1:
               if node.hasChild(pattern[0]) and node.getChild(pattern[0]).endpoint:
                  results.append("%s%s" % (word, node.getChild(pattern[0]).value))
               return results
            if node.hasChild(pattern[0]):
               results += self._mem_patternSearch(node.getChild(pattern[0]), pattern[1:], word)
      return results

   def _disk_patternSearch(self, filepath, pattern, word):
      if filepath is not None:
         if os.path.exists(filepath) and os.stat(filepath)[6] > 0:
            f = open(filepath, "r+b")
            f.seek(0)
            try:
               root = marshal.load(f)
               return self._disk_patternSearch_r(f, root, pattern, word)
            except ValueError, detail:
               raise DawgError("Unable to load (%s): %s - maybe not a database?" % (filepath, detail))

   def _disk_patternSearch_r(self, f, fp, pattern, word):
      results = []
      if fp != -1:
         f.seek(fp)
         value = marshal.load(f)
         endpoint = marshal.load(f)
         count = marshal.load(f)
         childfps = []
         for i in range(0, count):
            childfps.append(marshal.load(f))
         if value != -1:
            word += chr(value)
         if pattern[0] == ".":
            if len(pattern) == 1:
               for childfp in childfps:
                  f.seek(childfp)
                  value = marshal.load(f)
                  endpoint = marshal.load(f)
                  if endpoint != 0:
                     results.append("%s%s" % (word, chr(value)))
               return results
            for childfp in childfps:
               results += self._disk_patternSearch_r(f, childfp, pattern[1:], word)
         else:
            if len(pattern) == 1:
               for childfp in childfps:
                  f.seek(childfp)
                  value = marshal.load(f)
                  endpoint = marshal.load(f) 
                  if value != -1 and chr(value) == pattern[0]:
                     if endpoint != 0:
                        results.append("%s%s" % (word, chr(value)))
               return results
         for childfp in childfps:
            f.seek(childfp)
            value = marshal.load(f)
            if value != -1 and chr(value) == pattern[0]:
               results += self._disk_patternSearch_r(f, childfp, pattern[1:], word)
      return results
      
      
   ###############
   # add() method
   ###############
  
   def add(self, key):
      """
      Adds a key (word) to an existing trie/dawg.

      This function inserts into a dawg by building a list of the words in the
      dawg, inserting the new key into the list, and then re-building the dawg
      based on the new list.  Obviously, this is rather memory intensive and
      inefficient.  The whole point of using a dawg in the first place is to
      avoid having a list of words around.  However, I haven't found any other
      good way to do this.

      You may not really need this functionality.  Normally, a dawg would be
      filled using the L{loadFile} method.  This L{add} method would only be
      used to add a new word to an existing trie/dawg.  If you only need to add
      a few words to an existing dawg, consider whether you might be better off
      keeping around a small Python list or dictionary to hold the extra word,
      instead of adding to the dawg.

      Remember, once you add a word into a compressed dawg, it will no longer
      be compressed.

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("On-disk dawgs read-only.  To modify, create in-memory database from db file.")
      l = self.list()
      l.append(key)
      l.sort()
      self.loadList(l)


   ##################
   # remove() method
   ##################

   def remove(self, key):
      """
      Removes a key (word) from a dawg.

      This function removes a word from a dawg by building a list of the words
      in the dawg, removing the key from the list, and then re-building the
      dawg based on the new list.  Obviously, this is rather memory intensive
      and inefficient.  The whole point of using a dawg in the first place is
      to avoid having a list of words around.  However, I haven't found any
      other good way to do this.

      You may not really need this functionality.  If you only need to remove a
      few words from an existing dawg, consider whether you might be better off
      just keeping around a small Python list or dictionary to hold those
      words.  You could then use the list or dictionary to validate the results
      returned from the L{patternSearch} method.

      Remember, once you remove a word from a compressed dawg, it will no
      longer be compressed.

      @raise DawgError: under exception circumstances
      """
      if self._type == ON_DISK:
         raise DawgError("On-disk dawgs are read-only.  To modify, create in-memory database from db file.")
      l = self.list()
      l.remove(key)
      self.loadList(l)


   ###################
   # _insert() method
   ###################

   def _insert(self, root, key):
      if self._type == ON_DISK:
         raise DawgError("On-disk dawgs are read-only.  To modify, create in-memory database from db file.")
      if root is None:
         root = Node()
      self._mem_insert(root, key)
      return root

   def _mem_insert(self, node, key):
      child = node.addChild(key[0])
      if len(key[1:]) == 0:
         child.endpoint = True
      else:
         self._mem_insert(child, key[1:])

