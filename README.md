# Industrial and Scientific Product Recommender System

The motivation behind this project lies in the need to build a recommender system by leveraging the strength of neural networks and collaborative filtering to help users in the industrial and scientific community discover new products, explore different categories, and make informed decisions. This system predicts users' ratings for products that users have not yet rated and recommends the highest-rated products.

It utilises a neural network and user-based collaborative filtering to capture latent factors and non-linear patterns in user-item interactions, enabling personalised recommendations. Specifically, it learns embeddings of users and products from past interactions. These embeddings are then combined through dense neural layers to predict ratings for new user-product pairs. 

By using embeddings and a neural network, the model can predict ratings more accurately than traditional methods. This is because the embeddings capture the latent features of users and products, which are not directly observable. The neural network then learns to use these latent features to predict ratings.

This project focuses on simplicity and efficiency. By providing personalised recommendations based on predicted ratings, the aim is to enhance the user experience, provide recommendations that align with the unique preferences of each individual and simplify the process of finding relevant products.


## Project Description

The system is divided into the following components:

- Data Ingestion: This component fetches the Amazon data from an external source and performs initial data preprocessing.  
- Data Preprocessing: This component loads, encodes, and normalises data, calculates statistics, divides the data into train and val sets, and saves the preprocessed data and necessary parameters.
- Build Model: This component builds and compiles a neural network to predict ratings.  
- Train Model: This component trains the neural network on the training data.  
- Evaluate Model: This component evaluates the performance of the neural network on the validation data.  
- Inference: This component generates recommendations based on the predicted ratings for unrated products and recommends a specified number of relevant products to individual users.
- User Interface: This component focuses on creating interactive web applications and interfaces for the recommender system.
- Deployment: This component deals with the containerisation of the web [application](https://scientific-product-recommender-system.onrender.com/) using Docker and deployment on the [cloud](https://render.com/). 


## Data

This subset of Amazon Review Data (2018), consisting of 77,071 reviews, is obtained by filtering out users and items that do not meet the minimum requirement of having at least 5 reviews each. Focusing on this dense data subset of frequent users and popular items facilitates the discovery of meaningful patterns within the data. This benefits both the analysis of user behaviours and product properties, as well as the development of high-performance recommendation models.

| Column Name     | Description                                                        |
| --------------- | ------------------------------------------------------------------ |
| asin            | ID of the product, e.g. 0000013714                                 |
| image           | Images that users post after they have received the product        |
| overall         | Rating of the product                                              |
| reviewText      | Text of the review                                                 |
| reviewTime      | Time of the review (raw)                                           |
| reviewerID      | ID of the reviewer, e.g. A20SUNCQVVYYZO                            |
| reviewerName    | Name of the reviewer                                               |
| style           | A dictionary of the product metadata, e.g., "Format" is "Hardcover"|
| summary         | Summary of the review                                              |
| unixReviewTime  | Time of the review (Unix time)                                     |
| vote            | Helpful votes of the review                                        |


## Getting Started

To use this recommender system on the local machine, follow these basic steps:


### Installation

1. Clone this repository or download the project files on the local machine. 

    ```
    git clone https://github.com/abdullahml42/recommender-system.git
    ```

2. Go to the project directory. 

    ```
    cd recommender-system
    ```

3. Create a Python virtual environment.

    ```
    python -m venv dev
    ```

4. Activate the `dev` virtual environment.

    - On Windows:
        ```
        dev\Scripts\activate.bat
        ```
    - On Linux or MacOS:
        ```
        source dev/bin/activate
        ```

5. Install the dependencies. 

    ```
    pip install -r requirements.txt
    ```


## Running the Application

1. Run the application.

    ```
    python app.py
    ```

2. In the web browser, enter the following URL. 
    
    ```
    localhost:8000/
    ```

3. Trigger the training pipeline to train the model on the Amazon data.

    ```
    localhost:8000/train
    ```

4. Inference for a specific user.

    - Enter a User ID or select one from the suggestions.
    - Enter the number of items for recommendation.
    - Click the `Recommend Products` button, and it will return the top product IDs ordered by their predicted ratings for that user.    


5. Run the Streamlit application.

    ```
    streamlit run streamlit_app.py
    ```


## Acknowledgement

[Data Source: Amazon Review Data (2018)](https://nijianmo.github.io/amazon/index.html)