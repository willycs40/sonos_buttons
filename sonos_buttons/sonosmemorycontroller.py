import logging
import parameters as params
import soco
import json

class SonosMemoryController:

    def __init__(self):
        self.load_stations()
        self.connect()

    def connect(self):
        self.sonos = soco.SoCo(params.SONOS_IP)

    def play(self):
        self.sonos.play()

    def pause(self):
        self.sonos.pause()

    def load_stations(self):
        try:
            with open(params.STATIONS_FILENAME, 'r') as f:
                self.stations = json.load(f)    
        except:
            self.stations = {}

    def save_stations(self):
        with open(params.STATIONS_FILENAME, 'w') as f:
            json.dump(self.stations, f)

    def set_station(self, station_name):

        queue = self.sonos.get_queue(max_items=250)
        
        tracks = []
        if queue is not None:            
            for track in queue:
                tracks.append(track.to_dict())

        self.stations[station_name] = tracks

        self.save_stations()

    def open_station(self, station_name):

        if station_name not in self.stations:
            logging.debug('No station called: {}'.format(station_name))
            return

        try:
            # clear the queue
            sonos.clear_queue()

            # add and kick off the first track
            #sonos.add_uri_to_queue(artist['tracks'][0]['uri'])
            #sonos.play_from_queue(0)

            # add the rest of the tracks
            #for item in artist['tracks'][1:]:
            #    sonos.add_uri_to_queue(item['uri'])
                
        except:
            print("Issue calling Sonos.")