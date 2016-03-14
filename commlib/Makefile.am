SUBDIRS = .
vpath %.c ./src
vpath %.cpp ./src
nobase_include_HEADERS = genibus/genibus.h genibus/crc.h genibus/datalink.h
lib_LTLIBRARIES = libgenibus.la
libgenibus_la_SOURCES = src/datalink.c src/crc.c src/posix_serial.c
libgenibus_la_CPPFLAGS = -I$(top_srcdir)/genibus
libgenibus_la_CFLAGS = -Wall -std=c99
libgenibus_la_CXXFLAGS = -Wall -std=c++0x
