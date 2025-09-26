
import streamlit as st
import json
import pandas as pd
from urllib.parse import urlparse

# Set page configuration
st.set_page_config(
    page_title="StreamFlix - Your Movie & TV Hub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .content-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .video-player {
        border-radius: 10px;
        overflow: hidden;
    }
    .sidebar .sidebar-content {
        background-color: #f1f3f4;
    }
</style>
""", unsafe_allow_html=True)

# Load content database
@st.cache_data
def load_content():
    try:
        with open('content_database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Content database not found. Please ensure content_database.json exists.")
        return {'movies': [], 'tv_shows': []}

# Initialize session state
if 'current_content' not in st.session_state:
    st.session_state.current_content = None
if 'content_type' not in st.session_state:
    st.session_state.content_type = 'movies'

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 StreamFlix</h1>
        <p>Your Ultimate Streaming Destination</p>
    </div>
    """, unsafe_allow_html=True)

    # Load content
    content_data = load_content()

    # Sidebar navigation
    st.sidebar.header("🎭 Navigation")
    page = st.sidebar.selectbox("Choose Section", 
                               ["Home", "Movies", "TV Shows", "Search", "Trending"])

    # Filter options
    if page in ["Movies", "TV Shows"]:
        st.sidebar.header("🔍 Filters")
        genres = set()
        if page == "Movies":
            for movie in content_data['movies']:
                genres.add(movie['genre'])
        else:
            for show in content_data['tv_shows']:
                genres.add(show['genre'])

        selected_genre = st.sidebar.selectbox("Genre", ["All"] + sorted(list(genres)))
        year_range = st.sidebar.slider("Year Range", 2020, 2024, (2020, 2024))
        rating_filter = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 0.0)

    # Main content area
    if page == "Home":
        display_home(content_data)
    elif page == "Movies":
        display_movies(content_data, selected_genre, year_range, rating_filter)
    elif page == "TV Shows":
        display_tv_shows(content_data, selected_genre, year_range, rating_filter)
    elif page == "Search":
        display_search(content_data)
    elif page == "Trending":
        display_trending(content_data)

def display_home(content_data):
    st.header("🏠 Welcome to StreamFlix")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎬 Featured Movies")
        if content_data['movies']:
            featured_movie = content_data['movies'][0]
            display_content_card(featured_movie, 'movie')

    with col2:
        st.subheader("📺 Featured TV Shows")
        if content_data['tv_shows']:
            featured_show = content_data['tv_shows'][0]
            display_content_card(featured_show, 'tv_show')

    # Recently added section
    st.subheader("🆕 Recently Added")
    recent_content = content_data['movies'][:3] + content_data['tv_shows'][:2]

    cols = st.columns(min(len(recent_content), 5))
    for idx, content in enumerate(recent_content):
        if idx < len(cols):
            with cols[idx]:
                content_type = 'movie' if content in content_data['movies'] else 'tv_show'
                display_content_thumbnail(content, content_type)

def display_movies(content_data, genre_filter, year_range, rating_filter):
    st.header("🎬 Movies")

    # Filter movies
    filtered_movies = []
    for movie in content_data['movies']:
        if (genre_filter == "All" or movie['genre'] == genre_filter) and            (year_range[0] <= movie['year'] <= year_range[1]) and            (movie['rating'] >= rating_filter):
            filtered_movies.append(movie)

    if not filtered_movies:
        st.warning("No movies match your filters.")
        return

    # Display movies in grid
    cols = st.columns(3)
    for idx, movie in enumerate(filtered_movies):
        with cols[idx % 3]:
            display_content_card(movie, 'movie')

def display_tv_shows(content_data, genre_filter, year_range, rating_filter):
    st.header("📺 TV Shows")

    # Filter TV shows
    filtered_shows = []
    for show in content_data['tv_shows']:
        if (genre_filter == "All" or show['genre'] == genre_filter) and            (year_range[0] <= show['year'] <= year_range[1]) and            (show['rating'] >= rating_filter):
            filtered_shows.append(show)

    if not filtered_shows:
        st.warning("No TV shows match your filters.")
        return

    # Display TV shows in grid
    cols = st.columns(3)
    for idx, show in enumerate(filtered_shows):
        with cols[idx % 3]:
            display_content_card(show, 'tv_show')

