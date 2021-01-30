# Import packages
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import itertools, collections
from wordcloud import WordCloud, STOPWORDS
import urllib
from asgiref.sync import sync_to_async
import time


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
    mc = dict(word_counts.most_common(30))
    print(mc)
    x=  mc.keys()
    y = mc.values()
    plt.figure(figsize=(15,10))
    plt.xticks(rotation =  45)
    plt.bar(x,y)
    graph = get_graph()
    return graph


def get_wordcloud(all_words):
    t0 = time.time()    
    word_counts = collections.Counter(all_words)
    mc = dict(word_counts.most_common(100))
    t2 = time.time()
    #text = " ".join(all_words)
    # Generate wordcloud
    """width = 3000, height = 2000, random_state=1, background_color='black', colormap='Set2', collocations=False"""
    wc = WordCloud(max_font_size=50, max_words=100,width=600, height=400, background_color="white").generate_from_frequencies(mc)
    plt.figure(figsize=(15,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    graph = get_graph()
    t1 = time.time()
    print("countingwords",t2-t0)
    print("get_wcloud_run_time",t1-t0)
    return graph