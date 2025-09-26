# Create a complete streaming website structure
import streamlit as st
import pandas as pd
import os
from urllib.parse import urlparse
import json

# Sample movie/series data structure
sample_data = {
    'movies': [
        {
            'id': 1,
            'title': 'Sample Movie 1',
            'genre': 'Action',
            'year': 2023,
            'rating': 8.5,
            'description': 'An exciting action movie with thrilling scenes.',
            'thumbnail': 'https://via.placeholder.com/300x450?text=Movie+1',
            'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
            'duration': '2h 15m'
        },
        {
            'id': 2,
            'title': 'Sample Movie 2', 
            'genre': 'Drama',
            'year': 2022,
            'rating': 7.8,
            'description': 'A compelling drama about human relationships.',
            'thumbnail': 'https://via.placeholder.com/300x450?text=Movie+2',
            'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_640x360_1mb.mp4',
            'duration': '1h 45m'
        }
    ],
    'tv_shows': [
        {
            'id': 101,
            'title': 'Sample Series 1',
            'genre': 'Sci-Fi',
            'year': 2024,
            'rating': 9.1,
            'description': 'A futuristic series exploring space and technology.',
            'thumbnail': 'https://via.placeholder.com/300x450?text=Series+1',
            'seasons': 3,
            'episodes': [
                {
                    'season': 1,
                    'episode': 1,
                    'title': 'Pilot',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4',
                    'duration': '45m'
                }
            ]
        }
    ]
}

# Save sample data to JSON file
with open('content_database.json', 'w') as f:
    json.dump(sample_data, f, indent=2)
    
print("Sample content database created successfully!")
print("Structure includes movies and TV shows with metadata")