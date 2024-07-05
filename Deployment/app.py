import streamlit as st
import pandas as pd
import pickle
import time
import requests 

# Loading the required dataset and similarity set
data = pickle.load(open(r"C:\Users\rashi\DATASCIENCE\ML Projects\CurrentProject\MovieRecommenderSystem\DataDic.pkl", "rb"))
dataset = pd.DataFrame(data)
similar_movies=pickle.load(open(r"C:\Users\rashi\DATASCIENCE\ML Projects\CurrentProject\MovieRecommenderSystem\similar.pkl","rb"))


#Function to fetch poster from website
def fetch_posters(movie_id):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YzU1NzYwNmJhNTRjMDY2NzM4NmM0MjhiNjYwYWQyNSIsIm5iZiI6MTcyMDA5NTA5Ny41MTYxMDgsInN1YiI6IjY2ODY4ODhkNzFiMjM4ZmZmNzE3ZTRlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.TjfCAcCUfpWsDWdffkJ_IH_ThIm4Rpz9jpsnYfAbgK4"
    }
    res=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?",headers=headers)
    info=res.json()
    return "https://image.tmdb.org/t/p/w500/" + info["poster_path"]



#Recommending function 
def recommend(name):
    movie_index=dataset[dataset["title"]==name].index[0]
    current_list=sorted(list(enumerate(similar_movies[movie_index])),reverse=True,key=lambda x:x[1])[1:6]
    movie_name=[]
    movie_posters=[]
    for i in current_list:
        movie_id=dataset.iloc[i[0]]["id"]
        movie_name.append(dataset.iloc[i[0]]["title"])
        # fetching poster from tmdb website
        movie_posters.append(fetch_posters(movie_id))
    return movie_name,movie_posters


#Interface
st.title("The Movie Recommender System")
movie_list = dataset['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    with st.spinner("Wait for a sec..."):
        time.sleep(2)
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.image(recommended_movie_posters[0])
            st.text(recommended_movie_names[0])
        with col2:
           
            st.image(recommended_movie_posters[1])
            st.text(recommended_movie_names[1])

        with col3:
           st.image(recommended_movie_posters[2])
           st.text(recommended_movie_names[2])
           
        with col4:
           st.image(recommended_movie_posters[3])
           st.text(recommended_movie_names[3])
           
        with col5:
           st.image(recommended_movie_posters[4])
           st.text(recommended_movie_names[4])
           
        st.success("Done!")


  
    