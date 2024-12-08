import streamlit as st
import pickle
import numpy as np

# importing usefull files
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

# Main Function 
def recommend(book_name) -> list:
    """ Returns the recommended books """
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data


# ------------------------------------- Page Designing ----------------------------------------- #
# page header
st.header("Book Recommender System")

# taking book name as input
book_name = st.text_input(
    "",
    placeholder="Enter book name here"
)

# Button
done_btn = st.button(
    "Recommend",
    key="done"
)

@st.dialog("Invalid Book name")
def none_btn_dialog():
    st.write("Please enter something first.")



# This code runs when user click on Button['Done']
if st.session_state.done == True:
    if book_name is None:
        none_btn_dialog()
    else:
        data = recommend(book_name)

        for book in data:
            img_url = book[2]
            st.image(img_url)
        
            st.write(f"### {book[0]}")
            st.write(f"Author: :blue[{book[1]}]")
    
        
