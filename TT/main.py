# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema Timetabling
José González Ayerdi - A01036121
ITESM Campus Monterrey
04/2017  
"""
from formatter import Formatter
import numpy as np

def main():
	course_content    = None
	student_info      = None
	courses_file_name = "data/car-f-92.crs"
	student_file_name = "data/car-f-92.stu"
	course_dict       = {}
	student_dict      = {}


	# leemos el archivo con la informacion de los cursos (id, cantidad de estudiantes)
	with open(courses_file_name, "r+") as f:
		course_content = [course.split() for course in [line.rstrip('\n') for line in f]]
	#print(studen_info)

	# leemos el archivo con la información de los estudiantes (lista de cursos a los que está inscrito)
	with open(student_file_name, "r+") as f:
		student_info = [student.split() for student in [line.rstrip('\n') for line in f]]
	#print(course_content)

	# generamos diccioanrios de objetos que representan a los cursos y a los estudiantes con todos sus atributos
	course_dict, student_dict = Formatter(course_content, student_info).format()

	total_students  = len(student_dict)
	total_courses   = len(course_dict)
	conflict_matrix = np.zeros(total_courses * total_courses).reshape(total_courses, total_courses)
	conflicts = 0

	for course_id, course in course_dict.items():
		students = course.student_list
		for course_id2, course2 in course_dict.items():
			students2 = course2.student_list
			for student in students:
				for student2 in students2:
					if student.student_id == student2.student_id:
						conflict_matrix[course.get_numeric_id() - 1][course2.get_numeric_id() - 1] = 1
						conflicts += 1
						print(conflicts)

	print(conflict_matrix)
	print("Conflict density:", conflicts/(total_courses*total_courses))

	"""
	# imprime contenido de diccionario de cursos para probar
	for course_id, course in course_dict.items():
		print(course.course_id)
		print(course.no_students)
		for student in course.student_list:
			print(student.student_id)
	"""

	""" 
	# imprimie contenio de dicionario de estudiantes para probar
	for student_id, student in student_dict.items():
		print(student_id)
		for course in student.course_list:
			print(course.course_id)
	"""

if __name__ == "__main__":
    main()