# python standard library
from io import StringIO

# third-party
from expects import equal
from expects import expect
from expects import raise_error
import pytest

# this package
from smem.system_memory import SystemMemory

@pytest.fixture
def open_mock(mocker):
    mock = mocker.patch("{0}.open".format(SystemMemory.__module__))
    mock.return_value = StringIO(MEMINFO)
    return mock


class TestSystem(object):
    @pytest.fixture(autouse=True)    
    def system(self):
        self.source = "/proc"
        system = SystemMemory(self.source)
        return system

    def test_source(self, system):
        expect(system.source).to(equal(self.source))
        return

    def test_meminfo(self, system, open_mock):
        expect(system.meminfo["memtotal"]).to(equal("8157084"))
        expect(system.meminfo["memfree"]).to(equal("943076"))
        expect(system.meminfo["memavailable"]).to(equal("4169868"))
        return

    def test_property(self, system, open_mock):
        expect(system.memtotal).to(equal("8157084"))
        expect(system.memfree).to(equal("943076"))
        expect(system.memavailable).to(equal("4169868"))
        return

    def test_bad_property(self, system, open_mock):
        def bad_property():
            return system.ummagumma

        expect(bad_property).to(raise_error(AttributeError))
        return
    

MEMINFO = """
MemTotal:        8157084 kB
MemFree:          943076 kB
MemAvailable:    4169868 kB
Buffers:          636772 kB
Cached:          2364652 kB
SwapCached:            0 kB
Active:          4790936 kB
Inactive:        1393764 kB
Active(anon):    3188260 kB
Inactive(anon):   206856 kB
Active(file):    1602676 kB
Inactive(file):  1186908 kB
Unevictable:         424 kB
Mlocked:             424 kB
SwapTotal:       8369148 kB
SwapFree:        8369148 kB
Dirty:                60 kB
Writeback:             0 kB
AnonPages:       3183420 kB
Mapped:           661316 kB
Shmem:            211844 kB
Slab:             812116 kB
SReclaimable:     742592 kB
SUnreclaim:        69524 kB
KernelStack:       14384 kB
PageTables:        62012 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:    12447688 kB
Committed_AS:   10903196 kB
VmallocTotal:   34359738367 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
HardwareCorrupted:     0 kB
AnonHugePages:   1056768 kB
CmaTotal:              0 kB
CmaFree:               0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:      338432 kB
DirectMap2M:     8032256 kB
DirectMap1G:           0 kB
"""    
