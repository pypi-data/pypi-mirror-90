# student class

class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		# Call Function
		self.AddEXP(10)

	def Hello(self):
		print('Hello ผมชื่อ {} '.format(self.name))

	def Coding(self):
		print('{}: กำลังเขียนโปรแกรม'.format(self.name))
		self.exp += 5
		self.lesson +=1

	def ShowEXP(self):
		print('-{} มีประสบการณ์ {} EXP'.format(self.name,self.exp))
		print('-เรียนไปแล้ว {} ครั้ง-'.format(self.lesson))

	def AddEXP(self,score):
		self.exp += score
		self.lesson += 1 

class Specialstudent(Student):                    # มีการ สืบทอด Class จาก Class Student
	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia =['Bill Gate','Donald Trump','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):
		self.exp += (score*3)
		self.lesson += 1

	def AskEXP(self,score=10):
		print('ครู!! ขอคะแนนพิเศษให้ผมสัก {} EXP'.format(score))
		self.AddEXP(score)


# print(__name__) # เป็นการเช็กว่าอยู่ในไฟล์ main


#ถ้าภูก import เข้าไปใน File อื่นจะไม่ run
if __name__ == '__main__':
	
# เป็นการเช็กว่าอยู่ใน studentclass.py จริงๆ
	print('========2021,1 Jan========')
	student0 =Specialstudent('Mark','Bill Gate')
	student0.AskEXP()
	student0.ShowEXP()

	student1 = Student('Albert') #Object
	print(student1.name)
	student1.Hello()
	print('-----------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()


	print('========2021,2 Jan========')
	print('--------ใครอยากเรียน coding บ้าง?----(10 xp)----')
	student1.AddEXP(10)

	print('========2021,3 Jan========')
	student1.name = 'Albert Einstein'
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')
	print(student1.name,student1.exp)
	print(student2.name,student2.exp)

	print('========2021,4 Jan========')
	for i in range(5):
		student2.Coding()
	student0.ShowEXP()
	student1.ShowEXP()
	student2.ShowEXP()
