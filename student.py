from sets import Set

GRADE_TYPES = ["grade","auto","human"]


class Student(object):

	submissions = Set([])
	grades = {}
	short_id = None
	
	def __init__(self, student_id):
		self.id = student_id
		self.short_id = student_id[0:5]
		self.grades = dict()

	def addProject(self, project):
		if project not in self.grades.keys():
			self.grades[project] = dict()
		
	def addSubmission(self, project, submit):
		if submit not in self.grades[project].keys():
			self.grades[project][submit] = dict.fromkeys(GRADE_TYPES)
			
	def addGradeData(self, project, submit, grade_type, data):
		if grade_type not in GRADE_TYPES:
			raise ValueError("Invalid grade type")
		else:
			self.grades[project][submit][grade_type] = data

	def getFinalSubmit(self, project):
		if project in self.grades.keys():
			final = max(self.grades[project].keys())
		else:
			raise ValueError("Nothing submitted for this project")
		return final

	def getGradeData(self):
		return self.grades
				