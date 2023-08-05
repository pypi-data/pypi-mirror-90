
#-*- coding: utf-8 -*-

class Student:
	def __init__(self,name,lastname):
		self.name = name
		self.lastname = lastname
		self.exp = 0 #คะแนนประสบการณ์
		self.lession = 0 #จำนวนคลาสที่เรียน
		self.vehicle = 'รภเมลล์'

	@property
	def fullname(self):
		return '{} {}'.format(self.name, self.lastname)

	def Codeing(self):
		'''
		นี่คือคลาสเรียนวิชาเขียนโปรแกรม'''
		self.AddEXP()
		print('{} กำลังเรียนเขียนโปรแกรม...'.format(self.fullname))

	def ShowExp(self):
		print('{} ได้คะแนน {} exp (เรียนไปแล้ว {} ครั้ง)'.format(self.name, self.exp, self.lession))

	def AddEXP(self):
		self.exp += 10 
		self.lession += 1

	def __str__(self):
		return self.fullname

	def __repr__(self):
		return self.fullname

	def __add__(self, other):
		return self.exp + other.exp

class Tesla:
	def __init__(self):
		self.model = 'Tesla Model S'

	def SelfDriving(self,st):
		print('ระบบขับอัติโนมัติกำลังทำงาน...กำลังไาคุณ{}กลับบ้าน!'.format(st.name))

	def __str__(self):
		return self.model

class SpecialStudent(Student):
	def __init__(self, name, lastname,father):
		super().__init__(name, lastname)

		self.father = father
		self.vehicle = Tesla()

		print('รู้ไหมฉันลูกใคร?...! พ่อฉันชื่อ {}'.format(self.father))

	def AddEXP(self):
		self.exp += 30
		self.lession += 2

class Teacher:
	def __init__(self,fullname):
		self.fullname = fullname
		self.students = []

	def CheckStudent(self):
		print('----นักเรียนของคุณครู {}----'.format(self.fullname))
		for i,st in enumerate(self.students):
			print('{}-->{} [ {}exp][เรียนไป {} ครั้ง]'.format(i+1, st.fullname, st.exp, st.lession))

	def AddStudent(self,st):
		self.students.append(st)

if __name__ == '__main__':
	#Day 0
	allstudent = []

	teacher1 = Teacher('Ada Lovelace')
	teacher2 = Teacher('Bill Gates')
	print(teacher1.students)




	#Day 1
	print('----------Day 1 --------')
	St1 = Student('Albert','Einstein')
	allstudent.append(St1)
	teacher2.AddStudent(St1)
	print(St1.fullname)

	print('----------Day 2 --------')
	#Day 2
	St2 = Student('Steve','Jobs')
	allstudent.append(St2)
	teacher2.AddStudent(St1)
	print(St2.fullname)

	#Day 3
	print('----------Day 3 --------')
	for i in range(3):
		St1.Codeing()

	St2.Codeing()
	St1.ShowExp()
	St2.ShowExp()

	#Day 4
	print('----------Day 4 --------')

	stp1 = SpecialStudent('Thomas', 'Edison', 'Hitler')
	allstudent.append(stp1)
	teacher1.AddStudent(stp1)
	print(stp1.fullname)
	print('คุณครูครับ ชอคะแนนฟรี 20 คะแนนได้ไหม')
	stp1.exp = 20
	stp1.Codeing()
	stp1.ShowExp()

	#Day 5
	print('----------Day 5 --------')
	print('นักเรียนกลีบบ้านกันยังไง')

	print(allstudent)
	for st in allstudent:
		print('ผม {} กลับ้านด้วย {} ครับ'.format(st.name, st.vehicle))
		print(isinstance(st,SpecialStudent))
		if isinstance(st,SpecialStudent):
			st.vehicle.SelfDriving(st)

	#Day 6
	print('----------Day 6 --------')


	teacher1.CheckStudent()
	teacher2.CheckStudent()

	print('รวมพลังของนักเรียน 2 คน', St1 + St2)
