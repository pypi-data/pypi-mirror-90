from multiprocessing import shared_memory
import msgpack
import msgpack_numpy as m
import copy

m.patch()

debug = False


class Publisher:
    def __init__(self, name: str, block_size: int = None, qsize: int = None):
        """Initializes Publisher Object. if no block size and qsize is
        specified, assumes connecting to existing shared memory, else
        block_size is size of memory block, qsize is size of queue,
        name is memory name."""

        # Check to see if initializing or attatching
        self.name = name
        if block_size is None or qsize is None:
            self.primary = False
        else:
            self.primary = True

        # If creating, make shareable blocksize, shareable qsize,
        # as well as memory, writer position
        # Always initialize writer position to 0, we'll check again when we write

        self.writer_pos = 0

        if self.primary:
            self.block_size = block_size
            self.qsize = qsize

            self.block_size_mem = shared_memory.SharedMemory(
                name=self.name + "block_size", create=True, size=32
            )
            self.block_size_mem.buf[:] = self.block_size.to_bytes(32, "big")

            self.qsize_mem = shared_memory.SharedMemory(
                name=self.name + "qsize", create=True, size=32
            )

            self.qsize_mem.buf[:] = self.qsize.to_bytes(32, "big")

            self.writer_pos_mem = shared_memory.SharedMemory(
                name=self.name + "wpos", create=True, size=32
            )

            self.writer_pos_mem.buf[:] = self.writer_pos.to_bytes(32, "big")

            self.shared_mem = shared_memory.SharedMemory(
                name=self.name, create=True, size=self.block_size * self.qsize
            )

            self.lock_mem = shared_memory.SharedMemory(
                name=self.name + "lock", create=True, size=1
            )

            self.lock_mem.buf[:] = (0).to_bytes(1, "big")

        else:
            self.block_size_mem = shared_memory.SharedMemory(
                name=self.name + "block_size"
            )
            self.block_size = int.from_bytes(self.block_size_mem.buf, "big")

            self.qsize_mem = shared_memory.SharedMemory(name=self.name + "qsize")
            self.qsize = int.from_bytes(self.qsize_mem.buf, "big")

            self.writer_pos_mem = shared_memory.SharedMemory(name=self.name + "wpos")
            self.lock_mem = shared_memory.SharedMemory(name=self.name + "lock")
            self.shared_mem = shared_memory.SharedMemory(name=self.name)

    def publish(self, msg, safe=True):
        """Publishes any type serializable by msgpack"""
        if safe:
            while True:
                if int.from_bytes(self.lock_mem.buf, "big") == 0:
                    self._set_num_buffer(1, 1, self.lock_mem.buf)
                    break
                else:
                    continue
        dict_message = {"msg": msg}
        byte_message = msgpack.packb(dict_message)
        if len(byte_message) > self.block_size:
            raise MemoryError("Object Larger than Block Size!")
        byte_message = byte_message.zfill(self.block_size)
        self.writer_pos = self._get_num_buffer(self.writer_pos_mem.buf)
        begin, end = self._get_buffer_range()
        self.shared_mem.buf[begin:end] = byte_message
        self.writer_pos += self.block_size
        self._set_num_buffer(self.writer_pos, 32, self.writer_pos_mem.buf)
        if safe:
            self._set_num_buffer(0, 1, self.lock_mem.buf)

        if debug:
            print(self.shared_mem.buf.tobytes())

    def publishb(self, msg, safe=True):
        "Publishes raw bytes, does not attempt serialize, possibly more performant"
        assert type(msg) == bytes, "Message Must be bytes, use publish instead"
        if safe:
            while True:
                if int.from_bytes(self.lock_mem.buf, "big") == 0:
                    self._set_num_buffer(1, 1, self.lock_mem.buf)
                    break
                else:
                    continue
        if len(msg) > self.block_size:
            raise MemoryError("Object Larger than Block Size!")
        msg = msg.zfill(self.block_size)
        self.writer_pos = self._get_num_buffer(self.writer_pos_mem.buf)
        begin, end = self._get_buffer_range()
        self.shared_mem.buf[begin:end] = msg
        self.writer_pos += self.block_size
        self._set_num_buffer(self.writer_pos, 32, self.writer_pos_mem.buf)
        if safe:
            self._set_num_buffer(0, 1, self.lock_mem.buf)

    def _set_num_buffer(self, value, size, buffer):
        buffer[:] = value.to_bytes(size, "big")

    def _get_num_buffer(self, buffer):
        return int.from_bytes(buffer[:], "big")

    def _get_buffer_range(self):
        q_pos = self.writer_pos // self.block_size
        subq_size = q_pos % self.qsize
        begin = subq_size * self.block_size
        end = begin + self.block_size
        return (begin, end)

    def delete(self):
        self.block_size_mem.unlink()
        self.block_size_mem.close()
        self.qsize_mem.unlink()
        self.qsize_mem.close()
        self.writer_pos_mem.unlink()
        self.writer_pos_mem.close()
        self.lock_mem.unlink()
        self.lock_mem.close()
        self.shared_mem.unlink()
        self.shared_mem.close()

    def close(self):
        self.block_size_mem.close()
        self.qsize_mem.close()
        self.writer_pos_mem.close()
        self.lock_mem.close()
        self.shared_mem.close()


