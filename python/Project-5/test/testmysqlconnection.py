import match
import pymysql
import pymysql.cursors


# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Anirud@10302025@$',
                             port= 3306,
                             database='sys',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "SELECT * from sys.chemistryquestions"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            #for match in matches:
            sql = "INSERT INTO sys.chemistryquestions (id, subjectName, questionText, answerOptions, chapterName) VALUES (1, 'Chemistry', '1. What is the SI unit of mass?', 'None', 'None')"
            cursor.execute(sql)
            connection.commit()


except Exception as e:
    print(f"An error occurred: {e}")

finally:
        cursor.close()
        connection.close()
