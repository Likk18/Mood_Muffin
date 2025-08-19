# music_therapy.py
import random

def get_stage_for_emotion(emotion_analysis):
    """
    The "GPS Navigator": Determines the CURRENT stage name based on emotion and intensity.
    """
    emotion, intensity = emotion_analysis.split('-')

    stage_index = 0  # Default to stage 1 for Low intensity
    if intensity == 'Medium':
        stage_index = 1  # Stage 2
    elif intensity == 'High':
        stage_index = 2  # Stage 3

    journeys = {
        'Sadness': ['Acknowledge & Validate', 'Process & Reflect', 'Empower & Uplift'],
        'Anger': ['Match the Intensity', 'Channel & Process', 'Cool Down & Calm'],
        'Distress': ['Safe Space', 'Gentle Reflection', 'Finding Hope'],
        'Joy': ['Embrace the Joy', 'Amplify the Feeling', 'Sustained Happiness'],
        'Default': ['Acknowledgment', 'Reflection', 'Empowerment']
    }
    
    stage_names = journeys.get(emotion, journeys['Default'])
    
    if stage_index >= len(stage_names):
        stage_index = len(stage_names) - 1
        
    return stage_names[stage_index]


def create_emotional_journey_plan(emotion_analysis):
    """
    Creates the FULL three-stage plan with randomized playlist URIs for each stage.
    """
    emotion, _ = emotion_analysis.split('-')  # We only need the emotion type

    # Each stage now has multiple playlist options. We'll pick one randomly.
    journeys = {
        'Sadness': [
            {'label': 'Acknowledge & Validate', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX7qK8ma5wgG1',  # Sad Bops
                'spotify:playlist:37i9dQZF1DWZUAeYvs88zc',  # Sad Hindi
                'spotify:playlist:37i9dQZF1DX3YSRoSdA634',  # Indie Chill
                'spotify:playlist:37i9dQZF1DXbvABJXBIyiY',  # Emotional Ballads
                'spotify:playlist:37i9dQZF1DWVV27DiNWxkR'   # Chill Sad Vibes
            ]},
            {'label': 'Process & Reflect', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
                'spotify:playlist:37i9dQZF1DWXJfnUiYjUKT',
                'spotify:playlist:37i9dQZF1DX2sUQwD7tbmL',
                'spotify:playlist:37i9dQZF1DWSlw12ofHcMM',
                'spotify:playlist:37i9dQZF1DWVDC7a6aol5C'
            ]},
            {'label': 'Empower & Uplift', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
                'spotify:playlist:37i9dQZF1DXdxcBWuJkbcy',
                'spotify:playlist:37i9dQZF1DX2sUQwD7tbmL',
                'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
                'spotify:playlist:37i9dQZF1DWWeNOD4fJ8j4'
            ]}
        ],
        'Anger': [
            {'label': 'Match the Intensity', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M',
                'spotify:playlist:37i9dQZF1DWZJhOVGWqUKF',
                'spotify:playlist:37i9dQZF1DX1s9knjP51Oa',
                'spotify:playlist:37i9dQZF1DWY4xHQp97fN6',
                'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP'
            ]},
            {'label': 'Channel & Process', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
                'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
                'spotify:playlist:37i9dQZF1DX2Nc3B70tvx0',
                'spotify:playlist:37i9dQZF1DWXLeA8Omikj7',
                'spotify:playlist:37i9dQZF1DX0jgyAiPl8Af'
            ]},
            {'label': 'Cool Down & Calm', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX4sWSpwq3LiO',
                'spotify:playlist:37i9dQZF1DX889U0CL85jj',
                'spotify:playlist:37i9dQZF1DX2pSTOxoPbx9',
                'spotify:playlist:37i9dQZF1DX82GYcclJ3Ug',
                'spotify:playlist:37i9dQZF1DX5Ejj0EkURtP'
            ]}
        ],
        'Distress': [
            {'label': 'Safe Space', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DWXLeA8Omikj7',
                'spotify:playlist:37i9dQZF1DWYJ5kmTbkZiz',
                'spotify:playlist:37i9dQZF1DWZZbwlv3Vmtr',
                'spotify:playlist:37i9dQZF1DWXti3N4Wp5xy',
                'spotify:playlist:37i9dQZF1DX0BcQWzuB7ZO'
            ]},
            {'label': 'Gentle Reflection', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DWUa8ZRTfalHk',
                'spotify:playlist:37i9dQZF1DWVV27DiNWxkR',
                'spotify:playlist:37i9dQZF1DWWhB4HOWKFQc',
                'spotify:playlist:37i9dQZF1DX8ymr6UES7vc',
                'spotify:playlist:37i9dQZF1DX6ziVCJnEm59'
            ]},
            {'label': 'Finding Hope', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DXb0n5M1Mebrs',
                'spotify:playlist:37i9dQZF1DX6ntWKaOqGAp',
                'spotify:playlist:37i9dQZF1DX3Ogo9pFvBkY',
                'spotify:playlist:37i9dQZF1DX8FwnYE6PRvL',
                'spotify:playlist:37i9dQZF1DX4fpCWaHOned'
            ]}
        ],
        'Joy': [
            {'label': 'Embrace the Joy', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX0UrRvztWcAU',
                'spotify:playlist:37i9dQZF1DX1clOuib1KtQ',
                'spotify:playlist:37i9dQZF1DX7KNKjOK0o75',
                'spotify:playlist:37i9dQZF1DXdPec7aLTmlC',
                'spotify:playlist:37i9dQZF1DXbYM3nMM0oPk'
            ]},
            {'label': 'Amplify the Feeling', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX2iUghHXGIjj',
                'spotify:playlist:37i9dQZF1DX2RxBh64BHjQ',
                'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
                'spotify:playlist:37i9dQZF1DWZjqjZMudx9T',
                'spotify:playlist:37i9dQZF1DWXRqgorJj26U'
            ]},
            {'label': 'Sustained Happiness', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DXdPec7aLTmlC',
                'spotify:playlist:37i9dQZF1DWVDC7a6aol5C',
                'spotify:playlist:37i9dQZF1DX2yvmlOdMYzV',
                'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd',
                'spotify:playlist:37i9dQZF1DX7KNKjOK0o75'
            ]}
        ],
        'Default': [
            {'label': 'Acknowledgment', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX889U0CL85jj',
                'spotify:playlist:37i9dQZF1DWXRqgorJj26U',
                'spotify:playlist:37i9dQZF1DX5Ejj0EkURtP',
                'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M',
                'spotify:playlist:37i9dQZF1DWWeNOD4fJ8j4'
            ]},
            {'label': 'Reflection', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DWYJ5kmTbkZiz',
                'spotify:playlist:37i9dQZF1DWVV27DiNWxkR',
                'spotify:playlist:37i9dQZF1DWSlw12ofHcMM',
                'spotify:playlist:37i9dQZF1DWZJhOVGWqUKF',
                'spotify:playlist:37i9dQZF1DX2sUQwD7tbmL'
            ]},
            {'label': 'Empowerment', 'playlist_uris': [
                'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
                'spotify:playlist:37i9dQZF1DXdxcBWuJkbcy',
                'spotify:playlist:37i9dQZF1DWXLeA8Omikj7',
                'spotify:playlist:37i9dQZF1DWXti3N4Wp5xy',
                'spotify:playlist:37i9dQZF1DWY4xHQp97fN6'
            ]}
        ]
    }

    stages = journeys.get(emotion, journeys['Default'])

    # Randomly select one playlist URI for each stage
    journey_plan = []
    for stage in stages:
        uri = random.choice(stage['playlist_uris'])
        journey_plan.append({'label': stage['label'], 'playlist_uri': uri})

    return journey_plan
