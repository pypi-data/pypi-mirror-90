def download(url,format):
    import pafy
    mode = format
    if mode == 'mp3' or mode=='3' or mode=='MP3':
        video=pafy.new(url)
        bestau=video.getbestaudio()
        bestau.download()
    
    elif mode == 'mp4' or mode=='4' or mode=='MP4':
        video = pafy.new(url) 
        streams = video.streams 
        best = video.getbest()
        best.download()

    else:
        print("Entered invalid input as : '",mode,"'   Try again ")
