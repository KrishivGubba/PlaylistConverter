from ytmusicapi import YTMusic

class youtubemusic():
    def __init__(self):
        self.ytmusic = YTMusic("oauth.json")
    
    def getplaylist(self, id):
        data = self.ytmusic.get_playlist(id)
        title = data["title"]
        description = data["description"] if data["description"]!=None else ""
        image = data["thumbnails"][0]["url"]
        alltracks = data["tracks"]
        trackinfo = {}
        for dict in alltracks:
            trackname = dict["title"]
            artistslist = []
            for artist in dict["artists"]:
                artistslist.append(artist["name"])
            trackinfo[trackname] = artistslist
        final = {
            "title":title,
            "description":description,
            "image":image,
            "tracks":trackinfo,
            "id" : id
        }
        return final
    
    def getplaylistarray(self, array):
        details= [ ]
        for i in range(0, len(array)):
            try:
                details.append(self.getplaylist(array[i]))
            except:
                details.append(f"error at {i}")
        return details
