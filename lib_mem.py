import numpy as np
import time 
import psutil
import os

# def mem_usage():
    
print(psutil.Process(os.getpid()).memory_info().rss)