#!/usr/bin/python
# Python program to organize IntroClass files
import os
from subprocess import call
from sets import Set
from student import Student
from patch import Patch, SearchRepairPatch, StudentPatch
from grade_utils import BASE_PATH, patch_grade
import json

GENPROG_TEST = BASE_PATH + "bin/genprog_tests.py" # Path to GenProg test script
BUGHUNT = "/home/chris/Desktop/bughunt/" # Path to SearchRepair patches
projects = ["median"]# ["checksum","digits","grade","median","smallest","syllables"]
students = []
patches = []
project_tests = dict.fromkeys(projects)
project_fails = {}
auto_count = 0
patch_count = 0

def load():
	load_tests()
	load_patches()

def load_tests():
	for proj in project_tests.keys():
		project_tests[proj] = []
		for t in ['blackbox', 'whitebox']:
			test_cases = []
			temp = BASE_PATH+proj+"/tests/"+t+"/"
			for f in os.listdir(temp):
				tcase = f.split(".")[0]
				if tcase not in test_cases:
					test_cases.append(tcase)
					with open(os.path.join(temp, tcase+".in"), "r") as in_file:
						tin = os.path.join(temp, tcase+".in")
					project_tests[proj].append(tin)

def load_patches():
	# auto patces
	i = 0
	for project in projects:
		path = BUGHUNT+project+"/"
		for d in os.listdir(path):
			if '.' in d or "temp" not in os.listdir(path+d):
				continue
			for f in os.listdir(path+d+"/temp/"):
				if "new" in f:
					print f
					i += 1
					patch = SearchRepairPatch(path+d+"/original",path+d+"/temp/"+f)
					patches.append(patch)

def getAutoPatch(project, student, version, test):
	print "Checking for patches..."
	for p in patches:
		if p.project == project and p.student == student and p.version == version:
			p.addFail(test)
			print "Automatic Patch Found"
			return p
	return None

def getStudentPatch(project, current, versions, test):
	versions.sort()
	v = current.split("/")[-1]
	if v in versions and v != max(versions):
		patch = versions[versions.index(v)+1]
		patch_dir = current.replace(v,patch)
		try:
			with open(os.path.join(patch_dir,"metadata.json")) as md:
				data = json.load(md)
		except IOError:
			return None
		test_case = test.split("/")[-1].replace(".in","")
		test_type = test.split("/")[-2]
		if test_case in data[test_type]["pass"]:
			print "Human Patch Found"
			return StudentPatch(current,patch_dir,test)		
	return None

def grade_patches(grade_data):
	g = 0
	for x in grade_data:
		if type(x) == int:
			g += x
		else:
			g += patch_grade(x.original,x.patched,len(set(project_fails[x.fail])),x.project)
	return 100.0*g/len(grade_data)


