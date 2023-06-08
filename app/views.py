from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from app.models import User,Comment
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import PDFFile,SharedFile
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .serializers import UserSerializer,PDFFileSerializer,SharedFileSerializer,CommentSerializer
import json
from django.views.generic import TemplateView
from django.db.models import Q


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = PDFFile.objects.all()
        return context

@login_required(login_url='login')
def user_list(request):
    try:
        search_query = request.GET.get('search_query')
        if(search_query==None):
            users=User.objects.filter()
        else:
            users = User.objects.filter(
                        Q(username__icontains=search_query) |
                        Q(first_name__icontains=search_query) |
                        Q(last_name__icontains=search_query) |
                        Q(email__icontains=search_query)
                    )
    except Exception as e:
        print(str(e))
        users = None
    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='login')
def search_users(request):
    try:
        # breakpoint()
        search_query = request.GET.get('search_query')
        users = User.objects.filter(Q(title__icontains=search_query))

    except Exception as e:
        print(str(e))
        files = None

    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='login')
def file(request, file_uuid):

    pdf_file=None
    comments=None

    try:
        pdf_file = PDFFile.objects.get(unique_link=file_uuid)
    except PDFFile.DoesNotExist:
        return render(request, 'file_does_not_exist.html')

    user=request.user

    # Check if a SharedFile with the given user and pdf_file already exists
    if SharedFile.objects.filter(user=user, pdf_file=pdf_file).exists()==False and pdf_file.uploaded_by!=user:
        return render(request, 'access_denied.html')
    

    try:
        comments = Comment.objects.filter(pdf_file=pdf_file)
    except Comment.DoesNotExist:
        pass
    return render(request, 'profile.html', {'file': pdf_file,'comments':comments})


@login_required(login_url='login')
def search_files(request):
    try:
        # breakpoint()
        search_query = request.GET.get('search_query')

        user =  request.user
        shared_file_objs=SharedFile.objects.filter(user_id=user.id)
        ids=[]
        for shared_file in shared_file_objs:
            ids.append(shared_file.pdf_file.id)
        
        files1=None
        files2=None
        
        if(search_query==None):
            files1 = PDFFile.objects.filter(Q(uploaded_by_id=user.id))
            files2 = PDFFile.objects.filter(Q(id__in=ids))
        else:
            files1 = PDFFile.objects.filter(Q(title__icontains=search_query) & Q(uploaded_by_id=user.id))
            files2 = PDFFile.objects.filter(Q(title__icontains=search_query) & Q(id__in=ids))
        
        files = list(files1) + list(files2)

        # files = file1 | file2
    except  Exception as e:
        print(str(e))
        files = None
    return render(request, 'search.html', {'files': files})

@login_required(login_url='login')
def add_comment(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        comment_text = request.POST.get('comment')
        unique_link = request.POST.get('unique_link')
        print(unique_link)
        pdf_file = PDFFile.objects.get(unique_link=unique_link)
        # Create a new Comment object and save it to the database
        comment = Comment(user=request.user, content=comment_text,pdf_file=pdf_file)
        comment.save()

        # Redirect to a success page or the same page to display the updated comments
        return redirect('/file/'+ str(unique_link))

    return render(request, 'add_comment.html')

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'upload.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        name=request.POST.get('name')
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            try:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1, first_name=name)
                my_user.save()
                return redirect('login')
            except:
                return render (request,'duplicate.html')

    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('search')
        else:
             return render(request, 'base.html')

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def upload(request):
    print(request)
    title = request.POST.get('title')
    file = request.FILES.get('file')
    uploaded_by = request.user
    print("testing")
    # Check if the file is a PDF
    if file.content_type != 'application/pdf':
        return HttpResponse('Invalid file type. Only PDF files are allowed.',status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    if title and file and uploaded_by:
        # Save the file using default storage
        file_path = default_storage.save(file.name, ContentFile(file.read()))
        
        # Save the file details in the database
        uploaded_file = PDFFile.objects.create(title=title, file=file_path, uploaded_by=uploaded_by)
        return HttpResponseRedirect('/search/')  # Redirect to the desired page
        return HttpResponse({'file_id': uploaded_file.id}, status=status.HTTP_201_CREATED)
    else:
        return HttpResponse({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def files(request):
    try:
        user = request.user
        files = None
        
        if user.is_superuser:
            files = PDFFile.objects.all()
        else:
            files = SharedFile.objects.filter(user=user)
            
        serializer = PDFFileSerializer(files, many=True)
        json_data = json.dumps(serializer.data)
        
        return HttpResponse(json_data)
    
    except ObjectDoesNotExist:
        return HttpResponse("User or file does not exist", status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def share(request):
    try:
        file_id = request.POST.get('file')
        shared_with_email = request.POST.get('email')

        if User.objects.filter(email=shared_with_email).exists()==False:
           return HttpResponse("Account Does not Exist ", status=404)


        user_obj = User.objects.get(email=shared_with_email)
        pdf_file_obj = PDFFile.objects.get(id=file_id)
        
        

        # Check if a SharedFile with the given user and pdf_file already exists
        if SharedFile.objects.filter(user=user_obj, pdf_file=pdf_file_obj).exists():
            return HttpResponse("SharedFile already exists", status=409)
        
        if PDFFile.objects.filter(uploaded_by=user_obj, id=file_id).exists():
            return HttpResponse("Selected Email is Owner of this File", status=409)

        obj = SharedFile(user=user_obj, pdf_file=pdf_file_obj)
        obj.save()
        
        serializer = SharedFileSerializer(obj)
        return JsonResponse(serializer.data)
        
    except ObjectDoesNotExist:
        return HttpResponse("Invalid file_id or shared_with_email or user does not exist", status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)