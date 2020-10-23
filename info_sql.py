import csv

outputSQL_file = "courseInfo.sql"
with open("course_data.csv") as fin:
    reader = csv.reader(fin)
    data = [row for row in reader]

def produce_sql():
    sqlStr = "INSERT INTO course_info VALUES "
    for row in data:
        sqlStr += "('{}','{}',{},'{}'),".format(row[0], row[1], row[2], row[3])
    sqlStr = sqlStr[:-1]
    with open(outputSQL_file, "w") as f:
        f.write(sqlStr)

produce_sql()