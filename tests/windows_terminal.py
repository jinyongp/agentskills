"""Run confirmation tests in a real Windows ConPTY using only the standard library."""

import ctypes as c
from ctypes import wintypes as w
import os
import queue
import threading
import time


class Coord(c.Structure):
    _fields_ = [("x", c.c_short), ("y", c.c_short)]


class Startup(c.Structure):
    _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR), ("desktop", w.LPWSTR),
                ("title", w.LPWSTR), *[(n, w.DWORD) for n in
                ("x", "y", "width", "height", "columns", "rows", "fill", "flags")],
                ("show", w.WORD), ("reserved_size", w.WORD), ("reserved_data", c.c_void_p),
                ("input", w.HANDLE), ("output", w.HANDLE), ("error", w.HANDLE)]


class StartupEx(c.Structure):
    _fields_ = [("startup", Startup), ("attributes", c.c_void_p)]


class Process(c.Structure):
    _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE), ("pid", w.DWORD), ("tid", w.DWORD)]


def confirm_after(argv, cwd, env, mutate, response, wait_for):
    kernel = c.WinDLL("kernel32", use_last_error=True)

    def api(name, result, *args):
        function = getattr(kernel, name)
        function.restype, function.argtypes = result, args
        return function

    pointer = c.c_void_p
    handle_ptr = c.POINTER(w.HANDLE)
    dword_ptr = c.POINTER(w.DWORD)
    create_pipe = api("CreatePipe", w.BOOL, handle_ptr, handle_ptr, pointer, w.DWORD)
    create_console = api("CreatePseudoConsole", c.c_long, Coord, w.HANDLE, w.HANDLE, w.DWORD, handle_ptr)
    close_console = api("ClosePseudoConsole", None, w.HANDLE)
    init_attributes = api("InitializeProcThreadAttributeList", w.BOOL, pointer, w.DWORD, w.DWORD, c.POINTER(c.c_size_t))
    update_attributes = api("UpdateProcThreadAttribute", w.BOOL, pointer, w.DWORD, c.c_size_t, pointer, c.c_size_t, pointer, pointer)
    delete_attributes = api("DeleteProcThreadAttributeList", None, pointer)
    create_process = api("CreateProcessW", w.BOOL, w.LPCWSTR, w.LPWSTR, pointer, pointer, w.BOOL,
                         w.DWORD, pointer, w.LPCWSTR, c.POINTER(StartupEx), c.POINTER(Process))
    read_file = api("ReadFile", w.BOOL, w.HANDLE, pointer, w.DWORD, dword_ptr, pointer)
    write_file = api("WriteFile", w.BOOL, w.HANDLE, pointer, w.DWORD, dword_ptr, pointer)
    wait = api("WaitForSingleObject", w.DWORD, w.HANDLE, w.DWORD)
    exit_code = api("GetExitCodeProcess", w.BOOL, w.HANDLE, dword_ptr)
    terminate = api("TerminateProcess", w.BOOL, w.HANDLE, w.UINT)
    close = api("CloseHandle", w.BOOL, w.HANDLE)

    def checked(ok):
        if not ok:
            raise c.WinError(c.get_last_error())

    input_read, input_write, output_read, output_write, console = (w.HANDLE() for _ in range(5))
    process, attributes, reader = Process(), None, None
    attributes_ready = False
    chunks = queue.Queue(maxsize=64)
    stats = {"bytes": 0}
    try:
        checked(create_pipe(c.byref(input_read), c.byref(input_write), None, 0))
        checked(create_pipe(c.byref(output_read), c.byref(output_write), None, 0))
        result = create_console(Coord(120, 40), input_read, output_write, 0, c.byref(console))
        if result:
            raise OSError(f"CreatePseudoConsole failed: HRESULT {result & 0xffffffff:#x}")
        size = c.c_size_t()
        init_attributes(None, 1, 0, c.byref(size))
        attributes = c.create_string_buffer(size.value)
        checked(init_attributes(attributes, 1, 0, c.byref(size)))
        attributes_ready = True
        checked(update_attributes(attributes, 0, 0x20016, console, c.sizeof(console), None, None))
        startup = StartupEx()
        startup.startup.cb = c.sizeof(startup)
        startup.attributes = c.cast(attributes, pointer)
        # The test runner redirects its own stdout. Reopen the attached console
        # in the child so those redirected handles cannot bypass the ConPTY.
        if any(any(char in word for char in '%!^"\r\n') for word in argv):
            raise ValueError("Unsupported terminal fixture argument")
        shell = os.path.join(os.environ["SystemRoot"], "System32", "cmd.exe")
        command = c.create_unicode_buffer('"' + shell + '" /d /s /c "' +
                                          " ".join('"' + word + '"' for word in argv) + ' <CON >CON 2>CON"')
        environment = c.create_unicode_buffer("\0".join(f"{k}={v}" for k, v in sorted(env.items(), key=lambda item: item[0].upper())) + "\0")
        checked(create_process(shell, command, None, None, False, 0x80000 | 0x400,
                               environment, str(cwd), c.byref(startup), c.byref(process)))
        close(input_read)
        input_read = w.HANDLE()
        close(output_write)
        output_write = w.HANDLE()

        def drain():
            buffer, count = c.create_string_buffer(4096), w.DWORD()
            while read_file(output_read, buffer, len(buffer), c.byref(count), None) and count.value:
                stats["bytes"] += count.value
                try:
                    chunks.put_nowait(buffer.raw[:count.value])
                except queue.Full:
                    pass  # Keep draining during shutdown, even after a noisy failure.

        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        output, deadline = b"", time.monotonic() + 15
        while wait_for not in output:
            if time.monotonic() > deadline or wait(process.process, 0) == 0:
                raise AssertionError(f"Prompt missing; last 4096 bytes ({max(0, stats['bytes']-len(output[-4096:]))} omitted): {output[-4096:]!r}")
            try:
                output = (output + chunks.get(timeout=0.05))[-65536:]
            except queue.Empty:
                pass
        mutate()
        data = c.create_string_buffer(response.replace(b"\n", b"\r"))
        count = w.DWORD()
        checked(write_file(input_write, data, len(data) - 1, c.byref(count), None))
        if wait(process.process, 15000) != 0:
            raise AssertionError("CLI did not exit after terminal response")
        code = w.DWORD()
        checked(exit_code(process.process, c.byref(code)))
        return code.value
    finally:
        if process.process and wait(process.process, 0) != 0:
            terminate(process.process, 1)
            wait(process.process, 2000)
        if console:
            close_console(console)
        if reader:
            reader.join(timeout=2)
        if attributes_ready:
            delete_attributes(attributes)
        for handle in (input_read, input_write, output_read, output_write, process.thread, process.process):
            if handle:
                close(handle)
