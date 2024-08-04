"""
This file defines the API routes for the Flask application using the 'apis' Blueprint.
It includes endpoints for calculating the average age of users, summarizing posts, and extracting
keywords from post content.

The routes make use of SQLAlchemy for database queries, the Transformers library for text summarization,
and NLTK for keyword extraction.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from . import db
from .models import User, Post, Comment, Img
from transformers import pipeline
from sqlalchemy.sql import func

# Define the 'apis' Blueprint for API routes
apis = Blueprint("apis", __name__)

@apis.route('/avg-age', methods=['GET'])
def avg_age():
    """
    API endpoint to calculate the average age of users.
    Returns the average age as a JSON response.
    """
    average_ages = User.query.with_entities(func.avg(User.age)).scalar()
    return jsonify({"Avg_age": average_ages})

# Load the summarization pipeline from Transformers
summarizer = pipeline("summarization")

@apis.route('/summarize', methods=['GET'])
def summarize_text():
    """
    API endpoint to summarize the content of all posts.
    Uses a pre-trained summarization model to generate summaries.
    Returns a JSON response with post titles and their corresponding summaries.
    """
    posts = {}
    all_posts = db.session.query(Post.title, Post.content).all()

    for title, post in all_posts:
        summary = summarizer(post, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        posts[title] = summary

    return jsonify(posts)

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

@apis.route('/extract_keywords', methods=['GET'])
def extract_keywords():
    """
    API endpoint to extract keywords from the content of all posts.
    Uses NLTK to tokenize and filter words, and calculates word frequencies.
    Returns a JSON response with post titles and their corresponding keywords.
    """
    posts = db.session.query(Post.title, Post.content).all()
    keywords = {}
    stop_words = set(stopwords.words('english'))

    for title, post in posts:
        word_tokens = word_tokenize(post.lower())
        print(f"Word Tokens: {word_tokens}")  # Debug print
        
        # Filter out stop words and non-alphabetic tokens
        filtered_words = [word for word in word_tokens if word.isalpha() and word not in stop_words]
        print(f"Filtered Words: {filtered_words}")  # Debug print
        
        # Extract keywords using word frequency
        word_freq = Counter(filtered_words)
        print(f"Word Frequency: {word_freq}")  # Debug print
        
        # Return all filtered words as keywords
        keywords[title] = list(word_freq.keys())

    return jsonify(keywords)
