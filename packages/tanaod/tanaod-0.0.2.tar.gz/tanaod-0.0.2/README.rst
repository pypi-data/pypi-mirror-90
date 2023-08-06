(oop school) ไลบราลี่สำหรับใช้เรียน by TanAod
=============================================

PyPI: https://pypi.org/project/tanaod/

โปรแกรมนี้ใช้สำหรับเขียนโปรแกรมแบบ OOP

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install tanaod

วิธีใช้
~~~~~~~

[STEP 1] - เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

    from tanaod import Student,Tesla,SpecialStudent,Teacher
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

พัฒนาโดย: ตนุภัทร สถืตวรรธนะ FB:
https://www.facebook.com/tanupat.satitvattana/ IG: tan\_aod , a0d14
