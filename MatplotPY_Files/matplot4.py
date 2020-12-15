from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

Artists = ['Ariana Grande','Bad Bunny','Justin Beiber', 'DaBaby', 'Megan Three Stalliion']

Number = [3, 10, 4, 4, 3]

plt.bar(Artists, Number)

plt.title("Top Performing Artists")

plt.xlabel('Artists')

plt.ylabel("Number of Songs on Top 100 Billboard 2020")

plt.tight_layout()

plt.show()