def display_search(content_data):
    st.header("🔍 Search Content")

    search_query = st.text_input("Search for movies or TV shows:", placeholder="Enter title, genre, or keyword...")

    if search_query:
        search_results = []

        # Search movies
        for movie in content_data['movies']:
            if (search_query.lower() in movie['title'].lower() or 
                search_query.lower() in movie['genre'].lower() or
                search_query.lower() in movie['description'].lower()):
                search_results.append((movie, 'movie'))

        # Search TV shows
        for show in content_data['tv_shows']:
            if (search_query.lower() in show['title'].lower() or 
                search_query.lower() in show['genre'].lower() or
                search_query.lower() in show['description'].lower()):
                search_results.append((show, 'tv_show'))

        if search_results:
            st.subheader(f"Search Results ({len(search_results)} found)")
            cols = st.columns(3)
            for idx, (content, content_type) in enumerate(search_results):
                with cols[idx % 3]:
                    display_content_card(content, content_type)
        else:
            st.warning("No results found for your search.")

def display_trending(content_data):
    st.header("🔥 Trending Now")

    # Sort by rating for trending
    all_content = [(movie, 'movie') for movie in content_data['movies']] +                   [(show, 'tv_show') for show in content_data['tv_shows']]
    trending_content = sorted(all_content, key=lambda x: x[0]['rating'], reverse=True)

    cols = st.columns(3)
    for idx, (content, content_type) in enumerate(trending_content):
        with cols[idx % 3]:
            display_content_card(content, content_type)

def display_content_card(content, content_type):
    with st.container():
        st.markdown(f"""
        <div class="content-card">
            <h4>{content['title']}</h4>
            <p><strong>Genre:</strong> {content['genre']} | <strong>Year:</strong> {content['year']}</p>
            <p><strong>Rating:</strong> ⭐ {content['rating']}/10</p>
            <p>{content['description'][:100]}...</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"▶️ Watch {content['title']}", key=f"watch_{content['id']}"):
            st.session_state.current_content = content
            st.session_state.content_type = content_type
            st.experimental_rerun()

        # Display video player if this content is selected
        if (st.session_state.current_content and 
            st.session_state.current_content['id'] == content['id']):
            display_video_player(content, content_type)

def display_content_thumbnail(content, content_type):
    st.image(content['thumbnail'], use_column_width=True)
    st.write(f"**{content['title']}**")
    st.write(f"⭐ {content['rating']}")
    if st.button(f"▶️ Watch", key=f"thumb_{content['id']}"):
        st.session_state.current_content = content
        st.session_state.content_type = content_type
        st.experimental_rerun()

def display_video_player(content, content_type):
    st.subheader(f"🎬 Now Playing: {content['title']}")

    # Video player
    try:
        if content_type == 'movie':
            st.video(content['video_url'])
        else:  # TV show
            # For TV shows, display episode selector
            if 'episodes' in content:
                st.subheader("📺 Episodes")
                for episode in content['episodes']:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"Season {episode['season']}, Episode {episode['episode']}: {episode['title']}")
                    with col2:
                        if st.button(f"▶️ Play", key=f"ep_{episode['season']}_{episode['episode']}"):
                            st.video(episode['video_url'])
    except Exception as e:
        st.error(f"Error loading video: {str(e)}")
        st.info("This is a demo. In a real application, you would integrate with actual video hosting services.")

    # Content information
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Genre:** {content['genre']}")
        st.write(f"**Year:** {content['year']}")
        st.write(f"**Rating:** ⭐ {content['rating']}/10")
        if content_type == 'movie':
            st.write(f"**Duration:** {content['duration']}")
        else:
            st.write(f"**Seasons:** {content['seasons']}")

    with col2:
        st.write("**Description:**")
        st.write(content['description'])

if __name__ == "__main__":
    main()
