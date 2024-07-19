
heat_map_URls = {"Iowa":"https://carleton.maps.arcgis.com/apps/Embed/index.html?webmap=5cd9a917f230485d8faf69498a946cd9&extent=-99.2284,39.2199,-87.7147,44.5399&zoom=true&previewImage=false&scale=true&search=true&searchextent=true&disable_scroll=true&theme=dark",
                "US": "https://carleton.maps.arcgis.com/apps/Embed/index.html?webmap=5cd9a917f230485d8faf69498a946cd9&extent=-141.8018,10.2505,-49.6924,55.7892&zoom=true&previewImage=false&scale=true&search=true&searchextent=true&disable_scroll=true&theme=light",
                }

highest_google_map_URLs = {
    "Iowa":"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d48309.811509081745!2d-91.22510295481115!3d40.81998491147134!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87e132f08bf6e487%3A0x31804d6f513c96d6!2sWest%20Burlington%2C%20IA!5e0!3m2!1sen!2sus!4v1684447628548!5m2!1sen!2sus",
}

lowest_google_map_URLs = {
    "Iowa" : "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23803.936073405966!2d-93.73299490486794!3d41.774609110182766!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x87ee8224595186fb%3A0x3b1edf636cfc7af8!2sPolk%20City%2C%20IA%2050226!5e0!3m2!1sen!2sus!4v1684447794659!5m2!1sen!2sus",
}

class EmbeddedURLs:
    '''
    This class exists to return the correct urls responsible for our embedded maps.
    '''
    def get_highest_CR_map_URL(self, state):
        return highest_google_map_URLs[state]
    
    def get_lowest_CR_map_URL(self, state):
        return lowest_google_map_URLs[state]
    
    def get_heat_map_URL(self, state):
        return heat_map_URls[state]

