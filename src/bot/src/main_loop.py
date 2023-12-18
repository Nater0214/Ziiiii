# src/bot/src/main_loop.py


# Imports
from threading import Thread


class MainLoop(Thread):
    def __init__(self):
        self.terminate_flag = False

    
    def __call__(self):
        super().__init__(target=self._loop)
        self.start()
    
    
    def stop(self):
        self.terminate_flag = True
        self.thrd.join()
    
    
    def _loop(self):
        pass

main_loop = MainLoop()