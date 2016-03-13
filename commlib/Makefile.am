SUBDIRS = .
vpath %.c ./src
vpath %.cpp ./src
nobase_include_HEADERS = genibus/genibus.h
lib_LTLIBRARIES = libgenibus.la
libgenibus_la_SOURCES = src/datalink.cpp src/crc.cpp src/posix_timer.c
libgenibus_la_CPPFLAGS = -Wall -std=c99 -I$(top_srcdir)/genibus
libgenibus_la_CXXFLAGS = -Wall -std=c++0x -I$(top_srcdir)/genibus
