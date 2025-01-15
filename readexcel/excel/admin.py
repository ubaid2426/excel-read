from django.contrib import admin
from .models import UploadedFile
import pandas as pd

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uploaded_at', 'content')
    readonly_fields = ('uploaded_at',)

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly if the object is already uploaded
        if obj:
            return [field.name for field in self.model._meta.fields]
        return self.readonly_fields

    def changelist_view(self, request, extra_context=None):
        # Add parsed Excel data to the admin changelist view
        if request.method == 'POST' and 'content' in request.FILES:
            file = request.FILES['content']
            try:
                # Parse the uploaded Excel file
                df = pd.read_excel(file, engine='openpyxl')
                # Pass the data as context for the admin panel
                extra_context = extra_context or {}
                extra_context['excel_data'] = df.to_dict(orient='records')
            except Exception as e:
                self.message_user(request, f"Error reading Excel file: {str(e)}", level="error")

        return super().changelist_view(request, extra_context=extra_context)
