(MACOOP) สำหรับเรียนรู้พัฒนาระบบ
================================

โปรแกรมนี้ใช้ทดสอบระบบเท่านั้น!!

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install macoop

Day 0
=====

::

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

\`\`\`
