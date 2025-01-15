import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer

class UploadFileView(APIView):
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
