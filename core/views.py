from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Attendance
from .forms import AddStudentForm, AttendanceForm, UserSignUpForm, UserLoginForm
from django.db.models import Count, Q
from django.core.paginator import Paginator
import json

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'There was an error with your registration.')
    else:
        form = UserSignUpForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    students = Student.objects.all()
    courses = Student.objects.values_list('course', flat=True).distinct()
    
    total_students = students.count()
    total_courses = courses.count()
    has_data = total_students > 0

    if has_data:
        students_per_course = list(students.values('course').annotate(count=Count('course')))
        
        gender_per_course = {}
        for course in courses:
            male_count = students.filter(course=course, gender='M').count()
            female_count = students.filter(course=course, gender='F').count()
            other_count = students.filter(course=course, gender='O').count()
            gender_per_course[course] = {'Male': male_count, 'Female': female_count, 'Other': other_count}

        filter_course = request.GET.get('course')
        if not filter_course and courses:
            filter_course = courses.first()
        top_students = students.filter(course=filter_course).order_by('-percentage')[:10]
    else:
        students_per_course = []
        gender_per_course = {}
        top_students = []
        filter_course = None
        courses = []

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'has_data': has_data,
        'students_per_course': json.dumps(students_per_course),
        'gender_per_course': json.dumps(gender_per_course),
        'top_students': top_students,
        'courses': courses,
        'selected_course': filter_course,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='login')
def add_student_view(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record added successfully!')
            return redirect('student_log')
        else:
            messages.error(request, 'There was an error saving the student record.')
    else:
        form = AddStudentForm()
    return render(request, 'core/add_student.html', {'form': form})

@login_required(login_url='login')
def student_log_view(request):
    students = Student.objects.all()

    filter_course = request.GET.get('course')
    if filter_course:
        students = students.filter(course=filter_course)

    query = request.GET.get('q')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    
    sort_by = request.GET.get('sort', 'asc')
    if sort_by == 'desc':
        students = students.order_by('-first_name', '-last_name')
    else:
        students = students.order_by('first_name', 'last_name')

    paginator = Paginator(students, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = Student.objects.values_list('course', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'courses': courses,
        'selected_course': filter_course,
        'sort_by': sort_by,
        'query': query,
    }
    return render(request, 'core/student_log.html', context)

@login_required(login_url='login')
def update_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = AddStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record updated successfully!')
            return redirect('student_log')
        else:
            messages.error(request, 'There was an error updating the student record.')
    else:
        form = AddStudentForm(instance=student)
    return render(request, 'core/update_student.html', {'form': form})

@login_required(login_url='login')
def delete_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted successfully!')
        return redirect('student_log')
    return redirect('student_log') 

@login_required(login_url='login')
def attendance_log_view(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.save()
            messages.success(request, 'Attendance record saved successfully!')
            return redirect('attendance_log')
        else:
            messages.error(request, 'There was an error saving the attendance record.')
    else:
        form = AttendanceForm()

    students = Student.objects.all().order_by('first_name')
    context = {
        'form': form,
        'students': students,
    }
    return render(request, 'core/attendance_log.html', context)

@login_required(login_url='login')
def about_us_view(request):
    return render(request, 'core/about_us.html')
