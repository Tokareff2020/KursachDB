from database import DatabaseController, SubjectController, TeachersController

if __name__ == '__main__':
    controller = DatabaseController()
    result = controller.execute_fetchall('select * from teachers;')
    subject_controller = SubjectController()
    teacher_controller = TeachersController()
    print(teacher_controller.create({'name': 'Алексей',
                                     'surname': 'Абросимов',
                                     'patronymic': 'Дмитриевич'})[-1])
    print(teacher_controller.connect_with_subject({'teacher_id': 32, 'subject_id': 7}))
    print(teacher_controller.read(32))
    print(teacher_controller.update({'id': 32,
                                     'name': 'Максим',
                                     'surname': 'Бермецуцкий',
                                     'patronymic': 'Антонович'}))
    print(teacher_controller.delete(32))


