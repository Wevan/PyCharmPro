import xlrd
from xlwt import *
import pymysql
import xlsxwriter


# 创建xls文件
def createExcel():
    w = Workbook(encoding='utf-8')
    sheet1 = w.add_sheet('problem_sheet')
    row0 = [u'num', u'title', u'category', u'difficulty', u'answer', u'analysis', u'teacher', u'add_time', u'score', u'complete_time', u'status', u'direction_id', u'stage_id', u'course_id', u'days_id', u'gongsi_id', u'zhiwei_id', u'type', u'url', u'orderd']
    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    w.save('Problems.xls')
    print("模板创建成功，请于程序同级目录下查找使用")



def createTables():
    tname = input("请输入表名：\n")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS problems")
    while 1:
        sectionName = input("请输入属性名称\n")
        sectionType = input("请输入属性类型\n")
        sectionSize = input("请输入属性类型大小\n")
        # 使用预处理语句创建表
        sql = """CREATE TABLE %(tname) (
                 pid  INT (20) NOT NULL,
                 content  CHAR(50),
                 analysis CHAR(50),  
                 chapter CHAR(50),
                 tips CHAR(50),
                 answer CHAR(50),
                 course CHAR (50))""" % (tname)
    cursor.execute(sql)


def sonmenu():
    dbname = input("请输入已创建的数据库的名称：\n")

    dbuser = input("请输入mysql用户名：\n")

    dbpwd = input("请输入mysql密码：\n")

    global db
    db = pymysql.connect("193.112.6.35", dbuser, dbpwd, dbname, use_unicode=True, charset="utf8")
    # db = pymysql.connect("localhost", dbuser, dbpwd, dbname, use_unicode=True, charset="utf8")
    print("请将Excel复制到程序同级目录下，再进行以下选择\n")
    print("1.库中已经有表\n")
    print("2.库中需创建新表（暂不使用此功能）\n")
    a = input()
    if a == "1":
        insertData()
    elif a == "2":
        createTables()


def transferContent(content):
    if content is None:
        return None
    else:
        string = ""
        for c in content:
            if c == '"':
                string += '\\\"'
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string


def insertData():
    ename = input("请输入要导入的Excel文件名称：\n")
    workbook = xlrd.open_workbook(ename)
    print("导入全部sheet...\n")
    for i in workbook.sheet_names():
        print("表名====>>" + i + "/")
    print("\n")
    a = len(workbook.sheets())
    cursor = db.cursor()
    # 遍历sheetlist
    for j in range(0, a):
        sheet1 = workbook.sheet_by_index(j)
        print("打开了表" + sheet1.name + "\n")
        title = ""
        # 获取表头
        for l in range(0, int(sheet1.ncols)):
            if l == sheet1.ncols - 1:
                title += sheet1.cell_value(0, l)
                break
            title += sheet1.cell_value(0, l) + ","
        print("表头是"+title)
        # 遍历sheet
        for nrows_one in range(1, int(sheet1.nrows)):
            con = ""
            for s in range(0, int(sheet1.ncols)):
                try:
                    values = sheet1.cell_value(nrows_one, s)
                    if sheet1.cell_value(0, s) == "score" or sheet1.cell_value(0, s) == "complete_time":
                        try:
                            con = con + str(int(values)) + ","
                        except:
                            con = con + str(1)+","
                        continue
                    elif sheet1.cell_value(0, s) == "orderd":
                        try:
                            con = con + str(int(values))
                        except:
                            con = con + str(0)
                        continue
                    elif sheet1.cell_value(0, s) == "category"or sheet1.cell_value(0, s) == "difficulty"or sheet1.cell_value(0, s) == "status"or sheet1.cell_value(0, s) == "type":
                        try:
                            con = con + "'"+str(int(values))+"'"+","
                        except:
                            con = con + "'"+ str(0)+"'"+","
                        continue
                    values = transferContent(str(values))
                    if s == int(sheet1.ncols) - 1:
                        con = con + "'" + str(values) + "'"
                        break
                    con = con + "'" + str(values) + "',"
                except:
                    print("出问题的是" + str(s) + "," + str(values))
            sql = "insert into uek_evaluate_titles1(" + title + ") values(" + con + ")"
            # print("SQL语句：" + sql)
            # 将数据存入数据库
            try:
                # 使用 cursor() 方法创建一个游标对象 cursor
                cursor.execute(sql)
                db.commit()  # 事务提交
                print(str(nrows_one) + '行存入成功')
            except Exception as e:
                # 发生错误时回滚
                db.rollback()
                print(str(nrows_one) + "行错了")
                print(str(e))

    # 关闭数据库连接
    db.close()


def menu():
    print("自动导库\n")
    print("1.创建Excel数据模板\n")
    print("2.导入数据到MySQL数据库\n")
    a = input("选择功能：\n")

    if a == "1":
        createExcel();
    elif a == "2":
        sonmenu();


menu()


