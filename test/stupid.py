import eyed3

meta = eyed3.load('C:/Users/j4ix/Documents/temp/Nasko - Maybe [DSG PREMIERE].mp3')
genre = meta.tag.genre
print(genre)
print(type(genre))
meta.tag.non_std_genre = genre
