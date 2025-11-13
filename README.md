
I. Introduction

This project explores the application of Natural Language Processing (NLP) in two related tasks: analyzing user comments to determine sentiment and recommending movies based on user input. In the first task, NLP techniques are used to process textual data, such as user reviews or comments, to identify whether they express a positive or negative sentiment. Methods like tokenization, stopword removal, stemming, and vectorization (using BOW or BOP) transform raw text into structured numerical representations that machine learning models can understand. In the second task, these textual features are leveraged for content-based movie recommendations: by representing movie metadata-such as genres, keywords, plot summaries, cast, and crew-as text, NLP allows the system to compute similarities between movies and user input. Techniques like TF-IDF vectorization and cosine similarity enable the model to identify movies most relevant to a user’s comment or review. Together, these two tasks illustrate how NLP can be applied both to understand human language and to drive intelligent recommendations, turning unstructured text into actionable insights that enhance user interaction and personalization in movie discovery.

As mentioned, there are two main functions which is analyzing comments and movie recommendations. First, regarding comments' analysis, users can input raw text from keyboard or input a CSV file including 2 columns named "stt" and "reviews", in the stt columns is from 1 to number of your reviews and in the review columns includes the comments. Second, regarding movie recommendation, users can write the name of their movie or select from the selectbox in order to get film recommendations. 

Especially, we use Streamlit to design web, share.streamlit.io to make the web usable for users and Render to deploy our Machine Learning Model from notebook to API deployment.

HERE IS THE LINK FOR THE WEB : https://reviewsentimentapp-xntsyzheg3id5vbngkiq6j.streamlit.app/ ( CAUTION: If this analyzing reviews meet RunTimeError or do not give result, try to analyse AGAIN as the API deployment on Render with the freemode sometimes work kinda slow especially at the first input, from the second one it is much faster ! )

Also, we want to introduce different branches in our Github as we need different parts to be in different branches. 
First, regarding Review_Sentiment_Machine_Learning, this is the first part of our work, in this branch, we test 3 different machine learning models for the NLP problem ( Bag of Words meet Bag of Popcorns ) and find the best model along with using TFIDF, data cleaning and dump these threes in a pkl file so that we can later use in other parts. 
Second, regarding Review_Sentiment_Backend_Render, this is a branch linking to our API deployment on Render consisting artifacts where we load the pkl file mentioned before, domain where API is received and results are returned and services where we process file, handle input and return output and main where we use all the before files for Render to run. 
Third, regarding Movie_Recommendations_Machine_Learning, this a branch where we test the algorithm to test the film and run on localhost before converting to the last part is uploading to share.streamlit.io
Foruth, regarding Homepage_Combine, this is the last part of our proect, consisting of all things we did before, where we create a homepage to approach 2 functions, review.py where we load the web for Review_Sentiment_Machine_Learning model to practice and recommendations.py where we apply the algorithm for recommend we test before. 

II. Team members and task assignment
1. Thái Thanh Bình (Leader) 120% :
- Finding ideas for the project, learn about the idea and the workflow of the Machine Learning Bag of Words meets Bag of Popcorns assignment.

- Learning about streamlit and divide works for members 

- Learning about Machine Learning algorithms for Bag of Words meets Bag of Popcorns assignment.  (Logistic regression + Linear SVC)

- Learning about how to deploy machine learning model to API deployment and code the Review_Sentiment_Backend_Render part 

- Code the ReviewSentiment.ipynb in Review_Sentiment_Machine_Learning branch from first code sentence to predict_batch ( except for the data cleaning part)

- Combine codes of each member, fixing bugs when combining and uploading to Share.streamlit.io

- Code the function part in review.py in Homepage_Combine branch
2. Nguyễn Ngọc Linh (nhóm phó) 101% :
- Learning about Machine Learning algorithms for Bag of Words meets Bag of Popcorns assignment.  (Random Forest)

- Code the ReviewSentiment.ipynb from predict_batch to end ( metrics calculating and comparing part )

- Finding ideas for expanding the project idea which is Movie Recommendations, learn about the idea and its workflow.

- Code the Movie_Recommendations_Testing part and the function part in recommendations.py in Homepage_Combine branch 
3. Phùng Nhật Minh 101% :
- Code the ReviewSentiment.ipynb cleaning data part 

- Learn about the TF-IDF 

- Code the design and function in homepage.py in Homepage_Combine branch 

4. Ngô Mạnh Duy 75%:
- Code the ReviewSentiment.ipynb cleaning data part 

- Learn about the TF-IDF 

- Write report

- Make slide for presentation
5. Hoàng Linh Phương 101% :
- Code the design for homepage

- Draw and Design Homepage, Review and Recommendation Frontend

- Code the design and function in homepage.py in Homepage_Combine branch 

- Learning about streamlit

6. Nguyễn Lâm Huy 101% :
- Code the design for review.py in Homepage_Combine branch 


- Learning about streamlit
7. Lê Thị Như Ý 101% :
- Code the design for recommendations in Homepage_Combine branch 

- Learning about streamlit

III. Instructions for installing and running the code:
1. Python version used : 3.12
2. List of libraries to install: There is a requirements.txt file in each branch
3. How to run :
   i. Files such as ReviewSentiment.ipynb and Movie_Recommendation_System.ipynb : Run like normal to test the code in local computer
   ii. Go to dashboard.Render to choose respitory and choose Review_Sentiment_Backend_Render branch, build command : pip install -r requirement.txt and start command : uvicorn main:review_app --host 0.0.0.0 --port $PORT
   iii. After having the ii running, we put all the files in Homepage_Combine into a Git branch and go to share.streamlit.io to deploy ( remember choosing homepage.py )
