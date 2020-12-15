# Hot 100
from matplotlib import pyplot as plt


plt.style.use('fivethirtyeight')

# songs = []
# conn = sqlite3.connect(
#     '/Users/Hamza Asad/Desktop/FinalProject206/MusicStats.db')
# cur = conn.cursor()
# cur.execute(f"SELECT numWeeks FROM TABLE Hot100 WHERE numWeeks={numWeeks}")

# for x in cur:
#     songs.append(x)
# conn.commit()
# print(songs)

Weeks = [17, 40, 6, 35, 5, 16, 11, 49, 32, 15, 53, 17, 16, 2, 30, 11, 22, 23, 17, 4, 16, 10, 8, 16, 5,
         9, 22, 2, 25, 6, 21, 25, 17, 5, 33, 7, 17, 2, 2, 9, 4, 44, 28, 22, 5, 7, 4, 43, 19, 37, 3, 13, 1, 15, 9, 9, 16, 11, 2, 1, 13, 14, 14, 1, 1, 18, 15, 6, 4, 9, 18, 1, 16, 1, 1, 16, 9, 1, 1, 5, 1, 7, 1, 2, 7, 2, 1, 4, 9, 13, 6, 7, 9, 1, 1, 3, 18, 8, 6, 2]

bins = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40.44, 48, 52]

plt.hist(Weeks, bins=bins, edgecolor='black')

plt.title('Songs and Weeks on billboard')

plt.xlabel('Weeks On Billboard')

plt.ylabel('Songs')

plt.tight_layout()

plt.show()
