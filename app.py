import streamlit as st 
import pickle
import requests

movies_list0 = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list0['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9116bc0a5a9867c442af734c9852dbd5&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_list0[movies_list0['title'] == movie].index[0]
    distances = similarity[movie_index]
    rmovies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in rmovies_list:
        movie_id = movies_list0.iloc[i[0]].movie_id
       
        recommended_movies.append(movies_list0.iloc[i[0]].title)

         # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender')

selected_movie_name = st.selectbox(
    'Movies List',
    movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    columns = st.columns(5)
    
    for i in range(5):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i])

