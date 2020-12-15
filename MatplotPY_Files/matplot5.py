from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

Artists = ['Ariana Grande', 'Bad Bunny','Justin Beiber', 'DaBaby', 'Megan Three Stalliion']

Avg_Word_Count = [399.33, 332.66, 281.5, 662.25, 540]

plt.bar(Artists, Avg_Word_Count)

plt.title("Average word count for top performing artists")

plt.xlabel('Artists')

plt.ylabel("Average word count")

plt.tight_layout()

plt.show()
