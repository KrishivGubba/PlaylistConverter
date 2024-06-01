from ytmusicapi import YTMusic

 #hello i am testing something, what now?
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

            # trackinfo[dict["title"]] = dict["artists"]

        final = {
            "title":title,
            "description":description,
            "image":image,
            "tracks":trackinfo,
            "id" : id
        }
        # for key in final:
        #     print(key, final[key])
        return final
    
    def getplaylistarray(self, array):
        details= [ ]
        for i in range(0, len(array)):
            try:
                details.append(self.getplaylist(array[i]))
            except:
                details.append(f"error at {i}")
        return details


tube = youtubemusic()
print(tube.getplaylist("PLRovNv8H-V5FnFDPl9tWcSEM6YN8xmDoe"))
