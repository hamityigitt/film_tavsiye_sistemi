#film tavsiye sisteminin gerçekleştirilmesi
import numpy as np
import pandas as pd

column_names = ['user_id','item_id','rating','timestamp']
df = pd.read_csv('users.data', sep='\t', names = column_names)
#sep='\t' dosyadaki verilerin tab ile ayrıldığını bildirir...

#result = df.head()    #dosyadaki ilk 5 satırı okur bize geri dondurur
#burada;
#item_id = filmin id 'sidir.
#user_id  =kullanıcının id'sidir.
#result = len(df) #dosyada kaç kayıt varmıs gorelim 
#100003 kayıt oldugunu bize söyler

movie_titles = pd.read_csv('movie_id_titles.csv')
#result = movie_titles.head()
# result = len(movie_titles)   #1682
# print(result)


#pandas kuuphanesini kullanarak merge işleminin gercekleştirilmesi
df = pd.merge(df,movie_titles,on='item_id') 
#ortak sütun üzerinden merge ile birlştirmw işlemi gerceklestirilmiştir.
#result = df.head()
#print(result)

#pivot table olusturmamız gerekiyor bunu nedeni
#her kullanıcı bir satır olacak ve her  film bir sutun olacak kullanıcının her filme verdiği puan ise bizim value miz olacak.  
#pivot tablomuz: 
moviemat = df.pivot_table(index = 'user_id', columns = 'title', values = 'rating')
# orneğin: 1 user id li  kullanıcılı kişi hangi 
# filmlere ne kadar puan verdi bunu gösterir
#result = moviemat.head()
#result = type(moviemat)  #dataframe 
#print(result)

#bir filmin kullanıcı ratingleri
#star wars rating
### amacımız istediğimiz filme benzer film onerisi yapmak ####
starwars_user_ratings = moviemat['Star Wars (1977)']  #olusturulan pivot tablodaki istenilen filme kullanıcıların  verdiği rating degerleri neler 
#result = starwars_user_ratings.head()
#print(result)
#corrwith() metodu aracılığıyla isteenilen filmin diğer filmlerle korelasyanunu hesaplayalım

similar_to_starwars = moviemat.corrwith(starwars_user_ratings)
#result = similar_to_starwars
#result = type(similar_to_starwars)  #pandas serisi
#print(result)  #tüm filimlerin starwars filmine göre korelasyonunu hesaplar


#seri olduğundan hata veriyor dataframe ye doonusturelim 
corr_starwars  = pd.DataFrame(similar_to_starwars,columns = ['Correlation'])
corr_starwars.dropna(inplace=True)   #nan olan kayıtları silelim program hata vermesin
#result = corr_starwars.head()
#result = corr_starwars.sort_values('Correlation',ascending = False).head(10)
#elde edilen dataframe belirlediğimiz filme en yakın korealsyon değerlerini en yüksekten en düşüğe doğru sıralar 
#!!! fakat buraya bakıldığında alakasız sonuçlar çikti (birden fazla korelasyon değeri 1 olan sonuclar cıktı)
# bakıldığında bunun sebebinin filmlerin çok az sayıda oy aldığından kaynaklandığını gördüm
#çözüm olarak 100 den az oy alan filmleri eleyelim. bu amaçla ratings isimli bir dataframe oluşturalım kaç tane oy aldığını tutalım 
#stires i izleyen birs kişi starwars a da 5 stripese de 5 vermiş bunun onune gecmeliyiz
df.drop(['timestamp'],axis=1)  #drop edemedik
#result = df.head()


#her filmin ortalama (mean value) rating degerini bulalım...
ratings = pd.DataFrame(df.groupby('title')['rating'].mean()) #baslığa göre grupla rating degerlerinin ortalamasını al
ratings.sort_values('rating',ascending=False).head()  # buyukten kucuge doğru sırala 
# en uste birden fazla 5 deger gelecek bunun nedeni bu filmi 2 kişi izlemiş iki kişide bu filme 5 vermiş ve ortalamsı 5 
#bu filmlerin kaç oy aldığınıda dikkate almamız gerekecek 


#şimdi her filmin aldığı oy sayısını bulalaım 
ratings['rating_oy_sayisi'] = pd.DataFrame(df.groupby('title')['rating'].count()) #hangi film ne kadar oy almış bakalım.
#result = ratings.head()
ratings.sort_values('rating_oy_sayisi', ascending=False).head()

#merge = iki tabloyu ortak sutuna göre birleştime işlemidir
#join = aynı satırı bulur yan yana koyar verileri(degerler unique dir (1 tanedir))
#essas amacımıza donelim 
corr_starwars.sort_values('Correlation', ascending=False).head()
corr_starwars = corr_starwars.join(ratings['rating_oy_sayisi'])
#VE sonucc

result = corr_starwars[corr_starwars['rating_oy_sayisi']>100].sort_values('Correlation',ascending=False).head()


print(result)




















