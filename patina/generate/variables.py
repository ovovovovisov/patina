# generate a lib.rs file for system variables
from hapenny.mem import BasicMemory, SpramMemory
import datetime

class RustLib:
    def __init__(self, soc):
        self.soc = soc

    def gen_lib_rs(self, file=None):

        def emit(content):
            """Utility function that emits a string to the targeted file."""
            print(content, file=file)

        # warning header
        emit("/*")
        emit(" * Automatically generated by PATINA; edits will be discarded on rebuild.")
        emit(" * (Most header files phrase this 'Do not edit.'; be warned accordingly.)")
        emit(" *")
        emit(f" * Generated: {datetime.datetime.now()}.")
        emit(" */")
        emit("")
        for i in self.soc.fabric.memory_map.all_resources():
            res = i.resource
            name = i.resource.name
            start = i.start
            sec_length = i.end - i.start
            # exclude the storage memory
            if isinstance(res, (BasicMemory, SpramMemory)):
                continue
            emit("/// {name}".format(name=name))
            emit(
                "pub const {name}: u32 = 0x{addr:01X} ; // {addr}".format(
                    name=name.upper()+"_ADDR", addr=i.start
                )
            )
            # log(res,name,start,sec_length)
        # Reset vector
        emit("/// Reset Vector")
        emit("pub const RESET_VECTOR: u32 = 0x{addr:01X}; // {addr}".format(addr = self.soc.fabric.reset_vector << 1))
        emit("/// Date stamp when this file was generated")
        emit('pub const DATE_STAMP: &str = "{}";'.format(datetime.datetime.now()))