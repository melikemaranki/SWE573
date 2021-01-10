# Import packages
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import itertools, collections
from wordcloud import WordCloud, STOPWORDS
import urllib

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(all_words):
    # Most common words
    word_counts = collections.Counter(all_words)
    mc = word_counts.most_common(10)
    x=  [i[0] for i in mc]
    y = [i[1] for i in mc]
    plt.figure(figsize=(10,10))
    plt.xticks(rotation =  45)
    plt.bar(x,y)
    graph = get_graph()
    return graph

def get_wordcloud(all_words):
    text = " ".join(all_words)
    # Generate wordcloud
    wc = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', colormap='Set2', collocations=False, stopwords = STOPWORDS).generate(text)
    
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    graph = get_graph()
    return graph