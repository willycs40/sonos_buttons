import logging
import parameters as params
import buttons
from sonosmemorycontroller import SonosMemoryController


def testing(smc):
    smc.play()


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s|%(levelname)s|%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S',
        level=logging.DEBUG)

    smc = SonosMemoryController()

    #smc.pause()
    #smc.save_playlist('test')
    smc.load_playlist('test')
    #smc.play()



