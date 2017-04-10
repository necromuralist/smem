"""
collects system-wide info
"""
# python standard library
import os


class SystemMemory(object):
    """gets the system memory information
    Args:
     source (str): path to the proc-files (e.g. /proc)
    """
    def __init__(self, source):
        self.source = source
        self._meminfo = None
        return

    @property
    def meminfo(self):
        """contents of meminfo file as a dictionary"""
        if self._meminfo is None:
            with open(os.path.join(self.source, "meminfo")) as lines:
                tokenized = (line.split() for line in lines)
                self._meminfo = {tokens[0].rstrip(":").lower(): tokens[1]
                                 for tokens in tokenized if tokens}
        return self._meminfo

    def __getattr__(self, key):
        """hack because I'm too lazy to map the keys"""
        try:
            return self.meminfo[key]
        except KeyError:
            raise AttributeError("unknown meminfo attribute: {0}".format(key))
        return
