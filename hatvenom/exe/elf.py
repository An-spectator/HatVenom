#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import struct


class ELF:
    magic = [
        b"\x7f\x45\x4c\x46"
    ]

    headers = {
        'armle': (
            b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x02\x00\x28\x00\x01\x00\x00\x00\x54\x80\x00\x00\x34\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00"
            b"\x00\x80\x00\x00\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
            b"\x00\x10\x00\x00"
        ),
        'mipsbe': (
            b"\x7f\x45\x4c\x46\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x02\x00\x08\x00\x00\x00\x01\x00\x40\x00\x54\x00\x00\x00\x34"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x40\x00\x00"
            b"\x00\x40\x00\x00\xde\xad\xbe\xef\xde\xad\xbe\xef\x00\x00\x00\x07"
            b"\x00\x00\x10\x00"
        ),
        'mipsle': (
            b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x02\x00\x08\x00\x01\x00\x00\x00\x54\x00\x40\x00\x34\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00"
            b"\x00\x00\x40\x00\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
            b"\x00\x10\x00\x00"
        ),
        'x86': (
            b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x02\x00\x03\x00\x01\x00\x00\x00\x54\x80\x04\x08\x34\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
            b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x04\x08"
            b"\x00\x80\x04\x08\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
            b"\x00\x10\x00\x00"
        ),
        'aarch64': (
            b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x02\x00\xb7\x00\x00\x00\x00\x00\x78\x00\x00\x00\x00\x00\x00\x00"
            b"\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x00\x00\x00\x00\x00\x00"
            b"\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\xef\xbe\xad\xde\x00\x00\x00\x00\xef\xbe\xad\xde\x00\x00\x00\x00"
            b"\x00\x10\x00\x00\x00\x00\x00\x00"
        ),
        'x64': (
            b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x02\x00\x3e\x00\x01\x00\x00\x00\x78\x00\x40\x00\x00\x00\x00\x00"
            b"\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x00\x00\x00\x00\x00\x00"
            b"\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00"
            b"\x41\x41\x41\x41\x41\x41\x41\x41\x42\x42\x42\x42\x42\x42\x42\x42"
            b"\x00\x10\x00\x00\x00\x00\x00\x00"
        )
    }

    def generate(self, arch, data):
        if data[:4] in self.magic:
            return data

        if arch in self.headers.keys():
            elf = self.headers[arch] + data
            if elf[4] == 1:
                if arch.endswith("be"):
                    p_filesz = struct.pack(">L", len(elf))
                    p_memsz = struct.pack(">L", len(elf) + len(data))
                else:
                    p_filesz = struct.pack("<L", len(elf))
                    p_memsz = struct.pack("<L", len(elf) + len(data))
                content = elf[:0x44] + p_filesz + p_memsz + elf[0x4c:]
            elif elf[4] == 2:
                if arch.endswith("be"):
                    p_filesz = struct.pack(">Q", len(elf))
                    p_memsz = struct.pack(">Q", len(elf) + len(data))
                else:
                    p_filesz = struct.pack("<Q", len(elf))
                    p_memsz = struct.pack("<Q", len(elf) + len(data))

                content = elf[:0x60] + p_filesz + p_memsz + elf[0x70:]
            else:
                content = b''
            return content
        return b''
