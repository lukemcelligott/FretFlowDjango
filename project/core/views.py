from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def hello_view(request):
    return JsonResponse({"message": "Hello from Django!"})

@api_view(['POST'])
def identify_chord(request):
    notes = request.data.get('notes', [])  # Assuming the notes are sent in the request body
    chord_library = {
        'C': ['C', 'E', 'G'],
        'D': ['D', 'F#', 'A'],
        # Add more chord definitions here...
    }

    for chord_name, chord_notes in chord_library.items():
        if all(note in chord_notes for note in notes):
            return Response({'chord': chord_name})

    return Response({'chord': 'Unknown'})