def main():
    import speech_recognition as sr
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    scopes = 'https://www.googleapis.com/auth/youtube'
    
    flow = InstalledAppFlow.from_client_secrets_file({"installed":{"client_id":"606795196106-7k5sfdvuoguap4imoco0tjcc21bhj0up.apps.googleusercontent.com","project_id":"yt-playlist-manager-300314","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"yj9PiOUO6-Oiak_XVrnQgIsd","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}},scopes)
    credentials = flow.run_console()
    
    youtube = build('youtube', 'v3', credentials= credentials, developerKey = 'AIzaSyDDiASLcaGi40XATzxatomNN75z-nFnXoQ')
    req_playlist = youtube.playlists().list(part = 'snippet,id',mine = True)
    res_playlist = req_playlist.execute()
    
    playlists = {}
    for i in res_playlist['items']:
        playlists[i['snippet']['title']] = i['id']
    
    print("Please say the name of the playlist you want to update")
    
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
    playlist = r.recognize_google(audio)
    while True:
        if playlist in playlists:
            break
        else:
            engine.say("please repeat")
            playlist = r.recognize_google(audio)
            continue
    
    print('Please say the title of the video')
    with mic as source:
        audio = r.listen(source)
    video = r.recognize_google(audio)
    
    search = youtube.search().list(part = 'snippet',q = video, maxResults = 1,order= 'viewCount')
    search_res = search.execute()
    search_res['items']
    
    req_insert = youtube.playlistItems().insert(part="snippet",
            body={
              "snippet": {
                "playlistId": playlists['playlist'],
                "position": 0,
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": search_res['items'][0]['id']['videoId']
                }
              }
            })
    res_insert =  req_insert.execute()
    
    
    
