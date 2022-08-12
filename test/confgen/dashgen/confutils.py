import sys,resource, time

def log_memory(msg=''):
    if "linux" in sys.platform.lower():
        to_MB = 1024
    else:
        to_MB = 1024 * 1024
    print("%s: Memory: %.1f MB, " % (msg,
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / to_MB),file=sys.stderr)

