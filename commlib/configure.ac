# Autoconf file.  Run ./autogen.sh to generate configure, etc.

# typical init
AC_INIT([SwigExample],[0.0.1])

# foreign: non-GNU, don't check for NEWS, AUTHORS, etc.
AM_INIT_AUTOMAKE([foreign no-define])

# ask autotools to put extra macros in m4/
AC_CONFIG_MACRO_DIR([m4])

dnl python checks (you can change the required python version bellow)
AM_PATH_PYTHON(2.7.0)
PY_PREFIX=`$PYTHON -c 'import sys ; print sys.prefix'`
PYTHON_LIBS="-lpython$PYTHON_VERSION"
PYTHON_CFLAGS="-I$PY_PREFIX/include/python$PYTHON_VERSION"
AC_SUBST([PYTHON_LIBS])
AC_SUBST([PYTHON_CFLAGS])

ax_python_devel


# Find swig executable
# http://www.gnu.org/software/autoconf-archive/ax_pkg_swig.html
#AX_PKG_SWIG([], [], [ AC_MSG_ERROR([SWIG is required to build.]) ])
AX_PKG_SWIG


# GetWIGFLAGS, CPPFLAGS, etc., for Python generation by swig

ax_pkg_swig


# Use libtool to link libraries and modules
LT_INIT

# We'll be compiling C files
AC_PROG_CC

AC_CONFIG_FILES([Makefile])

AC_OUTPUT