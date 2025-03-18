from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
from pyspark.sql.functions import col
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import functions as F
# Initialize Spark session
spark = SparkSession.builder \
    .appName("MovieLensDataProcessing") \
    .getOrCreate()


ratings_df = spark.read.csv("data_mk/u.data", sep="\t", inferSchema=True, header=False) \
    .toDF("user_id", "movie_id", "rating", "timestamp")
# Show the first few rows of the data
ratings_df.show()

films_df = spark.read.csv("data_mk/u.item", sep="|", inferSchema=True, header=False) \
    .toDF("movie_id", "title", "release_date", "video_release_date", "IMDb_url", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western")

users_df = spark.read.csv("data_mk/u.user", sep="|", inferSchema=True, header=False) \
    .toDF("user_id", "age", "gender", "occupation", "zip_code")
users_df.toPandas()

# Drop the timestamp column since it's not needed for the collaborative filtering model
ratings_df = ratings_df.drop("timestamp")

ratings_with_movie_titles = ratings_df.join(films_df.select("movie_id", "title"), on="movie_id", how="left")
ratings_with_movie_titles.toPandas()

for genre in genre_columns:
    ratings_with_movie_titles = ratings_with_movie_titles.join(films_df.select("movie_id", genre), 
                                                               on="movie_id", how="left")
    
(training_data, test_data) = ratings_df.randomSplit([0.8, 0.2], seed=1234)
als = ALS(userCol="user_id", itemCol="movie_id", ratingCol="rating", coldStartStrategy="drop")
als_model = als.fit(training_data)
predictions = als_model.transform(test_data)

evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
user_recommendations = als_model.recommendForAllUsers(6)

# Example: Show recommendations for the first user
user_recommendations.show(truncate=False)
als_model.save("maching_learning_model/als_model")
recommendations_list = []

for row in user_recommendations.collect():
    user_id = row['user_id']
    movies = row['recommendations']
    for movie in movies:
        movie_id = movie['movie_id']
        rating = movie['rating']  # Include the rating
        recommendations_list.append({
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating
        })

# Connect to Elasticsearch
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://elasticsearch:9200"])

# Index recommendations into Elasticsearcha
for recommendation in recommendations_list:
    es.index(index="movie_recommendations", document=recommendation)
users_list = users_df.toJSON().collect()

for user_json in users_list:
    es.index(index="users", document=user_json)

ratings_list = []

for row in ratings_with_movie_titles.collect():
    ratings_list.append({
        "user_id": row['user_id'],
        "movie_id": row['movie_id'],
        "title": row['title'],
        "rating": row['rating']
    })

# Index the ratings into Elasticsearch
for rating in ratings_list:
    es.index(index="movie_ratings", document=rating)

spark.stop()