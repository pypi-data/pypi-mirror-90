#!/usr/bin/python
# -*- coding: utf-8 -*-
# editor: mufei(ypdh@qq.com tel:+086 15712150708)
'''
Mufei _ __ ___   ___   ___  / _| ___(_)
| '_ ` _ \ / _ \ / _ \| |_ / _ \ |
| | | | | | (_) | (_) |  _|  __/ |
|_| |_| |_|\___/ \___/|_|  \___|_|
'''
__all__ = ['Thread']

import time
import threading

class Thread(threading.Thread):
    fncall = None #回调函数
    
    def __init__(self, fncall=None, thread_id=None, *args, **awgs):
        threading.Thread.__init__(self)
        self.args = args
        self.awgs = awgs
        if fncall: self.fncall=fncall
        self.thread_id = thread_id

    def run(self):
        self.fncall(self.thread_id, *self.args, **self.awgs)
        
    @classmethod    
    def main(cls, num, fncall, *args,  **awgs):
        """
        >>> rs = []            
        >>> def fncall(thread_id,L):
        >>>     while 1:
        >>>         time.sleep(0.5)
        >>>         if not L: break
        >>>         rs.append([thread_id,L.pop()])
        >>> Thread.main(10, fncall, range(10,100)) 
        >>> for e in rs: print(e)
        """
        threads = []
        for i in range(1,num+1):
            t = cls(fncall, i, *args,  **awgs)
            threads.append(t)

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()

            

        


    
            
