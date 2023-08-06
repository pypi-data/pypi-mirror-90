#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file implement the TCPAsyncPortScanner class. """

###################
#    This file implement the TCPAsyncPortScanner class.
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

__all__ = [ "TCPAsyncPortScanner" ]

from asyncio import (
    Queue,
    wait_for,
    open_connection,
    create_task,
    TimeoutError,
    sleep,
)

class TCPAsyncPortScanner:

    """ This class configure and launch the asynchronous TCP connect port scan. """

    def __init__ (self, target, ports = range(1,1024), timeout = 3, number_workers = 500, timeout_total = 100, with_handle = True):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.number_workers = number_workers
        self.timeout_total = timeout_total
        if not with_handle:
            self.opened_ports = []
        self.tasks = []
        self.with_handle = with_handle

    async def quit(self):

        """ Quit after timeout timeout. """

        await sleep(self.timeout_total)
        for task in self.tasks:
            if not task.done():
                task.cancel()

        if not self.with_handle and not self.opened_ports:
            print("No results: Reasons: The computer has no open TCP ports or"
                " a firewall is protecting this computer from this scan or the" 
                "number_workers is too high.")


    async def test_port(self):

        """ Try to connect to one port. """

        while not self.ports_queue.empty():
            port = await self.ports_queue.get()

            try:
                connection = open_connection(self.target, port)
                reader, writer = await wait_for(connection, timeout=self.timeout)
            except OSError:
                pass
            except TimeoutError:
                pass
            else:
                if self.with_handle:
                    await self.handle(port)
                else:
                    self.opened_ports.append(port)
                writer.close()
                connection.close()

            self.ports_queue.task_done()

    async def handle (self, port):

        """ Use this method to get port number in real time. """

        print(f"open: {port}")

    async def scan(self):
        self.ports_queue = Queue()

        if self.timeout_total:
            task = create_task(self.quit())

        for port in self.ports:
            if isinstance(port, int):
                self.ports_queue.put_nowait(port)
            else:
                for port_ in port:
                    self.ports_queue.put_nowait(port)

        for i in range(self.number_workers):
            self.tasks.append(create_task(self.test_port()))

        await self.ports_queue.join()

        for task_ in self.tasks:
            if not task_.done():
                task_.cancel()

        if self.timeout_total:
            task.cancel()

if __name__ == "__main__":
    from asyncio import run
    scanner = TCPAsyncPortScanner("127.0.0.1")
    run(scanner.scan())

    scanner = TCPAsyncPortScanner("192.168.0.29", ports = range(1,6536), number_workers = 2500, with_handle = False)
    run(scanner.scan())
    print(scanner.opened_ports)