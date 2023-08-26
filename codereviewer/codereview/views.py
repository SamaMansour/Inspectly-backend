from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.shortcuts import render

# Create your views here.

import gradio as gr
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()


def basic_code_review(code: str) -> str:
    lines = code.split('\n')
    line_count = len(lines)
    char_count = len(code)

    keywords = ['def', 'return', 'import',
                'for', 'while', 'if', 'else', 'elif']
    keyword_count = {word: code.count(word) for word in keywords}

    function_count = code.count('def ')
    comment_count = sum(1 for line in lines if line.strip().startswith("#"))
    comment_ratio = comment_count / line_count if line_count != 0 else 0

    long_lines = [line for line in lines if len(line) > 79]

    feedback = []
    feedback.append(f"Lines of code: {line_count}")
    feedback.append(f"Characters: {char_count}")
    feedback.append("\nKeywords count:")
    for k, v in keyword_count.items():
        if v > 0:
            feedback.append(f"{k}: {v}")

    feedback.append(f"\nNumber of functions: {function_count}")
    feedback.append(
        f"Comment ratio (comments/total lines): {comment_ratio:.2f}")

    if long_lines:
        feedback.append("\nCoding style issues:")
        feedback.append("Some lines are too long (more than 79 characters).")

    # Basic code quality check
    if line_count > 300:
        feedback.append(
            "\nThe code is quite long. Consider modularizing or refactoring.")
    if function_count == 0:
        feedback.append(
            "No functions found. Consider using functions/methods to organize your code better.")
    if comment_ratio < 0.1:
        feedback.append(
            "Low comment ratio. Consider adding more comments for clarity.")

    return "\n".join(feedback)


def gradio_interface(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        feedback = basic_code_review(code)
        return render(request, 'result.html', {'feedback': feedback})

    return render(request, 'interface.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username, password=password)
        return Response({'status': 'signup successful'}, status=200)
    else:
        return Response({'status': 'username already exists'}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        # you can also use JWT for authentication here
        return Response({'status': 'login successful'}, status=200)
    else:
        return Response({'status': 'invalid credentials'}, status=400)
