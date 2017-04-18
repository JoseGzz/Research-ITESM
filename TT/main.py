# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema Timetabling
José González Ayerdi - A01036121
ITESM Campus Monterrey
04/2017  
"""
from formatter import Formatter

def main():
	course_content = None
	student_info    = None
	courses_file_name = "data/car-f-92.crs"
	student_file_name = "data/car-f-92.stu"
	course_dict  = {}
	student_dict = {}

	with open(courses_file_name, "r+") as f:
		course_content = [course.split() for course in [line.rstrip('\n') for line in f]]
	#print(studen_info)

	with open(student_file_name, "r+") as f:
		student_info = [student.split() for student in [line.rstrip('\n') for line in f]]
	#print(course_content)

	course_dict, student_dict = Formatter(course_content, student_info).format()

	"""
	# imprime contenido de diccionario de cursos para probar
	for course_id, course in course_dict.items():
		print(course.course_id)
		print(course.no_students)
		for student in course.student_list:
			print(student.student_id)
	"""

	for student_id, student in student_dict.items():
		print(student_id)
		for course in student.course_list:
			print(course.course_id)

if __name__ == "__main__":
    main()