
I. Introduction

This project explores the application of Natural Language Processing (NLP) in two related tasks: analyzing user comments to determine sentiment and recommending movies based on user input. In the first task, NLP techniques are used to process textual data, such as user reviews or comments, to identify whether they express a positive or negative sentiment. Methods like tokenization, stopword removal, stemming, and vectorization (using BOW or BOP) transform raw text into structured numerical representations that machine learning models can understand. In the second task, these textual features are leveraged for content-based movie recommendations: by representing movie metadata-such as genres, keywords, plot summaries, cast, and crew-as text, NLP allows the system to compute similarities between movies and user input. Techniques like TF-IDF vectorization and cosine similarity enable the model to identify movies most relevant to a user’s comment or review. Together, these two tasks illustrate how NLP can be applied both to understand human language and to drive intelligent recommendations, turning unstructured text into actionable insights that enhance user interaction and personalization in movie discovery.

As mentioned, there are two main functions which is analyzing comments and movie recommendations. First, regarding comments' analysis, users can input raw text from keyboard or input a CSV file including 2 columns named "stt" and "reviews", in the stt columns is from 1 to number of your reviews and in the review columns includes the comments. Second, regarding movie recommendation, users can write the name of their movie or select from the selectbox in order to get film recommendations. 

Especially, we use Streamlit to design web, share.streamlit.io to make the web usable for users and Render to deploy our Machine Learning Model from notebook to API deployment
II. Team members and task assignment

1. Thái Thanh Bình (Leader) 115% :
- Finding ideas for the project, learn about the idea and the workflow of the Machine Learning Bag of Words meets Bag of Popcorns assignment.

- Learning about streamlit and divide works for members 

- Learning about Machine Learning algorithms for Bag of Words meets Bag of Popcorns assignment.  (Logistic regression + Linear SVC)

- Learning about how to deploy machine learning model to API deployment and code the Review_Sentiment_Backend_Render part 

- Code the ReviewSentiment.ipynb from first code sentence to predict_batch ( except for the data cleaning part)

- Combine codes of each member, fixing bugs when combining and uploading to Share.streamlit.io
2. Nguyễn Ngọc Linh (nhóm phó) 102% :
- Learning about Machine Learning algorithms for Bag of Words meets Bag of Popcorns assignment.  (Random Forest)

- Code the ReviewSentiment.ipynb from predict_batch to end ( metrics calculating and comparing part )

- Finding ideas for expanding the project idea, learn about the idea and the workflow of Movie Recommendations

- 
3. Phùng Nhật Minh 102% :
- Code the ReviewSentiment.ipynb cleaning data part 

- Learn about the TF-IDF 

- Code the design for homepage

4. Ngô Mạnh Duy 75%:
- Code the ReviewSentiment.ipynb cleaning data part 

- Learn about the TF-IDF 

- Write report

- Make slide for presentation
5. Hoàng Linh Phương 102% :
- Code the design for homepage

- Draw and Design Homepage, Review and Recommendation Frontend

- Code the design for homepage

- Learning about streamlit

6. Nguyễn Lâm Huy 102% :
- Code the design for review

- Learning about streamlit
7. Lê Thị Như Ý 102% :
- Code the design for recommendations

- Learning about streamlit

III. Instructions for installing and running the code:
1. Python version used : 3.12
2. List of libraries to install: There is a requirements.txt file in each branch
3. How to run :
   i. Files such as ReviewSentiment.ipynb and Movie_Recommendation_System.ipynb : Run like normal to test the code in local computer
   ii. In the branch, Review_Sentiment_Backend_Render, to upload the API into a deployment web, we first put all the files in this branch in a Git branch and go into Dashboard.render and deploy
   iii. After having the ii, running, we put all the files in Homepage_Combine into a Git branch and go to share.streamlit.io to deploy
