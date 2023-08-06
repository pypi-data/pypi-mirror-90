def main():
    import speech_recognition as sr
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    scopes = 'https://www.googleapis.com/auth/youtube'
    
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',scopes)
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
    
    
    
