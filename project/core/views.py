from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from music21 import *

# Create your views here.
def hello_view(request):
    return JsonResponse({"message": "Hello from Django!"})

@api_view(['POST'])
def identify_chord(request):
    # Define a series of notes
    #notes = ['C', 'E', 'G', 'B']  # For example, a C major 7 chord
    #notes = ['A#', 'G', 'D', 'F']
    notes = request.data.get('notes', [])

    # Create Note objects from the note names
    note_objects = [note.Note(n) for n in notes]

    # Create a Chord object from the Note objects
    chord_object = chord.Chord(note_objects)

    # Retrieve the specific chord name and root
    chord_name = chord_object.pitchedCommonName
    #chord_name = chord_object.commonName
    chord_root = chord_object.root().nameWithOctave

    print("Chord Name:", chord_name)
    print("Chord Root:", chord_root)
    return Response({'chord': chord_name})