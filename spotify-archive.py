# export SPOTIPY_CLIENT_ID=''
# export SPOTIPY_CLIENT_SECRET=''
# export SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'

import spotipy
from spotipy.oauth2 import SpotifyOAuth

if __name__ == "__main__":
  scope = 'user-follow-read, playlist-read-private, user-library-read'
  sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

  artists = list()
  albums = list()
  saved_tracks = list()
  saved_shows = list()

  limit = 20

  # Get Artists
  results = sp.current_user_followed_artists(limit)
  total_artists = int(results['artists']['total'])
  results_artists = results['artists']['items']

  print('Getting artists... Total: {}'.format(total_artists))
  while (len(artists) < total_artists):
    last_id = ''
    for r in results_artists:
      artists.append('{} - id: {}'.format(r['name'], r['id']))
      last_id = r['id']
    results = sp.current_user_followed_artists(limit, last_id)
    results_artists = results['artists']['items']

  print('Added: {}'.format(len(artists))) 

  if (len(artists) != total_artists):
    print('Some artists were not saved...')

  artists_file = open('artists_file.txt', 'w')
  artists_file.writelines(artists)
  artists_file.close()

  # Get Albums
  results = sp.current_user_saved_albums(limit)
  total_albums = int(results['total'])
  results_albums = results['items']

  print('Getting albums... Total: {}'.format(total_albums))
  offset = 0
  while (len(albums) < total_albums):
    for r in results_albums:
      artists_in_album = r['album']['artists']
      artists_tmp = list()
      for a in artists_in_album:
        artists_tmp.append(a['name'])
      album_name = r['album']['name']
      offset += 1
      albums.append('{} - {}'.format(album_name, ', '.join(artists_tmp)))

    results = sp.current_user_saved_albums(limit, offset)
    results_albums = results['items']

  print('Added: {}'.format(len(albums)))

  if (len(albums) != total_albums):
    print('Some albums were not saved...')

  albums_file = open('albums_file.txt', 'w')
  albums_file.writelines(albums)
  albums_file.close()  

  # Get all saved tracks
  results = sp.current_user_saved_tracks(limit)
  total_saved_tracks = int(results['total'])
  results_saved_tracks = results['items']

  print('Getting saved tracks... Total: {}'.format(total_saved_tracks))
  offset = 0
  while (len(saved_tracks) < total_saved_tracks):
    for t in results_saved_tracks:
      track_name = t['track']['name']
      track_artists = t['track']['album']['artists']
      artists_tmp = list()
      for a in track_artists:
        artists_tmp.append(a['name'])
      offset += 1
      saved_tracks.append('{} - {}'.format(track_name, ', '.join(artists_tmp)))
    results = sp.current_user_saved_tracks(limit, offset)
    results_saved_tracks = results['items']

  print('Added: {}'.format(len(saved_tracks))) 

  if (len(saved_tracks) != total_saved_tracks):
    print('Some saved_tracks were not saved...')

  saved_tracks_file = open('saved_tracks_file.txt', 'w')
  saved_tracks_file.writelines(saved_tracks)
  saved_tracks_file.close()

  # Get all saved shows
  results = sp.current_user_saved_shows(limit)
  total_saved_shows = int(results['total'])
  results_saved_shows = results['items']

  print('Getting saved shows... Total: {}'.format(total_saved_shows))
  offset = 0
  while (len(saved_shows) < total_saved_shows):
    for t in results_saved_shows:
      show_name = t['show']['name']
      offset += 1
      saved_shows.append('{}'.format(show_name))
    results = sp.current_user_saved_shows(limit, offset)
    results_saved_shows = results['items']

  print('Added: {}'.format(len(saved_shows)))   

  if (len(saved_shows) != total_saved_shows):
    print('Some saved_shows were not saved...')

  saved_shows_file = open('saved_shows_file.txt', 'w')
  saved_shows_file.writelines(saved_shows)
  saved_shows_file.close()