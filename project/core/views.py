from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from music21 import *

# Create your views here.
def hello_view(request):
    return JsonResponse({"message": "Hello from Django!"})

# Given an array of notes, return the according chord
@api_view(['POST'])
def identify_chord(request):
    notes = request.data.get('notes', [])
    note_objects = [note.Note(n) for n in notes]
    chord_object = chord.Chord(note_objects)

    chord_name = chord_object.pitchedCommonName
    chord_root = chord_object.root().nameWithOctave

    return Response({'chord': chord_name})

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
    # scales
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
    #progression = [enharmonic_equivalents[chord] if chord in enharmonic_equivalents else chord for chord in progression]

    return progression
