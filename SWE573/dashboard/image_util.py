# Import packages
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import itertools, collections
from wordcloud import WordCloud, STOPWORDS
import urllib
from asgiref.sync import sync_to_async
import time
import nltk
import pandas as pd
import networkx as nx


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
    # Generate wordcloud
    wc = WordCloud(max_font_size=50, max_words=100,width=600, height=400, background_color="white").generate_from_frequencies(mc)
    plt.clf() 
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    graph = get_graph()
    t1 = time.time()
    print("countingwords",t2-t0)
    print("get_wcloud_run_time",t1-t0)
    return graph

def get_network(all_words):
    x = (pd.Series(nltk.ngrams(all_words, 2)).value_counts())[:100]
    zipped = x.keys()
    unzipped_object = zip(*zipped)
    unzipped_list = list(unzipped_object) 
    a, b = unzipped_list
    #print(all_words)
    nodes = list(a) +list(b)
    edges = x.index.to_list()
    #print("type", type(edges))
    #print("nodes",nodes, "edges",edges)
    plt.clf() 
    
    #G=nx.path_graph(4)
    #pos=nx.circular_layout(G)
    G = nx.karate_club_graph()             
    G.add_nodes_from(nodes)                   
    G.add_edges_from(edges)     
    nx.draw_spring(G,node_size=0,edge_color='b',font_size=13, with_labels = True)#draw(G, with_labels=True, pos = pos)
    plt.show()

    graph = get_graph()
    return graph
