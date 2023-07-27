import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f4e802f8212efafe2a238109582e6a92&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies.append(movie_title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters


movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


#frontend
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select your movie: ',
movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.text(names[0])
        st.image(posters[0])
    with m2:
        st.text(names[1])
        st.image(posters[1])
    with m3:
        st.text(names[2])
        st.image(posters[2])
    with m4:
        st.text(names[3])
        st.image(posters[3])
    with m5:
        st.text(names[4])
        st.image(posters[4])

