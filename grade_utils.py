BASE_PATH = "/home/chris/Desktop/IntroClass/" # Path to IntroClass directory

# Number of students
size = {
	"checksum": 21,
	"digits": 55,
	"grade": 50,
	"median": 44,
	"smallest": 45,
	"syllables": 44
}

def distance(str1, str2):
	if str1 == str2:
		return 0
	last = None
	row = range(1, len(str2)+1) + [0]
	for x in xrange(len(str1)):
		last2, last, row = last, row, [0]*len(str2) + [x+1]
		for y in xrange(len(str2)):
			delete = last[y] + 1
			insert = row[y-1] + 1
			swap = last[y-1] + (str1[x] != str2[y])
			row[y] = min(delete, insert, swap)
	return row[len(str2) - 1]

def edit_distance(file1, file2):
	f1 = open(file1, 'r')
	f2 = open(file2, 'r')
	text1 = f1.read()
	text2 = f2.read()
	f1.close()
	f2.close()
	edit = distance(text1,text2)
	return 1 - (1.0*edit/(max(len(text1),len(text2))))

def class_performance(defects, project):
	return 1.0*defects/size[project]

def patch_grade(orig_path, patch_path, defects, project):
	ed = edit_distance(orig_path, patch_path)
	cp = class_performance(defects, project)
	grade = 0.5*ed + 0.5*cp
	return grade
