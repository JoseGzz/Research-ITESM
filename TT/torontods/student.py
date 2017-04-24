# -*- coding: utf-8 -*- 
"""
Clase Student para el problema Timetabling
José González Ayerdi - A01036121
ITESM Campus Monterrey
04/2017  
"""
class Student():
	"""Inicializamos el id y la lista de cursos a los que está inscrito un estudiante"""
	def __init__(self, student_id=0, course_list=[]):
		self.student_id = student_id
		self.course_list = []