INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_FLEX flex)

FIND_PATH(
    FLEX_INCLUDE_DIRS
    NAMES flex/api.h
    HINTS $ENV{FLEX_DIR}/include
        ${PC_FLEX_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    FLEX_LIBRARIES
    NAMES gnuradio-flex
    HINTS $ENV{FLEX_DIR}/lib
        ${PC_FLEX_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(FLEX DEFAULT_MSG FLEX_LIBRARIES FLEX_INCLUDE_DIRS)
MARK_AS_ADVANCED(FLEX_LIBRARIES FLEX_INCLUDE_DIRS)

