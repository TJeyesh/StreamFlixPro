
import streamlit as st
import json
import pandas as pd
from datetime import datetime
import requests
from urllib.parse import urlparse

# Set page configuration
st.set_page_config(
    page_title="StreamFlix Pro - Advanced Streaming Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .content-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .content-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }

    .video-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin: 2rem 0;
    }

    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }

    .genre-tag {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }

    .rating-badge {
        background: linear-gradient(45deg, #ffecd2, #fcb69f);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        color: #333;
        display: inline-block;
        margin: 0.5rem 0;
    }

    .feature-highlight {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }

    .play-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .play-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced content database with more features
@st.cache_data
def load_content():
    try:
        with open('content_database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create sample data if file doesn't exist
        sample_data = {
            'movies': [
                {
                    'id': 1,
                    'title': 'Cyber Revolution',
                    'genre': 'Sci-Fi',
                    'year': 2024,
                    'rating': 9.2,
                    'description': 'In a world dominated by AI, a group of rebels fights to preserve human consciousness.',
                    'thumbnail': 'https://via.placeholder.com/300x450/667eea/white?text=Cyber+Revolution',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
                    'duration': '2h 15m',
                    'director': 'Alex Chen',
                    'cast': ['Emma Stone', 'Ryan Gosling', 'Oscar Isaac'],
                    'languages': ['English', 'Spanish'],
                    'quality': ['HD', '4K'],
                    'views': 1250000,
                    'likes': 89750,
                    'release_date': '2024-03-15'
                },
                {
                    'id': 2,
                    'title': 'Ocean Depths',
                    'genre': 'Adventure',
                    'year': 2023,
                    'rating': 8.7,
                    'description': 'A deep-sea exploration team discovers an ancient underwater civilization.',
                    'thumbnail': 'https://via.placeholder.com/300x450/764ba2/white?text=Ocean+Depths',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_640x360_1mb.mp4',
                    'duration': '1h 58m',
                    'director': 'Maria Rodriguez',
                    'cast': ['Chris Pratt', 'Zoe Saldana', 'Michael Shannon'],
                    'languages': ['English', 'French'],
                    'quality': ['HD', '4K'],
                    'views': 980000,
                    'likes': 72400,
                    'release_date': '2023-08-22'
                },
                {
                    'id': 3,
                    'title': 'Mind Games',
                    'genre': 'Thriller',
                    'year': 2024,
                    'rating': 8.9,
                    'description': 'A psychological thriller about memory manipulation and identity crisis.',
                    'thumbnail': 'https://via.placeholder.com/300x450/f093fb/white?text=Mind+Games',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_720x480_1mb.mp4',
                    'duration': '2h 5m',
                    'director': 'Christopher Nolan',
                    'cast': ['Leonardo DiCaprio', 'Marion Cotillard', 'Tom Hardy'],
                    'languages': ['English'],
                    'quality': ['HD', '4K', '8K'],
                    'views': 2100000,
                    'likes': 156000,
                    'release_date': '2024-01-10'
                }
            ],
            'tv_shows': [
                {
                    'id': 101,
                    'title': 'Galaxy Guardians',
                    'genre': 'Sci-Fi',
                    'year': 2024,
                    'rating': 9.5,
                    'description': 'An elite space force protects the galaxy from interdimensional threats.',
                    'thumbnail': 'https://via.placeholder.com/300x450/667eea/white?text=Galaxy+Guardians',
                    'seasons': 3,
                    'total_episodes': 36,
                    'status': 'Ongoing',
                    'creator': 'J.J. Abrams',
                    'cast': ['John Boyega', 'Daisy Ridley', 'Adam Driver'],
                    'languages': ['English', 'Spanish', 'Mandarin'],
                    'quality': ['HD', '4K'],
                    'views': 5500000,
                    'likes': 425000,
                    'episodes': [
                        {
                            'season': 1,
                            'episode': 1,
                            'title': 'First Contact',
                            'description': 'The team encounters their first interdimensional threat.',
                            'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4',
                            'duration': '45m',
                            'air_date': '2024-01-15'
                        },
                        {
                            'season': 1,
                            'episode': 2,
                            'title': 'The Anomaly',
                            'description': 'Strange readings lead the team to a mysterious space anomaly.',
                            'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
                            'duration': '44m',
                            'air_date': '2024-01-22'
                        }
                    ]
                },
                {
                    'id': 102,
                    'title': 'Corporate Shadows',
                    'genre': 'Drama',
                    'year': 2023,
                    'rating': 8.8,
                    'description': 'Behind-the-scenes drama at a powerful multinational corporation.',
                    'thumbnail': 'https://via.placeholder.com/300x450/764ba2/white?text=Corporate+Shadows',
                    'seasons': 2,
                    'total_episodes': 20,
                    'status': 'Completed',
                    'creator': 'Vince Gilligan',
                    'cast': ['Bryan Cranston', 'Aaron Paul', 'Anna Gunn'],
                    'languages': ['English'],
                    'quality': ['HD', '4K'],
                    'views': 3200000,
                    'likes': 289000,
                    'episodes': [
                        {
                            'season': 1,
                            'episode': 1,
                            'title': 'The Deal',
                            'description': 'A major corporate acquisition sets the stage for conflict.',
                            'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
                            'duration': '42m',
                            'air_date': '2023-05-10'
                        }
                    ]
                }
            ]
        }

        # Save to file for future use
        with open('content_database.json', 'w') as f:
            json.dump(sample_data, f, indent=2)

        return sample_data

# Initialize session state
if 'current_content' not in st.session_state:
    st.session_state.current_content = None
if 'content_type' not in st.session_state:
    st.session_state.content_type = 'movies'
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'viewing_history' not in st.session_state:
    st.session_state.viewing_history = []

def main():
    # Enhanced header with stats
    content_data = load_content()
    total_movies = len(content_data['movies'])
    total_shows = len(content_data['tv_shows'])
    total_episodes = sum(show.get('total_episodes', 0) for show in content_data['tv_shows'])

    st.markdown(f"""
    <div class="main-header">
        <h1>🎬 StreamFlix Pro</h1>
        <p>Premium Streaming Experience</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
            <div><strong>{total_movies}</strong><br>Movies</div>
            <div><strong>{total_shows}</strong><br>TV Shows</div>
            <div><strong>{total_episodes}</strong><br>Episodes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced sidebar navigation
    st.sidebar.header("🎭 Navigation")
    page = st.sidebar.selectbox("Choose Section", 
                               ["🏠 Home", "🎬 Movies", "📺 TV Shows", "🔍 Search", 
                                "🔥 Trending", "❤️ Watchlist", "📊 Analytics"])

    # User preferences
    st.sidebar.header("⚙️ Preferences")
    quality_pref = st.sidebar.selectbox("Preferred Quality", ["HD", "4K", "8K"])
    language_pref = st.sidebar.selectbox("Language", ["English", "Spanish", "French", "Mandarin"])
    autoplay = st.sidebar.checkbox("Autoplay", value=True)

    # Advanced filters for content pages
    if page in ["🎬 Movies", "📺 TV Shows"]:
        st.sidebar.header("🔍 Advanced Filters")
        content_list = content_data['movies'] if page == "🎬 Movies" else content_data['tv_shows']

        # Genre filter
        genres = sorted(set(content['genre'] for content in content_list))
        selected_genre = st.sidebar.selectbox("Genre", ["All"] + genres)

        # Year filter
        years = sorted(set(content['year'] for content in content_list))
        year_range = st.sidebar.slider("Year Range", 
                                     min(years) if years else 2020, 
                                     max(years) if years else 2024, 
                                     (min(years) if years else 2020, max(years) if years else 2024))

        # Rating filter
        rating_filter = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.1)

        # Sort options
        sort_by = st.sidebar.selectbox("Sort By", ["Rating", "Year", "Views", "Title"])
        sort_order = st.sidebar.radio("Order", ["Descending", "Ascending"])
    else:
        selected_genre = "All"
        year_range = (2020, 2024)
        rating_filter = 0.0
        sort_by = "Rating"
        sort_order = "Descending"

    # Route to appropriate page
    if page == "🏠 Home":
        display_home(content_data)
    elif page == "🎬 Movies":
        display_movies(content_data, selected_genre, year_range, rating_filter, sort_by, sort_order)
    elif page == "📺 TV Shows":
        display_tv_shows(content_data, selected_genre, year_range, rating_filter, sort_by, sort_order)
    elif page == "🔍 Search":
        display_search(content_data)
    elif page == "🔥 Trending":
        display_trending(content_data)
    elif page == "❤️ Watchlist":
        display_watchlist(content_data)
    elif page == "📊 Analytics":
        display_analytics(content_data)

def display_home(content_data):
    st.header("🏠 Welcome to StreamFlix Pro")

    # Hero section with featured content
    col1, col2 = st.columns([2, 1])

    with col1:
        if content_data['movies']:
            featured = max(content_data['movies'], key=lambda x: x['rating'])
            st.markdown(f"""
            <div class="feature-highlight">
                <h3>🌟 Featured: {featured['title']}</h3>
                <p><strong>Genre:</strong> {featured['genre']} | <strong>Rating:</strong> ⭐ {featured['rating']}/10</p>
                <p>{featured['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("▶️ Watch Featured Movie", key="featured_movie"):
                st.session_state.current_content = featured
                st.session_state.content_type = 'movie'
                st.experimental_rerun()

    with col2:
        st.markdown("""
        <div class="stats-container">
            <h4>🎯 Quick Stats</h4>
            <p>Total Views: 12.5M+</p>
            <p>Active Users: 250K+</p>
            <p>Content Hours: 10K+</p>
        </div>
        """, unsafe_allow_html=True)

    # Continue watching section
    if st.session_state.viewing_history:
        st.subheader("⏯️ Continue Watching")
        for item in st.session_state.viewing_history[-3:]:
            st.write(f"📺 {item['title']} - {item['genre']}")

    # Categories showcase
    st.subheader("🎭 Browse by Category")

    # Get content by genre
    all_content = content_data['movies'] + content_data['tv_shows']
    genres = {}
    for content in all_content:
        genre = content['genre']
        if genre not in genres:
            genres[genre] = []
        genres[genre].append(content)

    for genre, content_list in genres.items():
        with st.expander(f"{genre} ({len(content_list)} items)"):
            cols = st.columns(min(len(content_list), 4))
            for idx, content in enumerate(content_list[:4]):
                if idx < len(cols):
                    with cols[idx]:
                        content_type = 'movie' if content in content_data['movies'] else 'tv_show'
                        display_content_thumbnail(content, content_type)

def display_movies(content_data, genre_filter, year_range, rating_filter, sort_by, sort_order):
    st.header("🎬 Movies Collection")

    # Apply filters
    filtered_movies = filter_content(content_data['movies'], genre_filter, year_range, rating_filter)

    # Apply sorting
    filtered_movies = sort_content(filtered_movies, sort_by, sort_order)

    if not filtered_movies:
        st.warning("No movies match your current filters.")
        return

    st.info(f"Showing {len(filtered_movies)} movies")

    # Display movies in responsive grid
    cols = st.columns(3)
    for idx, movie in enumerate(filtered_movies):
        with cols[idx % 3]:
            display_enhanced_content_card(movie, 'movie')

def display_tv_shows(content_data, genre_filter, year_range, rating_filter, sort_by, sort_order):
    st.header("📺 TV Shows Collection")

    # Apply filters
    filtered_shows = filter_content(content_data['tv_shows'], genre_filter, year_range, rating_filter)

    # Apply sorting
    filtered_shows = sort_content(filtered_shows, sort_by, sort_order)

    if not filtered_shows:
        st.warning("No TV shows match your current filters.")
        return

    st.info(f"Showing {len(filtered_shows)} TV shows")

    # Display TV shows in responsive grid
    cols = st.columns(3)
    for idx, show in enumerate(filtered_shows):
        with cols[idx % 3]:
            display_enhanced_content_card(show, 'tv_show')

def display_search(content_data):
    st.header("🔍 Advanced Search")

    col1, col2 = st.columns([2, 1])

    with col1:
        search_query = st.text_input("Search for content:", 
                                   placeholder="Enter title, actor, director, or keyword...")

    with col2:
        search_type = st.selectbox("Search in:", ["All", "Movies", "TV Shows"])

    if search_query:
        search_results = perform_advanced_search(content_data, search_query, search_type)

        if search_results:
            st.subheader(f"🎯 Search Results ({len(search_results)} found)")

            # Display results with highlighting
            for content, content_type, match_score in search_results:
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        st.image(content['thumbnail'], width=150)

                    with col2:
                        st.write(f"**{content['title']}** ({content['year']})")
                        st.write(f"Genre: {content['genre']} | Rating: ⭐ {content['rating']}/10")
                        st.write(f"Match Score: {match_score:.1%}")
                        st.write(content['description'][:100] + "...")

                    with col3:
                        if st.button(f"▶️ Watch", key=f"search_{content['id']}"):
                            st.session_state.current_content = content
                            st.session_state.content_type = content_type
                            add_to_viewing_history(content)
                            st.experimental_rerun()
        else:
            st.warning("No results found. Try different keywords.")

def display_trending(content_data):
    st.header("🔥 Trending Content")

    # Combine and sort by views and rating
    all_content = []
    for movie in content_data['movies']:
        movie_copy = movie.copy()
        movie_copy['content_type'] = 'movie'
        movie_copy['trend_score'] = movie['views'] * movie['rating'] / 1000
        all_content.append(movie_copy)

    for show in content_data['tv_shows']:
        show_copy = show.copy()
        show_copy['content_type'] = 'tv_show'
        show_copy['trend_score'] = show['views'] * show['rating'] / 1000
        all_content.append(show_copy)

    trending_content = sorted(all_content, key=lambda x: x['trend_score'], reverse=True)

    # Display trending chart
    st.subheader("📈 Trending Chart")
    chart_data = pd.DataFrame([
        {'Title': content['title'][:15], 'Views': content['views'], 'Rating': content['rating']}
        for content in trending_content[:10]
    ])

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(chart_data.set_index('Title')['Views'])
    with col2:
        st.bar_chart(chart_data.set_index('Title')['Rating'])

    # Display trending content cards
    st.subheader("🎬 Trending Now")
    cols = st.columns(3)
    for idx, content in enumerate(trending_content):
        with cols[idx % 3]:
            display_trending_card(content, content['content_type'])

def display_watchlist(content_data):
    st.header("❤️ My Watchlist")

    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add some content to get started!")
        return

    st.success(f"You have {len(st.session_state.watchlist)} items in your watchlist")

    # Find full content details
    watchlist_content = []
    for item_id, content_type in st.session_state.watchlist:
        content_list = content_data['movies'] if content_type == 'movie' else content_data['tv_shows']
        content = next((c for c in content_list if c['id'] == item_id), None)
        if content:
            watchlist_content.append((content, content_type))

    # Display watchlist items
    for content, content_type in watchlist_content:
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.image(content['thumbnail'], width=100)

        with col2:
            st.write(f"**{content['title']}** ({content['year']})")
            st.write(f"{content['genre']} | ⭐ {content['rating']}/10")
            st.write(content['description'][:100] + "...")

        with col3:
            if st.button(f"▶️ Watch", key=f"watchlist_{content['id']}"):
                st.session_state.current_content = content
                st.session_state.content_type = content_type
                st.experimental_rerun()

            if st.button(f"❌ Remove", key=f"remove_{content['id']}"):
                st.session_state.watchlist.remove((content['id'], content_type))
                st.experimental_rerun()

def display_analytics(content_data):
    st.header("📊 Platform Analytics")

    # Content statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_movies = len(content_data['movies'])
        st.metric("Movies", total_movies, delta=None)

    with col2:
        total_shows = len(content_data['tv_shows'])
        st.metric("TV Shows", total_shows, delta=None)

    with col3:
        total_episodes = sum(show.get('total_episodes', 0) for show in content_data['tv_shows'])
        st.metric("Episodes", total_episodes, delta=None)

    with col4:
        avg_rating = sum(c['rating'] for c in content_data['movies'] + content_data['tv_shows']) /                     len(content_data['movies'] + content_data['tv_shows'])
        st.metric("Avg Rating", f"{avg_rating:.1f}/10", delta=None)

    # Genre distribution
    st.subheader("🎭 Genre Distribution")
    genre_counts = {}
    for content in content_data['movies'] + content_data['tv_shows']:
        genre = content['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
    st.bar_chart(genre_df.set_index('Genre'))

    # Rating distribution
    st.subheader("⭐ Rating Distribution")
    ratings = [content['rating'] for content in content_data['movies'] + content_data['tv_shows']]
    rating_df = pd.DataFrame({'Rating': ratings})
    st.histogram(rating_df['Rating'], bins=20)

    # Top content
    st.subheader("🏆 Top Rated Content")
    all_content = content_data['movies'] + content_data['tv_shows']
    top_content = sorted(all_content, key=lambda x: x['rating'], reverse=True)[:10]

    for idx, content in enumerate(top_content, 1):
        st.write(f"{idx}. **{content['title']}** - ⭐ {content['rating']}/10 ({content['genre']})")

# Helper functions
def filter_content(content_list, genre_filter, year_range, rating_filter):
    filtered = []
    for content in content_list:
        if (genre_filter == "All" or content['genre'] == genre_filter) and            (year_range[0] <= content['year'] <= year_range[1]) and            (content['rating'] >= rating_filter):
            filtered.append(content)
    return filtered

def sort_content(content_list, sort_by, sort_order):
    reverse = sort_order == "Descending"

    if sort_by == "Rating":
        return sorted(content_list, key=lambda x: x['rating'], reverse=reverse)
    elif sort_by == "Year":
        return sorted(content_list, key=lambda x: x['year'], reverse=reverse)
    elif sort_by == "Views":
        return sorted(content_list, key=lambda x: x.get('views', 0), reverse=reverse)
    elif sort_by == "Title":
        return sorted(content_list, key=lambda x: x['title'], reverse=not reverse)

    return content_list

def perform_advanced_search(content_data, query, search_type):
    results = []
    query_lower = query.lower()

    content_lists = []
    if search_type in ["All", "Movies"]:
        content_lists.extend([(movie, 'movie') for movie in content_data['movies']])
    if search_type in ["All", "TV Shows"]:
        content_lists.extend([(show, 'tv_show') for show in content_data['tv_shows']])

    for content, content_type in content_lists:
        match_score = 0

        # Title match (highest weight)
        if query_lower in content['title'].lower():
            match_score += 0.4

        # Description match
        if query_lower in content['description'].lower():
            match_score += 0.2

        # Genre match
        if query_lower in content['genre'].lower():
            match_score += 0.2

        # Cast match (if available)
        if 'cast' in content:
            for actor in content['cast']:
                if query_lower in actor.lower():
                    match_score += 0.15
                    break

        # Director match (if available)
        if 'director' in content and query_lower in content['director'].lower():
            match_score += 0.1

        if match_score > 0:
            results.append((content, content_type, match_score))

    # Sort by match score
    return sorted(results, key=lambda x: x[2], reverse=True)

def display_enhanced_content_card(content, content_type):
    st.markdown(f"""
    <div class="content-card">
        <h4>{content['title']}</h4>
        <div class="genre-tag">{content['genre']}</div>
        <div class="rating-badge">⭐ {content['rating']}/10</div>
        <p><strong>Year:</strong> {content['year']} | <strong>Views:</strong> {content.get('views', 'N/A'):,}</p>
        <p>{content['description'][:120]}...</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"▶️ Watch", key=f"watch_{content['id']}"):
            st.session_state.current_content = content
            st.session_state.content_type = content_type
            add_to_viewing_history(content)
            st.experimental_rerun()

    with col2:
        watchlist_key = (content['id'], content_type)
        if watchlist_key not in st.session_state.watchlist:
            if st.button(f"❤️ Add", key=f"add_{content['id']}"):
                st.session_state.watchlist.append(watchlist_key)
                st.success("Added to watchlist!")
                st.experimental_rerun()
        else:
            if st.button(f"💔 Remove", key=f"rem_{content['id']}"):
                st.session_state.watchlist.remove(watchlist_key)
                st.success("Removed from watchlist!")
                st.experimental_rerun()

    with col3:
        if st.button(f"ℹ️ Info", key=f"info_{content['id']}"):
            display_content_details(content, content_type)

def display_content_thumbnail(content, content_type):
    st.image(content['thumbnail'], use_column_width=True)
    st.write(f"**{content['title']}**")
    st.write(f"⭐ {content['rating']} | {content['year']}")

    if st.button(f"▶️ Watch", key=f"thumb_{content['id']}"):
        st.session_state.current_content = content
        st.session_state.content_type = content_type
        add_to_viewing_history(content)
        st.experimental_rerun()

def display_trending_card(content, content_type):
    st.markdown(f"""
    <div class="content-card">
        <h4>🔥 {content['title']}</h4>
        <p><strong>Trend Score:</strong> {content['trend_score']:.0f}</p>
        <p><strong>Views:</strong> {content['views']:,} | <strong>Rating:</strong> ⭐ {content['rating']}/10</p>
        <p>{content['description'][:100]}...</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"▶️ Watch Now", key=f"trend_{content['id']}"):
        st.session_state.current_content = content
        st.session_state.content_type = content_type
        add_to_viewing_history(content)
        st.experimental_rerun()

def display_content_details(content, content_type):
    st.subheader(f"ℹ️ {content['title']} - Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Genre:** {content['genre']}")
        st.write(f"**Year:** {content['year']}")
        st.write(f"**Rating:** ⭐ {content['rating']}/10")
        st.write(f"**Views:** {content.get('views', 'N/A'):,}")

        if content_type == 'movie':
            st.write(f"**Duration:** {content.get('duration', 'N/A')}")
            st.write(f"**Director:** {content.get('director', 'N/A')}")
        else:
            st.write(f"**Seasons:** {content.get('seasons', 'N/A')}")
            st.write(f"**Episodes:** {content.get('total_episodes', 'N/A')}")
            st.write(f"**Status:** {content.get('status', 'N/A')}")

    with col2:
        if 'cast' in content:
            st.write("**Cast:**")
            for actor in content['cast']:
                st.write(f"• {actor}")

        if 'languages' in content:
            st.write("**Languages:**")
            st.write(", ".join(content['languages']))

        if 'quality' in content:
            st.write("**Available Quality:**")
            st.write(", ".join(content['quality']))

    st.write("**Description:**")
    st.write(content['description'])

def add_to_viewing_history(content):
    history_item = {
        'id': content['id'],
        'title': content['title'],
        'genre': content['genre'],
        'timestamp': datetime.now().isoformat()
    }

    # Remove if already exists and add to beginning
    st.session_state.viewing_history = [h for h in st.session_state.viewing_history if h['id'] != content['id']]
    st.session_state.viewing_history.insert(0, history_item)

    # Keep only last 10 items
    st.session_state.viewing_history = st.session_state.viewing_history[:10]

# Video player integration
def display_video_player(content, content_type):
    st.markdown(f"""
    <div class="video-container">
        <h3>🎬 Now Playing: {content['title']}</h3>
    </div>
    """, unsafe_allow_html=True)

    try:
        if content_type == 'movie':
            st.video(content['video_url'], start_time=0)
        else:  # TV show
            if 'episodes' in content:
                st.subheader("📺 Episode Selection")

                # Create episode selector
                episodes = content['episodes']
                episode_options = [f"S{ep['season']}E{ep['episode']}: {ep['title']}" for ep in episodes]
                selected_episode_idx = st.selectbox("Choose Episode:", range(len(episode_options)), 
                                                   format_func=lambda x: episode_options[x])

                selected_episode = episodes[selected_episode_idx]

                # Display episode info
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{selected_episode['title']}**")
                    st.write(selected_episode.get('description', 'No description available.'))
                with col2:
                    st.write(f"**Duration:** {selected_episode['duration']}")
                    if 'air_date' in selected_episode:
                        st.write(f"**Air Date:** {selected_episode['air_date']}")

                # Play episode
                st.video(selected_episode['video_url'], start_time=0)
            else:
                st.warning("No episodes available for this show.")

    except Exception as e:
        st.error(f"Error loading video: {str(e)}")
        st.info("This is a demo application. In production, you would integrate with actual video hosting services like AWS S3, Cloudflare Stream, or similar platforms.")

    # Content information panel
    display_content_info_panel(content, content_type)

def display_content_info_panel(content, content_type):
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📋 Details")
        st.write(f"**Genre:** {content['genre']}")
        st.write(f"**Year:** {content['year']}")
        st.write(f"**Rating:** ⭐ {content['rating']}/10")

        if content_type == 'movie':
            st.write(f"**Duration:** {content.get('duration', 'N/A')}")
        else:
            st.write(f"**Seasons:** {content.get('seasons', 'N/A')}")

    with col2:
        st.subheader("🎭 Cast & Crew")
        if 'director' in content:
            st.write(f"**Director:** {content['director']}")
        if 'cast' in content:
            st.write("**Starring:**")
            for actor in content['cast'][:3]:
                st.write(f"• {actor}")

    with col3:
        st.subheader("🌐 Availability")
        if 'languages' in content:
            st.write("**Languages:**")
            for lang in content['languages']:
                st.write(f"• {lang}")

        if 'quality' in content:
            st.write("**Quality:**")
            for quality in content['quality']:
                st.write(f"• {quality}")

# Check if content should be played
if st.session_state.current_content:
    st.markdown("---")
    display_video_player(st.session_state.current_content, st.session_state.content_type)

if __name__ == "__main__":
    main()
