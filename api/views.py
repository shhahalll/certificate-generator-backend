from django.shortcuts import render
from django.http import FileResponse
from .models import List, Template
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image, ImageDraw, ImageFont
from .serializers import ListSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import io
import os
from django.conf import settings

def getCertificate(name, role):
    """Generates a certificate as a PDF."""
    image_path = os.path.join(settings.BASE_DIR, 'api', 'templates', 'templat.png')
    bg_image = Image.open(image_path)
    draw = ImageDraw.Draw(bg_image)
    
    # Load font
    font_path = os.path.join(settings.BASE_DIR, 'api', 'fonts', 'Montserrat-Medium.ttf')
    font = ImageFont.truetype(font_path, 60)
    
    # Add Name
    draw.text((750, 600), name, font=font, fill="black")
    
    # Add Role
    font = ImageFont.truetype(font_path, 40)
    role_text = "Volunteer" if role == 0 else "Sub Coordinator" if role == 1 else "Core Coordinator"
    draw.text((1160, 700), role_text, font=font, fill="black")
    
    # Convert to PDF
    pdf_buffer = io.BytesIO()
    bg_image.convert("RGB").save(pdf_buffer, format="PDF")
    pdf_buffer.seek(0)

    return pdf_buffer

class GetCert(APIView):
    def post(self, request, state):
        data = request.data
        name = data.get("name")
        role = data.get("role", 0)
        
        if not name:
            return Response({"error": "Name is required"}, status=400)
        
        try:
            if state == 0:
                role = 0
            
            # Generate the PDF
            pdf_bytes = getCertificate(name=name, role=role)
            Listso = List.objects.create(name=name,role=role)
            Listso.save()
            
            # Return as a FileResponse
            response = FileResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{name}_certificate.pdf"'
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ListAll(APIView):
    def get(self, request):
        data = List.objects.all()
        serialized_data = ListSerializer(data, many=True)
        return Response(serialized_data.data)  # Fixed `.data`

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username') 
        password = request.data.get('password')   
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user.username
            })
        else:
            return Response({"error": "Invalid Credentials"}, status=400)

class UploadTemplate(APIView):
    def post(self, request):
        Template.objects.all().delete()
        Template.objects.create(template=request.data.get('src'))  # Fixed `.create()`
        return Response({"message": "Template uploaded successfully"})
