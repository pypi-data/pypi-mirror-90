cimport cython

cdef extern:
	ctypedef bint bool
	ctypedef unsigned char * byteptr
	ctypedef char * charptr
	ctypedef void * voidptr
	ctypedef struct string:
		byteptr str
		int len
		int is_lit

	string gencmd__gencmd(string cmd)
