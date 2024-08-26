import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('🎬 Movie Recommender System')
st.markdown("""
This page recommends similar movies based on the selected movie. Find your next favorite film!
""")



def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=6e0b31b10c8cadb6108e19e2605b4e8b&language=en-US'.format(movie_id), timeout=15)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch poster
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters



selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.subheader('🌟 Recommended Movies:')


    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.write(names[i])
