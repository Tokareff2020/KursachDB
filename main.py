from database import DatabaseController

if __name__ == '__main__':
    controller = DatabaseController()
    result = controller.execute_fetchall('select * from teachers;')


