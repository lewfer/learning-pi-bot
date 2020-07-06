from threading import Thread

# Helper functions
# -------------------------------------------------------------------------------------------------
def runThreadsTogether(threads):
    '''Run all threads in the list of threads and wait for them all to finish before returning'''
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def startThreads(threads):
    '''Run all threads in the list of threads'''
    for thread in threads:
        thread.start()

def joinThreads(threads):
    '''Wait for all threads in the list of threads to finish'''
    for thread in threads:
        thread.join()

