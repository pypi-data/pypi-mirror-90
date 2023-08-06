# -*- coding: utf-8 -*-
# school.py

class Student:
    def __init__(self,name,lastname):    
        self.name = name 
        self.lastname = lastname
        self.exp = 0
        self.lesson = 0
        self.vehicle = 'รถเมลล์'

    #@property ใส่เพื่อเวลาเรียกไม่ต้อง ใช้ () 
    @property
    def fullname(self):
        return '{} {}'.format(self.name,self.lastname)

    def Coding(self):
        self.AddExp()
        print('{} กำลังเรียนเขียนโปรแกรม...'.format(self.fullname))

    def Showexp(self):
        print('{} ได้คะแนน {} exp (เรียนไป {} ครั้ง )'.format(self.name , self.exp ,self.lesson))
    def AddExp(self):
        self.exp += 10
        self.lesson += 1
    def __str__(self):
        return self.fullname
    def __repr__(self):
        return self.fullname
    def __add__(self,other):
        return self.exp + other.exp

allstudent = [] 

class SpecialStudent(Student):
    def __init__(self,name,lastname,father):
        super().__init__(name,lastname)
        self.father = father
        self.vehicle = Tesla()
        print('รู้ไหมฉันลูกใคร.. พ่อฉันชื่อ {} '.format(self.father)) 
    def AddExp(self):
        self.exp += 30
        self.lesson += 2

class Tesla:
    def __init__(self):
        self.model = 'Tesla Modle S'
    def SelfDriving(self,st):
        return print('ระบบอัตโนมัตกำลังทำงาน...กำลังพาคุณ {} กลับบ้าน!'.format(st.name))
    def __str__(self):
        return self.model

class Teacher:
    def __init__(self,fullname): 
        self.fullname = fullname
        self.students = []
    def CheckStudent(self):
        for i,st in enumerate(self.students):
            print('----นักเรียนของ({})'.format(self.fullname))
            print('{}--->{} [ {} exp[เรียนไป {} ครั้ง]]'.format(i+1,st.fullname,st.exp,st.lesson))
    def Addstudent(self,st):
        self.students.append(st)


# print('FILE',__name__)
if __name__ == '__main__':
    print(__name__)


    #day0
    print('---------day0---------')
    allstudent = []
    teacher1 = Teacher('ada lovelace')
    teacher2 = Teacher('bill gate')
    print(teacher1.students)

    #day1
    print('--------day1--------')
    st1 = Student('Albert','Einstein')
    allstudent.append(st1)
    print(st1.fullname)
    teacher2.Addstudent(st1)


    #day2
    print('--------day2--------')
    st2 = Student('steve','jobs')
    allstudent.append(st2)
    print(st2.fullname)
    teacher2.Addstudent(st2)

    #day3
    print('--------day3--------')
    for i in range(3):
        st1.Coding()

    st2.Coding()
    st1.Showexp()
    st2.Showexp()

    #day4
    print('-------day4---------')
    stp1 = SpecialStudent('thomas' , 'Edison' ,'Hitler')
    allstudent.append(stp1)
    teacher1.Addstudent(st1)
    print(stp1.fullname)
    stp1.exp = 20
    stp1.Coding()
    stp1.Showexp() 

    #day5
    print('-------day5---------')
    print('กลับบ้านยังไง')

    print(allstudent)
    for st in allstudent:
        print('ผม {} กลับด้วย {} ครับ'.format(st.name,st.vehicle))
        if isinstance(st,SpecialStudent):
            st.vehicle.SelfDriving(st)

    #day6
    print('---------day6--------')
    teacher1.CheckStudent()
    teacher2.CheckStudent()

    print('รวมพลังของนักเรียน2คน',st1 + st2)
