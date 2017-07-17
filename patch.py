from grade_utils import BASE_PATH
import os

class Patch(object):

	original = None
	patched = None
	project = None
	student = None
	version = None
	fail = None

	def __init__(self, old_path, new_path, project, student, version, failed=None):
		self.original = old_path
		self.patched = new_path
		self.project = project
		self.student = student
		self.version = version
		self.fail = failed

	def addFail(self, test):
		self.fail = test

class SearchRepairPatch(Patch):
	def __init__(self, orig, patch):
		with open(orig, 'r') as o:
			yalin = o.read()
		orig_list = yalin.split("/")
		version = orig_list[-1]
		student = orig_list[-2]
		project = orig_list[-3]
		original = os.path.join(BASE_PATH,project,student,version,project+".c")
		Patch.__init__(self, original, patch, project, student, version)

class StudentPatch(Patch):
	def __init__(self, orig_dir, patch_dir, test=None):
		orig_list = orig_dir.split("/")
		version = orig_list[-1]
		student = orig_list[-2]
		project = orig_list[-3]
		original = os.path.join(orig_dir,project+".c")
		patched = os.path.join(patch_dir,project+".c")
		Patch.__init__(self, original, patched, project, student, version, test)

