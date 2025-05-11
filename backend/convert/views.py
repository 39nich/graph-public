from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from rest_framework.response import Response
""" from .graph_processing.extract_line import extract_line"""
from .ai_models.gpt_vision import analyze_image

@api_view(['POST'])
def upload_file(request):
    file_data = request.FILES.get('file')
    print("FILES received:", request.FILES)
    print("POST data:", request.POST)

    if file_data:
        fs = FileSystemStorage()
        filename = fs.save(file_data.name, file_data)
        file_url = fs.url(filename)

        try:
            full_path = fs.path(filename)

            graph_data = analyze_image(full_path)

            return Response({
                'success': True,
                'filename': filename,
                'file_url': file_url,
                'graph_data': graph_data,
            })
        except Exception as e:
            return Response({
                'fail': True,
                'error': f"Processing failed: {str(e)}",
            })
        
    return Response ({
        'fail': True,
        'error': 'No file received',
    },status=400)
    
