import pandas as pd 
import numpy as np

import matplotlib
# matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt

# print("Switched to:",matplotlib.get_backend())

import plotly.express as px

from sklearn.cluster import KMeans



def preprocess_data(file):
    df = pd.read_csv(file,sep=',')

    # df = pd.DataFrame(file, columns=file[0])

    #preprocessing data
    df.drop(['strike1', 'dip1', 'rake1', 'strike2', 'dip2', 'rake2'], axis=1, inplace=True)

    #mengganti format tgl dari varchar menjadi dateS
    df['tgl'] = pd.to_datetime(df['tgl'], format='%Y-%m-%d')

    #sorting data dari tgl dan timestamp terkecil ke terbesar
    df = df.sort_values(['tgl', 'ot'],
                ascending = [True, True])

    #menyimpan data yang telah di preprocessing data
    df.to_csv('data_gempa.csv', index=False)

    dataset = pd.read_csv('data_gempa.csv')
    data = pd.DataFrame(dataset, columns=['tgl', 'ot', 'lat', 'lon', 'depth', 'mag', 'remark'])

    return data

    # Hasil clustering
    # print('Hasil clustering')
    # print('Centroid KMeans \n', kmeans_centroid)
    # print ('Data hasil clustering \n', data)



def result_data(data):
    k=3
    kmeans = KMeans(n_clusters=k,  random_state=10).fit(data[['lat', 'lon', 'depth', 'mag']])
    kmeans_labels = kmeans.labels_
    kmeans_centroid = kmeans.cluster_centers_

    data['klaster'] = kmeans_labels

    # Visualisasi hasil clustering
    fig, ax1 = plt.subplots()
    ax1.scatter(data['depth'], data['mag'], c=kmeans_labels)
    ax1.scatter(kmeans_centroid[:,2], kmeans_centroid[:,3], color = 'black', marker  = '+', label='center')
    ax1.set(xlabel='Kedalaman', ylabel='Magnitudo')

    plt.suptitle('Hasil Clustering Algoritma K-Means',  fontsize=14, fontweight='bold')
    # plt.show()
    plt.savefig('C:\\Users\\ASUS\\OneDrive\\Desktop\\FINAL PROGRAM\\frontend\\public\\assets\\image\\fig_scatter.jpg')

    #hasil return
    #visualisasi boxplot untuk distribusi variabel tiap cluster
    cluster_colors = ['#636efa', '#ef553b', '#00cc96', '#fa63e7', '#6efa63', '#faef63']
    features = kmeans.feature_names_in_
    ncols=4
    nrows=len(features) // ncols + (len(features)%ncols >0)
    fig = plt.figure(figsize=(15,15))

    for n, feature in enumerate(features):
        ax = plt.subplot(nrows, ncols, n+1)
        box = data[[feature, 'klaster']].boxplot(by='klaster', ax=ax, return_type='both', patch_artist=True)

        for row_key, (ax,row) in box.iteritems():
            ax.set_xlabel('cluster')
            ax.set_title(feature, fontweight='bold')
            for i, box in enumerate(row['boxes']):
                box.set_facecolor(cluster_colors[i])
    plt.suptitle('Distribusi Parameter Di Tiap Klaster', fontsize=18, y=1)
    plt.tight_layout()

    plt.savefig('C:\\Users\\ASUS\\OneDrive\\Desktop\\FINAL PROGRAM\\frontend\public\\assets\\image\\fig_boxplot.jpg')
    # plt.show()

    #hasil return
    #frekuensi gempa tiap klaster
    data1 = len(data[(data['mag'] < 5) & (data['klaster'] == 0)])
    data2 = len(data[((data['mag'] >= 5) & (data['mag'] <7)) & (data['klaster'] == 0)])
    data3 = len(data[(data['mag'] >= 7) & (data['klaster'] == 0)])

    data4 = len(data[(data['mag'] < 5) & (data['klaster'] == 1)])
    data5 = len(data[((data['mag'] >= 5) & (data['mag'] <7)) & (data['klaster'] == 1)])
    data6 = len(data[(data['mag'] >= 7) & (data['klaster'] == 1)])

    data7 = len(data[(data['mag'] < 5) & (data['klaster'] == 2)])
    data8 = len(data[((data['mag'] >= 5) & (data['mag'] <7)) & (data['klaster'] == 2)])
    data9 = len(data[(data['mag'] >= 7) & (data['klaster'] == 2)])

    N=3
    ind=np.arange(N)
    width = 0.25

    fig = plt.subplots()

    klaster1 = [data1,data2,data3]
    bar1 = plt.bar(ind,klaster1, width, color ='r')
    klaster2 = [data4, data5, data6]
    bar2 = plt.bar(ind+width, klaster2, width, color='g')
    klaster3 = [data7, data8, data9]
    bar3 = plt.bar(ind+width*2, klaster3, width, color='b')


    plt.xlabel('Magnitudo')
    plt.ylabel('Frekuensi')
    plt.title('Frekuensi Kejadian Gempa Tiap Klaster Berdasarkan Magnitudo')

    plt.bar_label(bar1, padding=3)
    plt.bar_label(bar2, padding=3)
    plt.bar_label(bar3, padding=3)

    plt.xticks(ind+width, ['<5', '5-7', '>7'])
    plt.legend((bar1,bar2,bar3), ('Klaster 1', 'Klaster 2', 'Klaster 3'))
    plt.tight_layout()
    # plt.show()

    plt.savefig('C:\\Users\\ASUS\\OneDrive\\Desktop\\FINAL PROGRAM\\frontend\public\\assets\\image\\fig_frekuensi.jpg')

    #hasil return
    #visualisasi hasil clustering dalam bentuk peta
    data['klaster'] = data['klaster'].astype(str)
    fig_map = px.scatter_mapbox(data, lat="lat", lon="lon", zoom=3, color = "klaster", title ="Algoritma K-Means", mapbox_style="carto-positron")
    # fig_map.show()
    # fig.save('map.html')
    fig_map.write_html('C:\\Users\\ASUS\\OneDrive\\Desktop\\FINAL PROGRAM\\frontend\\src\\map.html')

    return data
