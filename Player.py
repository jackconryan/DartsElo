class Player():
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating
    def update_rating(self, new_rating):
        self.rating = new_rating