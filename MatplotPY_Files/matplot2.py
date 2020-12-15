# spotifysongsAPI
from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

slices = [66, 34]
labels = ['Album', 'Single']
explode = [0, 0.1]

plt.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'}, explode=explode, shadow=True, startangle=90, autopct='%1.1f%%')

plt.title("SpotifySongAPI Type")
plt.tight_layout()
plt.show()
