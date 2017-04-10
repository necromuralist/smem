# python stardard library
from io import StringIO
import os
import random

# third party
from expects import equal
from expects import expect
from mock import MagicMock
from mock import patch
import pytest

# this package
from smem.process import Process

class TestProcess(object):
    @pytest.fixture(autouse=True)
    def process(self):
        self.process_id = random.randrange(1, 100)
        self.source = "aoeue/"
        process = Process(self.source, self.process_id)
        return process

    def test_directory(self, process, mocker):
        # the mocker fixture tearsdown the patch for you
        os_mock = mocker.patch('{0}.os'.format(Process.__module__),
                               autospec=True)
        directory_list = "1 2 5 6 7 version".split()
        process_path = self.source + str(self.process_id)
        os_mock.listdir.return_value = directory_list
        os_mock.path.join.return_value = process_path
        output = process.directory
        os_mock.path.join.assert_called_once_with(self.source, str(self.process_id))
        os_mock.listdir.assert_called_once_with(process_path)
        expect(output).to(equal(directory_list))
        return
    
    def test_map_data(self, process):
        expect(process.map_data).to(equal("{0}{1}/smaps".format(
            self.source,
            self.process_id)))
        return
        

    def test_process_maps(self, process, mocker):
        open_mock = mocker.patch("{0}.open".format(Process.__module__))
        open_mock.return_value = StringIO(SMAPS)
        outcome = process.process_maps
        expected_pss = 5804, 5776

        range_keys = [int("00400000", 16),
                      int("009c9000", 16)]
        for index, key in enumerate(range_keys):
            expect(outcome[key]["pss"]).to(equal(expected_pss[index]))
        return

    def test_process_totals(self, process):
        range_keys = [int("00400000", 16),
                      int("009c9000", 16)]

        maps = {range_keys[0]: dict(size=5924, rss=5804, pss=5804, shared_clean=0,
                                    shared_dirty=0, private_clean=5804,
                                    private_dirty=0, referenced=5804,
                                    swap=0),
                range_keys[1]: dict(size=6032, rss=5776, pss=5776, shared_clean=0,
                                    shared_dirty=0, private_clean=5776,
                                    referenced=5776, swap=0)}
        process._process_maps = maps
        totals = process.process_totals
        expect(totals["size"]).to(equal(5924 + 6032))
        expect(totals["rss"]).to(equal(5804 + 5776))
        expect(totals['pss']).to(equal(5804 + 5776))
        expect(totals["shared_clean"]).to(equal(0))
        expect(totals["shared_dirty"]).to(equal(0))
        expect(totals["private_clean"]).to(equal(5804 + 5776))
        expect(totals["private_dirty"]).to(equal(0))
        return

    def test_process_name(self, process, mocker):
        open_mock = mocker.patch("{0}.open".format(Process.__module__))
        reader = MagicMock(name="reader")
        enter_mock = MagicMock(name="enter-mock")
        enter_mock.read.return_value = STAT
        reader.__enter__.return_value = enter_mock
        open_mock.return_value = reader
        output = process.name
        return

SMAPS = (
"""00400000-009c9000 r-xp 00000000 08:01 60037944                           /usr/bin/syncthing
Size:               5924 kB
Rss:                5804 kB
Pss:                5804 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:      5804 kB
Private_Dirty:         0 kB
Referenced:         5804 kB
Anonymous:             0 kB
AnonHugePages:         0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Locked:                0 kB
VmFlags: rd ex mr mw me dw sd
009c9000-00fad000 r--p 005c9000 08:01 60037944                           /usr/bin/syncthing
Size:               6032 kB
Rss:                5776 kB
Pss:                5776 kB
Shared_Clean:          0 kB
Shared_Dirty:          0 kB
Private_Clean:      5776 kB
Private_Dirty:         0 kB
Referenced:         5776 kB
Anonymous:             0 kB
AnonHugePages:         0 kB
Shared_Hugetlb:        0 kB
Private_Hugetlb:       0 kB
Swap:                  0 kB
SwapPss:               0 kB
KernelPageSize:        4 kB
MMUPageSize:           4 kB
Locked:                0 kB
VmFlags: rd mr mw me dw sd""")
    
STAT = "1030 (syncthing) S 1 1030 1030 0 -1 1077936384 62992 60 110 0 590088 96787 0 8 20 0 22 0 1396 84127744 20224 18446744073709551615 4194304 10258256 140725546270784 140725546270368 4566131 0 2079996452 0 2143420159 0 0 0 17 1 0 0 62 0 0 16437248 16766720 31748096 140725546274589 140725546274644 140725546274644 140725546274789 0"
