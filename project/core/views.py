from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from music21 import *

from core.models import UserModel

# Create your views here.
# TEST ENDPOINT
def hello_view(request):
    return JsonResponse({"message": "Hello from Django!"})

# CREATE NEW USER
@api_view(['POST'])
def save_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    passwordConf = request.data.get('passwordConf')

    if username and password and passwordConf:
        if password == passwordConf:
            try:
                new_user = User(username=username)
                new_user.set_password(password)
                new_user.save()
                
                user_data = {
                    'id': new_user.id,
                    'username': new_user.username,
                }

                return JsonResponse({'message': 'User saved successfully!', 'user': user_data})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'error': 'Invalid request. Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)

# LOGIN AUTHENTICATION
@api_view(['POST'])
def auth(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password) # authenticate

    if user is not None:
        # Authentication successful
        return JsonResponse({'message': 'Login successful'})
    else:
        # Authentication failed
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

# Given an array of notes, return the according chord
@api_view(['POST'])
def identify_chord(request):
    notes = request.data.get('notes', [])
    note_objects = [note.Note(n) for n in notes]
    chord_object = chord.Chord(note_objects)

    chord_name = chord_object.pitchedCommonName
    chord_root = chord_object.root().nameWithOctave

    return Response({'chord': chord_name})

# GENERATE CHORD PROGRESSION METHODS
# endpoint called when getting chords in a key
@api_view(['GET'])
def generate_chord_progression(request):
    # request params
    key = request.GET.get('key')
    acc = request.GET.get('acc')
    major_minor = request.GET.get('major_minor')

    generated_chords = generate_progression(key, acc, major_minor)

    # generated chord progression
    return Response({'chord_progression': generated_chords})

def generate_progression(selected_key, selected_acc, selected_major_minor):
    scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    starting_index = scale.index(selected_key)

    progression = [
        scale[(starting_index) % 12],        # I
        scale[(starting_index + 2) % 12],    # ii
        scale[(starting_index + 4) % 12],    # iii
        scale[(starting_index + 5) % 12],    # IV
        scale[(starting_index + 7) % 12],    # V
        scale[(starting_index + 9) % 12],    # vi
        scale[(starting_index + 11) % 12]    # vii°
    ]

    if selected_acc == '#':
        progression = [chord + '#' if '#' not in chord else chord.replace('#', '♭') for chord in progression]
    elif selected_acc == '♭':
        progression = [chord + '♭' if '♭' not in chord else chord.replace('♭', '#') for chord in progression]

    progression = ['F' if chord == 'E#' else chord for chord in progression]
    progression = ['C' if chord == 'B#' else chord for chord in progression]

    enharmonic_equivalents = {'C#': 'D♭', 'D#': 'E♭', 'F#': 'G♭', 'G#': 'A♭', 'A#': 'B♭', 'E#': 'F', 'B#': 'C'}

    return progression
