class Track:
    """Represents a track"""

    def __init__(self, track_name, artist):
        self.track_name = track_name
        self.artist = artist

    @staticmethod
    def are_equivalent(track_1, track_2):
        """Returns true if the given tracks are equivalent (ie: same track name and artist)"""
        return track_1.track_name.casefold() == track_2.track_name.casefold() \
            and track_1.artist.casefold() == track_2.artist.casefold()

    def __eq__(self, other):
        return isinstance(other, Track) \
               and self.track_name == other.track_name \
               and self.artist == other.artist \

    def __repr__(self):
        return str(self.__dict__)
