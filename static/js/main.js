// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const journalInterface = document.getElementById('journal-interface');
    if (!journalInterface) return;

    // --- Element Selectors ---
    const journalText = document.getElementById('journal-entry');
    const resultsContainer = document.getElementById('results-container');
    const sentimentResult = document.getElementById('sentiment-result');
    const stageResult = document.getElementById('stage-result');
    const musicContainer = document.getElementById('music-container');
    const tracksContainer = document.getElementById('tracks-container');
    const errorMessage = document.getElementById('error-message');

    // --- State Management ---
    let spotifyPlayer = null;
    let deviceId = null;
    let lastAnalyzedText = '';
    let currentSentiment = null;
    let isAnalyzing = false;

    // --- Spotify Player Initialization ---
    window.onSpotifyWebPlaybackSDKReady = () => {
        console.log("Spotify SDK is ready.");
        fetch('/get_token')
            .then(response => response.json())
            .then(data => {
                if (data.access_token) {
                    spotifyPlayer = new Spotify.Player({
                        name: 'Sentiment Journal Web Player',
                        getOAuthToken: cb => { cb(data.access_token); }
                    });
                    spotifyPlayer.addListener('ready', ({ device_id }) => {
                        console.log('Spotify Player is ready with Device ID', device_id);
                        deviceId = device_id;
                    });
                    spotifyPlayer.addListener('account_error', ({ message }) => { 
                        console.error('Account Error:', message); 
                        alert("An error occurred with your Spotify account. The Web Player requires a Spotify Premium subscription.");
                    });
                    spotifyPlayer.connect();
                }
            });
    };

    // --- "Sensing" Loop (10 seconds) ---
    setInterval(async () => {
        const currentText = journalText.value.trim();
        if (currentText && currentText !== lastAnalyzedText && !isAnalyzing) {
            await analyzeAndReact(currentText);
        }
    }, 60000);

    async function analyzeAndReact(textToAnalyze) {
        isAnalyzing = true;
        lastAnalyzedText = textToAnalyze;
        
        try {
            const sentimentResponse = await fetch('/analyze_sentiment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: textToAnalyze }),
            });
            const sentimentData = await sentimentResponse.json();
            if (!sentimentResponse.ok) throw new Error(sentimentData.error || 'Analysis failed.');

            const newSentiment = sentimentData.sentiment;
            displayResults(newSentiment, sentimentData.stage);
            
            if (newSentiment !== currentSentiment) {
                currentSentiment = newSentiment;
                await fetchAndPlayNewJourney(currentSentiment);
            }
        } catch (error) {
            displayError(error.message);
        } finally {
            isAnalyzing = false;
        }
    }

    async function fetchAndPlayNewJourney(sentiment) {
        if (!deviceId) {
            displayError("Spotify player is not ready yet. Please wait a moment.");
            return;
        }
        try {
            const journeyResponse = await fetch('/create_journey', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sentiment: sentiment }),
            });
            const journeyData = await journeyResponse.json();
            if (!journeyResponse.ok) throw new Error(journeyData.error || 'Failed to create journey.');
            
            const firstStage = journeyData.journey[0];
            if (!firstStage || !firstStage.playlist_uri) throw new Error("No playlist found in the journey.");

            await playPlaylistOnDevice(firstStage.playlist_uri);
            displayNowPlaying({ name: firstStage.label, artist: 'Various Artists', uri: firstStage.playlist_uri, album_art: 'https://placehold.co/64x64/png?text=Playlist' });
        } catch (error) {
            displayError(error.message);
        }
    }
    
    async function playPlaylistOnDevice(playlistUri) {
        await fetch('/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                playlist_uri: playlistUri,
                device_id: deviceId
            }),
        });
    }

    // --- UI Helper Functions ---
    function displayResults(sentiment, stage) {
        resultsContainer.classList.remove('hidden');
        sentimentResult.textContent = formatSentiment(sentiment);
        sentimentResult.className = getSentimentColorClass(sentiment.split('-')[0]);
        stageResult.textContent = stage;
        stageResult.className = "font-bold";
    }

    function displayNowPlaying(playlist) {
        musicContainer.classList.remove('hidden');
        tracksContainer.innerHTML = createTrackHtml(playlist);
    }

    function formatSentiment(s) { return `${s.split('-')[1]} ${s.split('-')[0]}`; }
    function createTrackHtml(p) { 
        return `<div class="flex items-center p-3 bg-white rounded-lg shadow-sm"><img src="${p.album_art}" alt="${p.name}" class="w-14 h-14 rounded-md mr-4 object-cover"><div class="flex-grow min-w-0"><p class="font-semibold text-gray-900 truncate">${p.name}</p><p class="text-sm text-gray-500 truncate">${p.artist}</p></div></div>`;
    }
    function displayError(m) { 
        errorMessage.innerHTML = `<p class="text-red-600 bg-red-100 p-4 rounded-lg font-medium">${m}</p>`; 
        errorMessage.classList.remove('hidden'); 
    }
    function getSentimentColorClass(e) { 
        const base = 'font-bold';
        switch (e.toLowerCase()) {
            case 'joy': case 'hopeful': case 'love': case 'surprise': return `text-green-600 ${base}`;
            case 'sadness': case 'anxious': case 'fear': return `text-blue-600 ${base}`;
            case 'anger': return `text-red-600 ${base}`;
            case 'calm': return `text-purple-600 ${base}`;
            case 'distress': return `text-orange-600 ${base}`;
            default: return `text-gray-600 ${base}`;
        }
    }
}); // 