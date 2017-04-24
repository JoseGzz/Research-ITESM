# -*- coding: utf-8 -*- 
"""
Clase para generar diccioanrios de objetos para el problema Timetabling
José González Ayerdi - A01036121
ITESM Campus Monterrey
04/2017  
"""

from student import Student
from course  import Course

class Formatter():
	"""Inicializamos las listas de cursos y estudiantes"""
	def __init__(self, course_content=None, student_info=None):
		self.course_content = course_content
		self.student_info   = student_info

	"""format regresa los diccioanrios de objetos correspondientes a los cursos y estudiantes"""
	def format(self):
		courses  = self.generate_course_dict()
		students = self.generate_student_dict(courses)
		return courses, students

	"""generate_course_dict genera el diccionario de cursos con su id y la cantidad de estudiantes"""
	def generate_course_dict(self):
		courses = {}
		for course in self.course_content:
			tmp = Course(course[0], int(course[1]))
			courses[tmp.course_id] = tmp
		return courses

	"""generate_student_dict genera el diccionario de estudiantes con su id, la lista de cursos a los que está
	inscrito y a esos cursos les agrega sus estudiantes inscritos"""
	def generate_student_dict(self, courses):
		students = {}
		for i, student_courses in enumerate(self.student_info):
			student = Student()
			student.student_id = i
			for course in student_courses:
				student.course_list.append(courses.get(course))
				# TODO: preguntar si este curso ya estaba asignado a alguien mas
				# pasar iccionario a funcion y curso actual
				courses[course].student_list.append(student)
			students[i] = student
		return students