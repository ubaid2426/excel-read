import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer

class UploadFileView(APIView):
    # Handle POST requests for file upload and parsing
    def post(self, request, *args, **kwargs):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()

            try:
                # Read and parse the uploaded Excel file
                file_path = uploaded_file.content.path
                df = pd.read_excel(file_path, engine='openpyxl')
                data = df.to_dict(orient='records')

                # Optionally log the data or store it in another model
                return Response({
                    "status": "success",
                    "uploaded_file": serializer.data,
                    "excel_data": data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                uploaded_file.delete()  # Clean up the uploaded file if parsing fails
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle GET requests to retrieve uploaded files and their data
    def get(self, request, *args, **kwargs):
        uploaded_files = UploadedFile.objects.all()
        # Serialize the data of uploaded files
        serializer = UploadedFileSerializer(uploaded_files, many=True)

        # Optionally, you can also return the Excel data by reading each file
        files_with_data = []
        for uploaded_file in uploaded_files:
            try:
                # Read and parse the uploaded Excel file
                file_path = uploaded_file.content.path
                df = pd.read_excel(file_path, engine='openpyxl')
                data = df.to_dict(orient='records')
                
                files_with_data.append({
                    "file_info": serializer.data,
                    "excel_data": data
                })
            except Exception as e:
                # Handle file reading errors if needed
                files_with_data.append({
                    "file_info": serializer.data,
                    "excel_data": str(e)  # You can store the error message if the file can't be processed
                })

        return Response({
            "status": "success",
            "files_with_data": files_with_data
        }, status=status.HTTP_200_OK)
