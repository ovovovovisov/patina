from amaranth import *
from amaranth.utils import bits_for
from amaranth.lib.fifo import SyncFIFOBuffered
from amaranth.lib import data, wiring
from amaranth.lib.wiring import In, Out, flipped, connect

from amaranth_soc import csr
from amaranth_soc.memory import MemoryMap
from amaranth_soc.csr import field as csr_field, Field


class MemFaker(wiring.Component):
    def __init__(self, mm, addr_width):
        self.mm = MemoryMap(addr_width=addr_width, data_width=16, name="mem")
        self.mm.add_resource(name="bob",resource=(),size=2** addr_width)
        mm.add_window(self.mm)
        super().__init__(
            {"csr_bus": In(csr.Signature(addr_width=addr_width, data_width=16))}
        )

class Counter(wiring.Component):
    csr_bus: In(csr.Signature(addr_width=2, data_width=16))
    
    class Enable(csr.Register, access="rw"):
        enable: Field(csr_field.RW,1)
    
    class Counter(csr.Register, access="r"):
        value: Field(csr_field.R,16)
    
    class Overflow(csr.Register, access="rw"):
        value: Field(csr_field.RW,16)
    
    def __init__(self):
        self.enable = self.Enable()
        self.counter = self.Counter()
        self.overflow = self.Overflow()

        self.reg_map = reg_map = csr.RegisterMap()
        reg_map.add_register(self.enable, name="enable")
        reg_map.add_register(self.counter, name="counter")
        reg_map.add_register(self.overflow, name="overflow")
        
        self._csr_bridge = csr.Bridge(reg_map, name="counter", addr_width=2, data_width=16)

        super().__init__()

        self.csr_bus.memory_map = self._csr_bridge.bus.memory_map

    def elaborate(platform):
        m = Module()

     
class Widget(wiring.Component):
    out: Out(1)
    csr_bus: In(csr.Signature(addr_width=2, data_width=16))

    class Config(csr.Register, access="rw"):
        active: Field(csr_field.RW, 1)
        speed: Field(csr_field.RW, 4)
        stuff: Field(csr_field.RW, 8)

    class Test(csr.Register, access="rw"):
        bork: Field(csr_field.RW, 8)
        awesome: Field(csr_field.RW, 8)

    def __init__(self, name):
        self.conf = self.Config()
        self.test = self.Test()

        self.reg_map = reg_map = csr.RegisterMap()
        reg_map.add_register(self.conf, name="config")
        reg_map.add_register(self.test, name="test")


        self._csr_bridge = csr.Bridge(reg_map, name=name, addr_width=2, data_width=16)

        super().__init__()

        self.csr_bus.memory_map = self._csr_bridge.bus.memory_map


class Overlord(wiring.Component):
    blink: Out(1)

    def __init__(self):
        self.mem_map = MemoryMap(addr_width=16, data_width=16)

        self.mem = MemFaker(self.mem_map,13)

        self._csr_decoder = csr.Decoder(addr_width=16, data_width=16)

        self._csr_decoder.bus.memory_map = self.mem_map
        
        self.widget = Widget("first")
        self._csr_decoder.add(self.widget.csr_bus,addr=0x9000)

        self.widget2 = Widget("second")
        self._csr_decoder.add(self.widget2.csr_bus)

        self.counter=  Counter()
        self._csr_decoder.add(self.counter.csr_bus)
        super().__init__()
        
    def show(self):
        print("show")
        mm = self.mem_map.all_resources()
        for i in mm:
            #print(dir(i))
            print(i.path, i.start, i.end,i.resource)
        return i 

if __name__ == "__main__":
    ol = Overlord()
    ol.show()
