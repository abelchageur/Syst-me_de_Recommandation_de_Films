from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch, ConnectionError, NotFoundError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Elasticsearch client using environment variables
es_host = os.getenv("ELASTICSEARCH_HOST")
es = Elasticsearch(hosts=[es_host])

@app.route('/')
def hello():
    return "Movie Recommendation API is running!"

@app.route('/recommendations/<int:movie_id>', methods=['GET'])
def get_recommendations(movie_id):
    """
    Endpoint to fetch movie recommendations based on movie_id.
    """
    try:
        # Get movie recommendations directly
        recommendations = get_movie_recommendations(movie_id)
        
        if not recommendations:
            return jsonify({"error": "No recommendations found for the given movie ID"}), 404
        
        return jsonify({
            "movie_id": movie_id,
            "recommendations": recommendations
        })
    
    except ConnectionError:
        return jsonify({"error": "Unable to connect to Elasticsearch"}), 500
    except NotFoundError:
        return jsonify({"error": "Elasticsearch index not found"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def get_movie_recommendations(movie_id):
    """
    Get movie recommendations based on movie_id.
    """
    # Define Elasticsearch query
    query = {
        "query": {
            "match": {"movie_id": movie_id}
        }
    }

    # Fetch data from Elasticsearch
    es_index = os.getenv("ELASTICSEARCH_INDEX_MOVIE_RECOMMENDATIONS")
    response = es.search(index=es_index, body=query)
    
    # Extract recommendations from Elasticsearch response
    if response['hits']['total']['value'] > 0:
        recommendations = [{
            "user_id": hit["_source"]["user_id"],
            "recommended_movie_id": hit["_source"]["movie_id"],  # Use movie_id instead
            "rating": hit["_source"].get("rating")
        } for hit in response['hits']['hits']]
        return recommendations
    else:
        return []

if __name__ == '__main__':
    # Run Flask app with configurations from .env
    flask_host = os.getenv("FLASK_HOST")
    flask_port = int(os.getenv("FLASK_PORT"))
    app.run(host=flask_host, port=flask_port)