class Consumer:
    def __init__(self, name: str, con_name: str, create=False):
        """Initializes Consumer Object. name, is topic name, con_name is optional for consumer group-like behavior"""

        self.name = name
        self.con_name = con_name

        if create:
            self.read_pos_mem = shared_memory.SharedMemory(
                self.con_name, create=True, size=32
            )
            self._set_num_buffer(0, 32, self.read_pos_mem.buf)
            self.con_lock_mem = shared_memory.SharedMemory(
                self.con_name + "lock", create=True, size=1
            )
            self._set_num_buffer(0, 1, self.con_lock_mem.buf)
        else:
            self.read_pos_mem = shared_memory.SharedMemory(self.con_name)
            self.con_lock_mem = shared_memory.SharedMemory(self.con_name + "lock")

        # Get Block Size
        self.block_size_mem = shared_memory.SharedMemory(name=self.name + "block_size")
        self.block_size = int.from_bytes(self.block_size_mem.buf, "big")

        # Get qzize
        self.qsize_mem = shared_memory.SharedMemory(name=self.name + "qsize")
        self.qsize = int.from_bytes(self.qsize_mem.buf, "big")

        self.shared_mem = shared_memory.SharedMemory(name=self.name)

        self.writer_pos_mem = shared_memory.SharedMemory(name=self.name + "wpos")
        self.writer_pos = self._get_num_buffer(self.writer_pos_mem.buf)

        if create:
            self.read_pos = int(
                max(self.writer_pos - ((self.qsize // 2) * self.block_size), 0)
            )
        else:
            self.read_pos = self._get_num_buffer(self.read_pos_mem.buf)

        self._set_num_buffer(self.read_pos, 32, self.read_pos_mem.buf)

    def consume(self, safe=True, minq=None, maxq=None):
        """Consumes messages serialized by publish"""
        if safe:
            while True:
                if int.from_bytes(self.con_lock_mem.buf, "big") == 0:
                    self._set_num_buffer(1, 1, self.con_lock_mem.buf)
                    break
                else:
                    continue

        self.read_pos = self._get_num_buffer(self.read_pos_mem.buf)
        self.writer_pos = copy.copy(self._get_num_buffer(self.writer_pos_mem.buf))
        if minq is not None:
            while (self.writer_pos - self.read_pos) // self.block_size < minq:
                # print((self.writer_pos - self.read_pos) // self.block_size)
                self.writer_pos = copy.copy(
                    self._get_num_buffer(self.writer_pos_mem.buf)
                )

        total_blocks = (self.writer_pos - self.read_pos) // self.block_size
        if maxq is not None:
            total_blocks = min(total_blocks, maxq)

        if total_blocks / self.qsize > 1:
            raise ValueError("Queue Overflow! Consumer not fast enough")

        blocks_to_end = self.qsize - ((self.read_pos // self.block_size) % self.qsize)
        start_byte = ((self.read_pos // self.block_size) % self.qsize) * self.block_size
        if total_blocks > blocks_to_end:
            blocks_over = total_blocks - blocks_to_end
            local_buf = (
                self.shared_mem.buf[start_byte:].tobytes()
                + self.shared_mem.buf[: blocks_over * self.block_size].tobytes()
            )

        else:
            # print(start_byte)
            # print(total_blocks * self.block_size)
            local_buf = self.shared_mem.buf[
                start_byte : start_byte + (total_blocks * self.block_size)
            ].tobytes()

        self.read_pos = self.read_pos + (total_blocks * self.block_size)
        self._set_num_buffer(self.read_pos, 32, self.read_pos_mem.buf)

        if safe:
            self._set_num_buffer(0, 1, self.con_lock_mem.buf)

        return_list = []
        for i in range(total_blocks):
            begin = i * self.block_size
            end = (i + 1) * self.block_size
            msg = msgpack.unpackb(local_buf[begin:end].lstrip(b"0"))
            msg = msg["msg"]
            return_list.append(msg)

        assert total_blocks == len(return_list), "You did something wrong dude"
        return (total_blocks, return_list)

    def consumeb(self, msg, safe=True):
        # TODO byte version
        pass

    def _set_num_buffer(self, value, size, buffer):
        buffer[:] = value.to_bytes(size, "big")

    def _get_num_buffer(self, buffer):
        return int.from_bytes(buffer[:], "big")

    def delete(self):
        self.block_size_mem.close()
        self.qsize_mem.close()
        self.writer_pos_mem.close()
        self.con_lock_mem.unlink()
        self.con_lock_mem.close()
        self.read_pos_mem.unlink()
        self.read_pos_mem.close()
        self.shared_mem.close()

    def close(self):
        self.block_size_mem.close()
        self.qsize_mem.close()
        self.writer_pos_mem.close()
        self.con_lock_mem.close()
        self.read_pos_mem.close()
        self.shared_mem.close()
