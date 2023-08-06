# -*- coding: utf-8 -*-

import tanaod.school
from tanaod.school import  Student , SpecialStudent
from tanaod.school import *

def Test():   
    '''
    นี่คือตัวอย่างการเขียนโปรแกรม จาก ลุงวิศวะกร
    st1 = school.Student('Albert','Einstein')
    print(st1)

    st2 = Student('bill','gates')
    print(st2)

    stp1 = SpecialStudent('t','e','p')

    teacher1 = Teacher('ada')
    print(teacher1.fullname)
    '''
    st1 = school.Student('Albert','Einstein')
    print(st1)

    st2 = Student('bill','gates')
    print(st2)

    stp1 = SpecialStudent('t','e','p')

    teacher1 = Teacher('ada')
    print(teacher1.fullname)

print(help(Test))