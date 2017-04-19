# -*- coding: utf-8 -*- 
"""
Clase Course para el problema Timetabling
José González Ayerdi - A01036121
ITESM Campus Monterrey
04/2017  
"""
class Course():
	"""Inicializamos el id, la cantidad de estudiantes y la lista de estudiantes para el curso"""
	def __init__(self, course_id=0, no_students=0, student_list=[]):
		self.course_id    = course_id
		self.no_students  = no_students
		self.student_list = []