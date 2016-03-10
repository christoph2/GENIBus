SUBDIRS = .
vpath %.c ./src
vpath %.cpp ./src
nobase_include_HEADERS = genibus/genibus.h
lib_LTLIBRARIES = libgenibus.la
libgenibus_la_SOURCES = datalink.c crc.c posix_timer.c
libgenibus_la_CPPFLAGS = -I$(top_srcdir)/genibus
