from matplotlib import pyplot as plt
from wordcloud import WordCloud

# change the name of the cluster file to see its word cloud
text=open("/Users/manasgaur/Desktop/MyApp/Multiprocessing/HW8_Manas_Gaur/cluster-4.txt","r").read()

wc=WordCloud().generate(text)
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.show()
