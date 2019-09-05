# Requires third party spotipy
import spotipy
import spotipy.util as util
import sys
import re
import os.path


# You'll also want to setup the environment variables
# SPOTIPY_CLIENT_ID
# SPOTIPY_CLIENT_SECRET
def getToken():
    token = util.prompt_for_user_token('cobertos', 'user-library-read', redirect_uri='http://localhost/')
    if token:
        return token

    raise RuntimeError("Auth failed")


#Note: redirect_uri needs to be whitelisted in your app in Spotify
#or you get an error
if __name__ == '__main__':
    sp = spotipy.Spotify(auth=getToken())

    def savedTracks():
        #Get the user tracks as an iterable, batching based on Spotify's max limit
        #https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-tracks/
        offset = 0
        limit = 50
        total = None
        while not total or (total and offset < total):
            query = sp.current_user_saved_tracks(limit=limit,offset=offset)
            #query = sp.user_playlist_tracks('coburn37', '38BHdoAzHRIpfJHJy7O2Qn') #Not on Spotify Playlist
            total = query['total'] #Save the total after the first query
            yield from query['items']
            offset += limit

    for savedTrack in savedTracks():
        track = savedTrack['track']
        artists = ", ".join([artist['name'] for artist in reversed(track['artists'])])
        exportStr = f"{artists} /// {track['name']} /// {savedTrack['added_at']} /// {track['is_local']}"
        sys.stdout.buffer.write(f"{exportStr}\n".encode('utf-8')) #Use buffer.write to print with bytes (the return of encode)
        
        #Useful for debugging the data structure of the songs
        #import pprint
        #pp = pprint.PrettyPrinter(indent=4)
        #try:
        #    wut = pp.pprint(track)
        #    if not wut:
        #        print('WUTTHEFUK')
        #    else:
        #        print(wut.encode('utf-8'))
        #except:
        #    pass
