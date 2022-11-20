import matplotlib.pyplot as plt
from wordcloud import WordCloud


def read_file(fileName):
    words = []
    f = open(fileName, 'r', encoding="utf-8")
    for line in f:
        line = line.strip()
        words.append(line)
    result = ' '.join([str(elem) for elem in words])
    return result


word_cloud = WordCloud(width=1400, height=1400, collocations=False, background_color="#FFFEC8").generate(
    read_file("output/result.txt"))

plt.Figure(figsize=(15, 15))
plt.imshow(word_cloud)
plt.axis("off")
plt.savefig("graphic_results/wordCloud.png", format="png", dpi=200)
plt.show()
