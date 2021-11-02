class Song:

    title = ""
    lyrics = ""
    chords_list = {}
    categories = []

    def __init__(self,title,lyrics,chords_list,categories):
        self.title = title
        self.lyrics = lyrics
        self.chords_list = chords_list
        self.categories = categories

    def addCategory(self, category):
        self.categories.append(category)

    def removeCategory(self, category):
        if category in self.categories:
            self.categories.remove(category)

    def addChord(self, chord, position):
        self.chords_list[position] = chord

    def removeChord(self, position):
        if position in self.chords_list.keys():
            self.chords_list.pop(position)