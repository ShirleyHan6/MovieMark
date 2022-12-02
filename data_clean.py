import pandas as pd
import string

df1 = pd.read_csv('imdb_top_1000_original.csv')
df1.head()
print("Original number of rows: ", df1.shape[0])
df1.drop_duplicates()
print("After removing duplicates: ", df1.shape[0])
drop_columns_not_nan = ['Poster_Link', 'Series_Title', 'Released_Year', 'Runtime', 'Genre', 'IMDB_Rating',
                        'Overview', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']
for column in drop_columns_not_nan:
    df1 = df1[df1[column].notna()]
print("After dropping rows with NaN: ", df1.shape[0])

df2 = pd.read_csv('tmdb_movies_data_original.csv')
print("Original number of rows: ", df2.shape[0])
df2.drop_duplicates()
print("After removing duplicates: ", df2.shape[0])
print(len(df2.isnull()))
drop_columns_not_nan = ['vote_average', 'release_year', 'genres', 'overview', 'tagline', 'keywords',
                        'director', 'homepage', 'cast', 'original_title', 'budget', 'revenue', 'runtime']
for column in drop_columns_not_nan:
    df2 = df2[df2[column].notna()]
print("After removing rows  with NaN: ", df2.shape[0])

for i in df1.index:
    for j in df2.index:
        if df1.at[i, 'Series_Title'].lower() == df2.at[j, 'original_title'].lower() \
            and df1.at[i, 'Director'].lower() == df2.at[j, 'director'].lower()\
            and str(df1.at[i, 'Released_Year']).translate(str.maketrans('', '', string.punctuation)) == \
                str(df2.at[j, 'release_year']).translate(str.maketrans('', '', string.punctuation)):
            if df1.at[i, 'Series_Title'] != df2.at[j, 'original_title']:
                df1.at[i, 'Series_Title'] = df2.at[j, 'original_title']
                print("fixed")
            if df1.at[i, 'Director'] != df2.at[j, 'director']:
                df1.at[i, 'Director'] = df2.at[j, 'director']
                print("fixed")
            if str(df1.at[i, 'Released_Year']) != str(df2.at[j, 'release_year']):
                df1.at[i, 'Released_Year'] = df2.at[j, 'release_year']
                print("fixed")

df1.to_csv('imdb_movies_data.csv')
df2.to_csv('tmdb_movies_data.csv')
# indexdrop = df1[(df1['Series_Title'].lower() in tmdb_title) | (df['Position'] == 'SG') ].index
# df.drop(indexdrop , inplace=True)
# df.head(15)


# test_str.translate
#     (str.maketrans('', '', string.punctuation))
