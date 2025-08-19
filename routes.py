# routes.py
from flask import Blueprint, render_template, request, jsonify, redirect, session
from sentiment_analysis import analyze_sentiment_with_gemini
from spotify_integration import get_spotify_client, get_spotify_oauth
from music_therapy import create_emotional_journey_plan, get_stage_for_emotion

main_routes = Blueprint('main', __name__)

# --- Login/Logout routes ---
@main_routes.route('/')
def index():
    sp = get_spotify_client()
    user_profile = None
    if sp:
        try:
            user_profile = sp.current_user()
        except Exception:
            session.clear()
    return render_template('index.html', user_profile=user_profile)

@main_routes.route('/login')
def login():
    auth_url = get_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@main_routes.route('/callback')
def callback():
    token_info = get_spotify_oauth().get_access_token(request.args.get('code'))
    session['spotify_token_info'] = token_info
    return redirect('/')

@main_routes.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# --- Analysis and Journey Creation ---
@main_routes.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyzes sentiment and returns the result + current stage."""
    try:
        data = request.get_json()
        journal_text = data.get('text', '')
        if not journal_text:
            return jsonify({'error': 'No text provided'}), 400

        sentiment = analyze_sentiment_with_gemini(journal_text)
        if isinstance(sentiment, dict) and "error" in sentiment:
            return jsonify(sentiment), 500

        stage_name = get_stage_for_emotion(sentiment)
        return jsonify({'sentiment': sentiment, 'stage': stage_name})
    except Exception as e:
        print(f"A critical error occurred in /analyze_sentiment: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

@main_routes.route('/create_journey', methods=['POST'])
def create_journey_endpoint():
    """
    Creates a full, personalized music therapy journey (3 stages) with playlist URIs.
    """
    sp_client = get_spotify_client()
    if not sp_client:
        return jsonify({'error': 'Spotify login required.'}), 401

    try:
        data = request.get_json()
        sentiment = data.get('sentiment', '')
        if not sentiment:
            return jsonify({'error': 'No sentiment provided'}), 400

        journey_plan = create_emotional_journey_plan(sentiment)
        journey_playlists = []

        for stage in journey_plan:
            playlist_uri = stage.get('playlist_uri')
            if playlist_uri:
                journey_playlists.append({
                    'label': stage['label'],
                    'playlist_uri': playlist_uri
                })
            else:
                return jsonify({'error': f'No playlist URI available for {stage.get("label","this stage")}.'}), 500

        if not journey_playlists:
            return jsonify({'error': 'No playlists available for this journey.'}), 500

        return jsonify({'journey': journey_playlists})
    except Exception as e:
        print(f"A critical error occurred in /create_journey: {e}")
        return jsonify({'error': f'Failed to create music journey: {str(e)}'}), 500

# --- SDK Helper Routes ---
@main_routes.route('/get_token', methods=['GET'])
def get_token():
    """Provides the access token to the frontend SDK."""
    token_info = session.get('spotify_token_info', None)
    if not token_info:
        return jsonify({'error': 'User not logged in'}), 401
    return jsonify({'access_token': token_info.get('access_token')})

@main_routes.route('/play', methods=['POST'])
def play_song():
    """
    Plays a specific playlist on a specific device.
    Important: transfer playback to the Web SDK device to avoid 5s cutoffs.
    """
    sp_client = get_spotify_client()
    if not sp_client:
        return jsonify({'error': 'Spotify login required.'}), 401

    try:
        data = request.get_json()
        playlist_uri = data.get('playlist_uri')
        device_id = data.get('device_id')

        if not playlist_uri or not device_id:
            return jsonify({'error': 'Playlist URI and Device ID are required.'}), 400

        # 1) Transfer playback to the Web Playback SDK device
        sp_client.transfer_playback(device_id=device_id, force_play=True)

        # 2) Start playback using playlist context on that same device
        sp_client.start_playback(device_id=device_id, context_uri=playlist_uri)

        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"A critical error occurred in /play: {e}")
        return jsonify({'error': f'Could not start playback: {str(e)}'}), 500
