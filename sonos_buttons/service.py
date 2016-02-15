import logging
import parameters as params
import time
from sonosmemorycontroller import SonosMemoryController


def testing(smc):
    smc.play()

if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.INFO)

    smc = SonosMemoryController()

    #smc.pause()

    #thread = threading.Thread(target=smc.save_playlist('Beach'), args=())
    #thread.setDaemon(True)
    #thread.start()
    smc.load_playlist_threaded('Beach')
    time.sleep(1)
    smc.cancel_threads()
    #smc.play()




