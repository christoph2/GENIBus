# Automake file.  Run ./autogen.sh to generate Makefile.in, etc.

# Use the m4/ directory for macros
ACLOCAL_AMFLAGS = -I m4

## This is the "plain C" example library
# The library we'll create
lib_LTLIBRARIES = libexample.la
# it's source files
libexample_la_SOURCES = src/example.c src/example.h

## This is the Python module interfacing to libexample
# example.py and example_wrap.c are created by SWIG from src/example.i
# Put these in the build tree
BUILT_SOURCES = $(builddir)/example.py $(builddir)/example_wrap.c
# tell Make how to create the generated SWIG files
$(builddir)/example.py $(builddir)/example_wrap.c: src/example.i
$(SWIG) $(AX_SWIG_PYTHON_OPT) -o $@ $<
	
# Ask autotools to install the generated Python file
python_PYTHON = $(builddir)/example.py
# This is the Python module
pyexec_LTLIBRARIES = _example.la
# It is composed of the generated C file
_example_la_SOURCES = $(builddir)/example_wrap.c src/example.h src/example.i
	
# -module tells libtool we don't need a 'lib' prefix
_example_la_LDFLAGS = -module ${PYTHON_LDFLAGS}
	
# One point of this example is to have the Python module
# link to another library
_example_la_LIBADD = libexample.la
	
# -I$(srcdir)/src is for src/example.h
_example_la_CPPFLAGS = -I$(srcdir)/src ${PYTHON_CPPFLAGS}
	