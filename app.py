import streamlit as st
import pickle
import pandas as pd
import requests
from requests.exceptions import ConnectionError, Timeout


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=caf58652a11e862793fe23fd3be58362"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            print(f"No poster available for movie ID {movie_id}")
            return "download.jpg"  # your local default image

    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
        return "download.jpg"
    except requests.exceptions.Timeout:
        print("The request timed out")
        return "download.jpg"
    except Exception as e:
        print("Some other error occurred:", e)
        return "download.jpg"


# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=caf58652a11e862793fe23fd3be58362"
#     try:
#         response = requests.get(url,timeout=1.5)  # Add a timeout
#         response.raise_for_status()
#         data = response.json()
#         return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#     except ConnectionError as e:
#         print("Connection error:", e)
#         return "default_image_url"
#     except Timeout:
#         print("The request timed out")
#         return "default_image_url"
#     except Exception as e:
#         print("Some other error occurred:", e)
#         return "default_image_url"





def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]  ## get movie index
    distances = similarity[movie_index]
    # get top5 similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters= []

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(  'Select movie',movies['title'].values)


if st.button('Recommend'):
    name,posters = recommend_movies(selected_movie_name)
    # for i in posters:
    #     st.text(i)


    col1, col2, col3 ,col4,col5 = st.columns(5)
    columns = [col1, col2, col3, col4,  col5]

    for i in range(5):
        with columns[i]:
            st.text(name[i])
            try:
                st.image(posters[i])
            except:
                st.image('download.jpg')