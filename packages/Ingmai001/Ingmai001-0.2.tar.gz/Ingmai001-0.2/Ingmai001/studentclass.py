# studentclass.py

class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		#Call Function
		self.AddExp(10)

	def Hello(self):
		print('สวัสดี ผมชื่อ{}'.format(self.name))	

	def Coding(self):
		print('{}:กำลังเขียนโปรแกรม...'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowExp(self):
		print('{} มี {} exp'.format(self.name,self.exp))
		print('- เรียนไป {} ครั้ง'.format(self.lesson))	

	def AddExp(self,score):
		self.exp += score # self.exp = self.exp + score
		self.lesson += 1


class SpecialStudent(Student):

	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddExp(self,score):
		self.exp += score * 3
		self.lesson += 1

	def AskExp(self,score=10):
		print('ครู ขอคะแนนพิเศษ {} exp'.format(score))
		self.AddExp(score)

if __name__ == '__main__': 

	print('======= 1 Jan 2021==========')
	student0 = SpecialStudent('Mark Zucherberg','Bill Gates')
	student0.ShowExp()
	student0.AskExp()

	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()

	print('-------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('======= 2 Jan 2021==========')
	print('-----ใครอยากเรียน coding?----(10 exp)---')
	student1.AddExp(10)

	print('======= 3 Jan 2021==========')
	student1.name= 'Albert Einstein'
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่')

	print(student1.name,student1.exp)
	print(student2.name,student2.exp)