def analyze():
	projA, projB, projC, projD, projF, total, count = 0, 0, 0, 0, 0, 0, 0
	autoA, autoB, autoC, autoD, autoF, autoTotal, autoP = 0, 0, 0, 0, 0, 0, 0
	manA, manB, manC, manD, manF, manTotal, manP = 0, 0, 0, 0, 0, 0, 0
	patch_total = 0
	baseCSV, autoCSV, manCSV = [], [], []
	for student in students:
		data = student.getGradeData()
		for project in data.keys():
			for version in data[project].keys():
				grade, auto_grade, man_grade = 0, 0, 0
				#print student.short_id, version, data[project][version]
				base = data[project][version]["grade"]
				grade = 100.0*base.count(0)/len(base)
				if grade == 100.0:
					auto_grade = 100.0
					man_grade = 100.0
				else:
					auto_grade = grade_patches(data[project][version]["auto"])
					man_grade = grade_patches(data[project][version]["human"])
					
				total += grade
				count += 1
				autoTotal += auto_grade
				manTotal += man_grade
				patch_total += auto_grade
				patch_total += man_grade
				if grade >= 90:
					projA += 1
				elif grade >= 80:
					projB += 1
				elif grade >= 70:
					projC += 1
				elif grade >= 65:
					projD += 1
				else:
					projF += 1
				if auto_grade >= 90:
					autoA += 1
				elif auto_grade >= 80:
					autoB += 1
				elif auto_grade >= 70:
					autoC += 1
				elif auto_grade >= 65:
					autoD += 1
				else:
					autoF += 1
				if man_grade >= 90:
					manA += 1
				elif man_grade >= 80:
					manB += 1
				elif man_grade >= 70:
					manC += 1
				elif man_grade >= 65:
					manD += 1
				else:
					manF += 1

				print "Generating output files "+project+" "+student.short_id+" "+version+"..."
				baseCSV.append(grade)
				autoCSV.append(auto_grade)
				manCSV.append(man_grade)
				output = os.path.join(".","results",project,student.short_id+".txt")
				res = open(output, "a")
				res.write('Submission: '+version+"\n\tGrade= "+str(grade)+"\n\tSearchRepair= "+str(auto_grade)+"\n\tStudent= "+str(man_grade)+"\n")
				res.close()
			output2 = os.path.join(".","results",project,"project_data.txt")
			project_res = open(output2, 'w')
			project_res.write("Basic Average= "+str(total/count)+" A= "+str(projA)+" B= "+str(projB)+" C= "+str(projC)+" D= "+str(projD)+" F= "+str(projF)+"\n"
				+ "Automated Average= "+str(autoTotal/count)+" A= "+str(autoA)+" B= "+str(autoB)+" C= "+str(autoC)+" D= "+str(autoD)+" F= "+str(autoF)+"\n"
				+ "Human Average= "+str(manTotal/count)+" A= "+str(manA)+" B= "+str(manB)+" C= "+str(manC)+" D= "+str(manD)+" F= "+str(manF)+"\n"
				+ "Patch Average= "+str(patch_total/(count*2)))#+" Automated Patches= "+str(auto_count)+" Human Patches= "+str(man_count))
			project_res.close()			
			csv = os.path.join(".","results",project,"grades.csv")
			csv_res = open(csv, 'w')
			csv_res.write("base,automated,human\n")
			for a, b, c in zip(baseCSV,autoCSV,manCSV):
				csv_res.write(",".join([str(a),str(b),str(c)])+"\n")	
			csv_res.close()
	
def autograder():
	a, s, both = 0, 0, 0
	for project in projects:
		print project.upper()
		output_path = "./results/"+project+"/"
		if not os.path.exists(os.path.dirname(output_path)):
			os.makedirs(os.path.dirname(output_path), 0777)	
		truth = os.path.join(BASE_PATH,project,"tests",project)
		for student in os.listdir(BASE_PATH+project):
			if '.' in student or student in ["Makefile", "tests"]:
				continue
			else:
				new_student = Student(student)
				new_student.addProject(project)
				submissions = os.listdir(os.path.join(BASE_PATH,project,student))
				submissions.remove("Makefile")
				for version in submissions:
					currentDir = os.path.join(BASE_PATH,project,student,version)
					if project not in os.listdir(currentDir):
						continue
					new_student.addSubmission(project, version)
					print new_student.short_id, version
					tests, auto_patches, student_patches = [], [], []
					for t in project_tests[project]:
						# call(["clang", os.path.join(BASE_PATH,project,student,version,project+".c"),"-o",os.path.join(BASE_PATH,project,student,version,project)])
						output = call(["python3",GENPROG_TEST,os.path.join(BASE_PATH,project,student,version,project),truth,t])
						tests.append(output)
						if output == 0:
							auto_patches.append(1)
							student_patches.append(1)
						else:
							if t not in project_fails.keys():
								project_fails[t] = []
								project_fails[t].append(student)
							else:
								project_fails[t].append(student)
							patchA = 0 if getAutoPatch(project,student,version,t) is None else getAutoPatch(project,student,version,t)
							patchS = 0 if getStudentPatch(project,currentDir,submissions,t) is None else getStudentPatch(project,currentDir,submissions,t)
							if patchA != 0:
								a += 1
							if patchS != 0:
								s += 1
							if patchA != 0 and patchS != 0:
								both += 1
							auto_patches.append(patchA)
							student_patches.append(patchS)
					new_student.addGradeData(project, version, "grade", tests)
					new_student.addGradeData(project, version, "auto", auto_patches)
					new_student.addGradeData(project, version, "human", student_patches)
				students.append(new_student)
		output = os.path.join(".","results",project,"patch_data.txt")
		patch_res = open(output, 'w')
		patch_res.write("Automated patch count= "+str(a)+" Human patch count= "+str(s)+" Both count= "+str(both))#+" Automated Patches= "+str(auto_count)+" Human Patches= "+str(man_count))
		patch_res.close()	
		print a, s, both

def main():
	load()
	autograder()
	analyze()
	return "DONE"


if __name__ == '__main__':
	main()

