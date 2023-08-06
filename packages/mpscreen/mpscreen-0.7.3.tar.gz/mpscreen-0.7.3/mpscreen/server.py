import os
import time
import sys
from faster_fifo import Queue
from multiprocessing import Process
from queue import Full, Empty

from mpscreen.components import buffer, bufferServer, line, lineServer, Vstr, Vint, SR, SL

consoleEscape = r'\u001b\[.+m'




def _screenMainLoop(s):

    s.getTerminalSize()
    s.refresh(f=True)
    resizeCheck = int(round(time.time() * 1000))
    messages=[]
    sizeOfQueue = 1e9
    start = time.time()
    while True:
        if int(round(time.time() * 1000)) - resizeCheck > 10000:
            s.getTerminalSize()
            resizeCheck = int(round(time.time() * 1000))
            s.refresh(f=True)
        try:
            sizeOfQueue = s.q.qsize()
            messages = s.q.get_many(timeout=0.5)
            #print(time.time() - start)
        except Empty:
            s.refresh()
        for msg in messages :
            elem = s.getElem(msg[0])
            if elem:
                elem.receive(msg)
        t = int(round(time.time() * 1000))
        if (sizeOfQueue < 1000 and t - s.lastRefresh > 30) or t - s.lastRefresh > 500:
            s.lastRefresh = t
            s.refresh()


class Server:
    def __init__(self):
        self.q = Queue(10 * 1024 * 1024)
        self.state = {}
        self._p = None
        self.elems = []
        self.rows = 20
        self.columns = 80
        self.lastRefresh = 0
        self.getTerminalSize()

    def start(self):
        self._p = Process(target=_screenMainLoop, args=(self,))
        self._p.start()

    def buildBuffer(self, top=None, bottom=None, height=None, color=249, background=235):
        elem_id = len(self.elems)
        element = bufferServer(top=top, bottom=bottom, height=height, color=color, background=background)
        self.elems.append(element)
        return buffer(self.q, elem_id)

    def buildLine(self, top=None, bottom=None, pattern=[''], background=40, color=50):
        elem_id = len(self.elems)
        element = lineServer(top=top, bottom=bottom, pattern=pattern, background=background, color=color)
        self.elems.append(element)
        return line(self.q, elem_id, element.variables, element.variableNames)

    def getElem(self, elem):
        if elem < len(self.elems):
            return self.elems[elem]
        return None

    def refresh(self, f=False):
        if f:
            print("\u001b[2J")
        for v in self.elems:
            v.paint(rows=self.rows, columns=self.columns, f=f)
        print('\u001b[{};0H'.format(self.rows - 1))

    def getTerminalSize(self):
        rc = []
        try:
            rc = os.popen('stty size', 'r').read().split()
        except:
            pass
        if len(rc) > 0:
            if self.rows != int(rc[0]) or self.columns != int(rc[1]):
                self.refresh(f=True)
            self.rows = int(rc[0])
            self.columns = int(rc[1])

    def close(self):
        self.q.put(['Q'])


def linePrinter(cs: line):
    t = time.time()
    while True:
        for i in range(300000):
            cs["v"].set(str(time.time()- t))
            #time.sleep(2.2)


def linePrinter2(cs: line):
    while True:
        for i in range(0, 10000):
            cs["count"].add(1)
            #time.sleep(1.2)


def bufferPrinter(bs: buffer):
    for i in range(1000, 3000):
        bs.append(('\u001b[48;5;13m') + (str(i) * (2)))
        bs.append((str(i) * 13))
        time.sleep(1.1)


if __name__ == "__main__":
    ss = Server()
    l1 = ss.buildLine(top=1, pattern=[" Main Pattern : ", SR(background=240), "  ",Vstr("v"),"  "], background=52, color=207)
    l2 = ss.buildLine(top=2, pattern=[" Main Pattern  ", SR(background=240), Vint("count:>8")," ", SR(background=245), Vint("total:>8")," "], background=55, color=207)
    upperConsole = ss.buildBuffer(top=3, height=20)
    lowerConsole = ss.buildBuffer(bottom=2, top=25, background = 117)
    ss.buildLine(top=24, background=24)
    ss.buildLine(bottom=1, background=24)
    ss.start()

    pr = [Process(target=linePrinter, args=[l1]),
          Process(target=linePrinter2, args=[l2]),
          Process(target=bufferPrinter, args=[upperConsole]),
          Process(target=bufferPrinter, args=[lowerConsole])
    ]

    for p in pr:
        p.start()

    for p in pr:
        p.join()

    ss.close()
