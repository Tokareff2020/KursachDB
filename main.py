from database import DatabaseController, SubjectController, TeachersController

if __name__ == '__main__':
    controller = DatabaseController()
    subject_controller = SubjectController()
    teacher_controller = TeachersController()
    print(f'Создана запись в таблице teachers: ' + str(teacher_controller.create({'name': 'Алексей',
                                                                                  'surname': 'Абросимов',
                                                                                  'patronymic': 'Дмитриевич'})[-1]))
    print(f'Создана запись в таблице subjects: ' + str(
        teacher_controller.connect_with_subject({'teacher_id': 32, 'subject_id': 7})))
    print(f'Проверка изменений. Новые предметы у преподавателя :' + str(teacher_controller.read(32)))
    print(f'Проверка изменений. Новые значения у преподавателя :' +
          str(teacher_controller.update({'id': 32,
                                         'name': 'Максим',
                                         'surname': 'Бермецуцкий',
                                         'patronymic': 'Антонович'})))
    print(f'Удаление записи в таблице teachers. Последняя запись: ' + str(teacher_controller.delete(32)[-1]))

    print(f'Создана запись в таблице subject_info: ' + str(subject_controller.create({'name': 'Математический анализ',
                                                                                      'classes_type': 'Лекция',
                                                                                      'planned_workload': 40,
                                                                                      'actual_workload': 48})))
    print(f'Создана запись в таблице subjects: ' + str(subject_controller.connect_with_teacher({'teacher_id': 29,
                                                                                                'subject_id': 31})))
    print(f'Проверка изменений. Новый предмет :' + str(subject_controller.read(31)))
    print(f'Проверка изменений. Новые значения у предмета :' +
          str(subject_controller.update({'id': 31,
                                         'name': 'Математика',
                                         'classes_type': 'Лабораторная работа',
                                         'planned_workload': 62,
                                         'actual_workload': 64})))
    print(f'Удаление записи в таблице subject_info. Последняя запись: ' + str(subject_controller.delete(31)[-1]))
