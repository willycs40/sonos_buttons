import logging
import parameters as params
import soco
import json

class SonosMemoryController:

    def __init__(self):
        self.read_playlists()
        self.connect()

    def connect(self):
        self.sonos = soco.SoCo(params.SONOS_IP)

    def play(self):
        self.sonos.play()

    def pause(self):
        self.sonos.pause()

    def read_playlists(self):
        try:
            with open(params.PLAYLISTS_FILENAME, 'r') as f:
                self.playlists = json.load(f)    
        except:
            self.playlists = {}

    def write_playlists(self):
        with open(params.PLAYLISTS_FILENAME, 'w') as f:
            json.dump(self.playlists, f)

    def save_playlist(self, playlist_name):

        queue = self.sonos.get_queue(max_items=250)
        
        tracks = []
        if queue is not None:            
            for track in queue:
                tracks.append(track.resources[0].uri)

        self.playlists[playlist_name] = tracks

        self.write_playlists()

    def load_playlist(self, playlist_name):

        if playlist_name not in self.playlists:
            logging.debug('No playlist called: {}'.format(playlist_name))
            return


        # clear the queue
        self.sonos.clear_queue()

        # add and kick off the first track
        self.sonos.add_uri_to_queue(self.playlists[playlist_name][0])
        self.sonos.play_from_queue(0)

        # add the rest of the tracks
        for track in self.playlists[playlist_name][1:]:
            self.sonos.add_uri_to_queue(track)
            
