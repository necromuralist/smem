"""
Module to gather data for a process
"""

# python standard library
import logging
import os
import re

class Process(object):
    """gatherer of information for one process
    Args:
     source (str): path to proc/ contents
     process_id (int): ID of process we're interested in
    """
    def __init__(self, source, process_id):
        self._process_id = None
        self.process_id = process_id
        self.source = source
        self._logger = None
        self._path = None
        self._directory = None
        self._map_data = None
        self._process_maps = None
        self._process_totals = None
        self._stat_path = None
        self._name = None
        return

    @property
    def logger(self):
        """python logger"""
        if self._logger is None:
            self._logger = logging.getLogger("{0}.{1}".format(
                self.__module__,
                self.__class__.__name__))
        return self._logger

    @property
    def process_id(self):
        """the process id we're interested in"""
        return self._process_id

    @process_id.setter
    def process_id(self, pid):
        """stores pid as a string
        Args:
         pid (int or str): process-id
        """
        self._process_id = str(pid)
        return

    @property
    def path(self):
        """path to the process sub-directory
        """
        if self._path is None:
            self._path = os.path.join(self.source, self.process_id)
        return self._path

    @property
    def directory(self):
        """list of things in top of source directory"""
        if self._directory is None:
            self._directory = os.listdir(self.path)
        return self._directory

    @property
    def stat_path(self):
        """path to the stat proc file"""
        if self._stat_path is None:
            self._stat_path = os.path.join(self.path, "stat")
        return self._stat_path

    @property
    def name(self):
        """the executable name"""
        if self._name is None:
            with open(self.stat_path) as stat:
                content = stat.read()
                self._name = re.search("\((?P<name>.*)\)",
                                       content).groupdict()["name"]
        return self._name
    
    @property
    def map_data(self):
        """path to the smaps file"""
        if self._map_data is None:
            self._map_data = os.path.join(self.path, "smaps")
        return self._map_data

    @property
    def process_maps(self):
        """dict of memory-measurement-type: value
        this is a conversions of /proc/<pid>/smaps
        """
        if self._process_maps is None:
            has_pss = False
            maps = {}
            start = None
            with open(self.map_data) as lines:
                tokenized = (line.split() for line in lines)
                for tokens in tokenized:
                    if not tokens:
                        continue
                    first_token = tokens[0].rstrip(":")
                    if tokens[-1] == 'kB':
                        maps[start][first_token.lower()] = int(tokens[1])
                        has_pss = has_pss or first_token == "Pss"
                    elif "-" in first_token and ":" not in first_token:
                        start, end = first_token.split("-")
                        start = int(start, 16)
                        name = "<anonymous>"
                        if len(tokens) > 5:
                            name = tokens[5]
                        maps[start] = dict(end=int(end, 16),
                                           mode=tokens[1],
                                           offset=int(tokens[2], 16),
                                           device=tokens[3],
                                           inode=tokens[4],
                                           name=name)
            if maps and not has_pss:
                self.logger.warning("Kernel doesn't seem to support PSS")
            self._process_maps = maps
        return self._process_maps

    @property
    def process_totals(self):
        """dict that sums values from the process maps"""
        if self._process_totals is None:
            totals = dict(size=0, rss=0, pss=0, shared_clean=0, shared_dirty=0,
                          private_clean=0, private_dirty=0, referenced=0,
                          swap=0)
            for memory_address in self.process_maps:
                for key in totals:
                    totals[key] += self.process_maps[memory_address].get(key,
                                                                         0)
            self._process_totals = totals
        return self._process_totals

    def reset_data(self):
        """clears the data dictionaries"""
        self._process_totals = None
        self._process_maps = None
