import logging
import parameters as params
import soco
import json
import threading
import time

class SonosMemoryController:

    def __init__(self):
        self.read_playlists()
        self.thread = None
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
            
    def delete_playlist(self, playlist_name):

        if playlist_name in self.playlists:
            self.playlists.pop(playlist_name)
            self.write_playlists()
        else:
            logging.debug('No playlist called {} to remove'.format(playlist_name))

    def load_playlist_threaded(self, playlist_name):

        if playlist_name not in self.playlists:
            logging.debug('No playlist called: {}'.format(playlist_name))
            return

        self.thread = PlaylistLoader(sonos=self.sonos, playlist=self.playlists[playlist_name])
        self.thread.start()

    def cancel_running_thread(self):
        if self.thread:
            self.thread.stop()

class PlaylistLoader(threading.Thread):

    def __init__(self, sonos, playlist):
        super(PlaylistLoader, self).__init__()
        self.sonos = sonos
        self.playlist = playlist
        self._stop_event = threading.Event()
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.isSet()

    def run(self):

        # clear the queue
        self.sonos.clear_queue()

        if self.stopped():
            return

        # add and kick off the first track
        self.sonos.add_uri_to_queue(self.playlist[0])

        if self.stopped():
            return

        self.sonos.play_from_queue(0)

        # add the rest of the tracks
        for track in self.playlist[1:]:
            if self.stopped():
                break
            self.sonos.add_uri_to_queue(track)