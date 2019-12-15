from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic import TemplateView
@login_required
def home(request):
	context = {'name' : 'Andy', 'age':'40'}
	return render(request, 'studentInfo/home.html',context)

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return[ dict(zip(columns,row)) for row in cursor.fetchall()]

@login_required
def studentinfo(request):
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM StudentDetails')
	student_list = dictfetchall(cursor)
	paginator = Paginator(student_list,5)
	page = request.GET.get('page')
	try:
		studentDetails = paginator.get_page(page)
	except PageNotAnInteger:
		studentDetails = paginator.get_page(1)
	except EmptyPage:
		studentDetails = paginator.get_page(1)
	except:
		studentDetails = paginator.get_page(1)

	return render(request, 'studentInfo/studentDetails.html', {'studentInfo':studentDetails})

@login_required
def courseinfo(request):
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM CourseDetails')
	student_list = dictfetchall(cursor)
	paginator = Paginator(student_list,5)
	page = request.GET.get('page')
	try:
		courseDetails = paginator.get_page(page)
	except PageNotAnInteger:
		courseDetails = paginator.get_page(1)
	except EmptyPage:
		courseDetails = paginator.get_page(1)
	except:
		courseDetails = paginator.get_page(1)
	return render(request, 'studentInfo/courseDetails.html', {'courseInfo':courseDetails})


def studentEnrollment(request):
	cursor = connection.cursor()
	if 'student' not in request.session:
		cursor.execute("SELECT LASTNAME FROM StudentDetails LIMIT 1")
		name = cursor.fetchone()
		request.session['student'] = name[0]
	if('student' in request.GET):
		request.session['student'] = request.GET.get('student')
	cursor.execute("SELECT * FROM StudentDetails WHERE LASTNAME = %s", [request.session['student']])
	cursor.execute("SELECT*FROM studentDetails")
	studentDetails1 = dictfetchall(cursor)
	cursor.execute("INSERT INTO studentEnrollment(LASTNAME, COURSENAME1, COURSENAME2, COURSENAME3) VALUES (%s, %s, %s, %s)",(request.session['student'], request.session['course1'], request.session['course2'], request.session['course3']))


	if 'course1' not in request.session:
		cursor.execute("SELECT COURSENAME FROM courseDetails LIMIT 1")
		name = cursor.fetchone()
		request.session['course1'] = name[0]
	if('course1' in request.GET):
		request.session['course1'] = request.GET.get('course1')
	cursor.execute("SELECT * FROM courseDetails WHERE COURSENAME = %s", [request.session['course1']])
	cursor.execute("SELECT*FROM courseDetails")
	courseDetails2 = dictfetchall(cursor)

	if 'course2' not in request.session:
		cursor.execute("SELECT COURSENAME FROM courseDetails LIMIT 1")
		name = cursor.fetchone()
		request.session['course2'] = name[0]
	if('course2' in request.GET):
		request.session['course2'] = request.GET.get('course2')
	cursor.execute("SELECT * FROM courseDetails WHERE COURSENAME = %s", [request.session['course2']])
	cursor.execute("SELECT*FROM courseDetails")
	courseDetails3 = dictfetchall(cursor)

	if 'course3' not in request.session:
		cursor.execute("SELECT COURSENAME FROM courseDetails LIMIT 1")
		name = cursor.fetchone()
		request.session['course3'] = name[0]
	if('course3' in request.GET):
		request.session['course3'] = request.GET.get('course3')
	cursor.execute("SELECT * FROM courseDetails WHERE COURSENAME = %s", [request.session['course3']])
	cursor.execute("SELECT*FROM courseDetails")
	courseDetails3 = dictfetchall(cursor)

	return render(request, 'studentInfo/studentEnrollment.html', {'studentInfo':studentDetails, 'courseInfo1':courseDetails1, 'courseInfo2':courseDetails2, 'courseInfo3':courseDetails3})

def graduationRate(request):
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM GraduationRate')
	graduationRate = dictfetchall(cursor)
	return render(request, 'studentInfo/graduationRate.html',{'graduationRateInfo': graduationRate})

