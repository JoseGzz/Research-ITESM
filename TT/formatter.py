from student import Student
from course  import Course

class Formatter():
	def __init__(self, course_content=None, student_info=None):
		self.course_content = course_content
		self.student_info   = student_info

	def format(self):
		courses  = self.generate_course_dict()
		students = self.generate_student_dict(courses)
		return courses, students

	def generate_course_dict(self):
		courses = {}
		for course in self.course_content:
			tmp = Course(course[0], int(course[1]))
			courses[tmp.course_id] = tmp
		return courses

	def generate_student_dict(self, courses):
		students = {}
		for i, student_courses in enumerate(self.student_info):
			student = Student()
			student.student_id = i
			for course in student_courses:
				student.course_list.append(courses.get(course))
				courses[course].student_list.append(student)
			students[i] = student
		return students