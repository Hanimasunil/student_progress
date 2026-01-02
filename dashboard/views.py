import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .models import Student, Progress
from .forms import StudentForm, ProgressForm

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            return render(request, 'dashboard/signup.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        profile = user.profile
        profile.otp = str(random.randint(100000, 999999))
        profile.save()


        send_mail(
            subject='Your OTP for Account Verification',
            message=f'Hello {email},\n\nYour OTP for account verification is: {profile.otp}\n\nThank you!',
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[email],
            fail_silently=False,
        )

        request.session['user_id'] = user.id
        return redirect('verify_otp')

    return render(request, 'dashboard/signup.html')



def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup')

    user = User.objects.get(id=user_id)
    profile = user.profile

    if request.method == 'POST':
        otp = request.POST['otp']
        if otp == profile.otp:
            user.is_active = True
            user.save()
            profile.is_verified = True
            profile.save()
            return redirect('login')
        else:
            return render(request, 'dashboard/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'dashboard/verify_otp.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user:
            if user.profile.is_verified:
                auth_login(request, user)
                return redirect('student_list')
            else:
                return render(request, 'dashboard/login.html', {'error': 'Account not verified. Check OTP.'})
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})


    return render(request, 'dashboard/login.html')



@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def student_list(request):
    exam_filter = request.GET.get('exam')
    search_query = request.GET.get('search')
    students = Student.objects.all()

    if search_query:
        students = students.filter(full_name__icontains=search_query) | students.filter(roll_number__icontains=search_query)

    student_data = []
    for student in students:
        if exam_filter:
            progress_entries = student.progress_set.filter(exam_type=exam_filter)
        else:
            progress_entries = student.progress_set.all()

        total = sum(p.total_marks for p in progress_entries)
        count = progress_entries.count()
        average = total / count if count > 0 else 0

        student_data.append({
            'student': student,
            'total': total,
            'average': round(average, 2),
        })

    student_data.sort(key=lambda x: x['total'], reverse=True)

    paginator = Paginator(student_data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_performer = student_data[0] if student_data else None

    return render(request, 'dashboard/student_list.html', {
        'page_obj': page_obj,
        'exam_filter': exam_filter,
        'top_performer': top_performer,
        'search_query': search_query
    })

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'dashboard/add_student.html', {'form': form})

@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'dashboard/add_student.html', {'form': form})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')


@login_required
def add_progress(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = ProgressForm(initial={'student': student})
    return render(request, 'dashboard/add_progress.html', {'form': form, 'student': student})
