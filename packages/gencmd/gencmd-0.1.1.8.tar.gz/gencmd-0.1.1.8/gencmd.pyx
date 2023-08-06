cimport cython

from gencmd_wrapper cimport *
from libc.stdlib cimport free

cdef class GenCmdException(Exception):
    pass

cdef class GenCmd(object):

    def send(self, cmd: str) -> str:
        cmd_bytes = cmd.encode('UTF-8')
        cdef string v_string
        v_string.str = <unsigned char*>cmd_bytes
        v_string.len = len(cmd_bytes)
        v_string.is_lit = 0
        result = gencmd__gencmd(v_string)
        cdef bytes py_bytes_string
        try:
            py_bytes_string = (<char*>result.str)[:result.len]
            return py_bytes_string.decode('UTF-8')
        finally:
            free(<void*>result.str)

