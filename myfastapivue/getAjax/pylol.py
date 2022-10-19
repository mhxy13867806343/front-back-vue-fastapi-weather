import requests
import json
from sqlite3 import Error
import sqlite3
import xlwt
def heroIdbt(sheet):
    l = ['heroId', 'alias', 'attack', 'banAudio', 'camp', 'campId', 'changeLabel', 'couponPrice'
        , 'defense', 'difficulty', 'goldPrice', 'instance_id', 'isARAMweekfree', 'isWeekFree', 'ispermanentweekfree',
         'keywords',
         'magic', 'name', 'roles', 'selectAudio', 'title',
         ]
    for index, item in enumerate(l):
        sheet.write(0, index, item)
 # 数据库文件路径
db_file = '../dbbase/actlol.db'
# 连接数据库
conn = sqlite3.connect(db_file)
# 创建游标
cursor = conn.cursor()
def createLOL():
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?ts=2776676'
    data = requests.get(url)
    content = bytes(data.content).decode('UTF-8')
    jsonContent = json.loads(content)

    fileName = jsonContent['fileName']
    fileTime = jsonContent['fileTime']
    hero = jsonContent['hero']
    version = jsonContent['hero']
    total = 0
    xls =xlwt.Workbook()
    sheet = xls.add_sheet('lol')
    heroIdbt(sheet)
    for index,item in enumerate(hero):
        alias=item['alias']
        attack=item['attack']
        banAudio=item['banAudio']
        camp=item['camp']
        campId=item['campId']
        changeLabel=item['changeLabel']
        couponPrice=item['couponPrice']
        defense=item['defense']
        difficulty=item['difficulty']
        goldPrice=item['goldPrice']
        heroId=item['heroId']
        instance_id=item['instance_id']
        isARAMweekfree=item['isARAMweekfree']
        isWeekFree=item['isWeekFree']
        ispermanentweekfree=item['ispermanentweekfree']
        keywords=item['keywords']
        magic=item['magic']
        name=item['name']
        roles=item['roles']
        selectAudio=item['selectAudio']
        title=item['title']
        total = total + 1
        sheet.write(total, 0, heroId)
        sheet.write(total, 1, title)
        sheet.write(total,2,attack)
        sheet.write(total,3,banAudio)
        sheet.write(total,4,camp)
        sheet.write(total,5,campId)
        sheet.write(total,6,changeLabel)
        sheet.write(total,7,couponPrice)
        sheet.write(total,8,defense)
        sheet.write(total,9,difficulty)
        sheet.write(total,10,goldPrice)
        sheet.write(total,11,instance_id)
        sheet.write(total,12,isARAMweekfree)
        sheet.write(total,13,isWeekFree)
        sheet.write(total,14,ispermanentweekfree)
        sheet.write(total,15,keywords)
        sheet.write(total,16,magic)
        sheet.write(total,17,name)
        sheet.write(total,18,roles)
        sheet.write(total,19,selectAudio)
        sheet.write(total,20,alias)
    xls.save('lol.xls')


def actHref(num=1):
    url=f'https://game.gtimg.cn/images/lol/act/img/js/hero/{num}.js?ts=2776929'
    data = requests.get(url)
    content = bytes(data.content).decode('UTF-8')
    data = json.loads(content)
    return data
def select_connection(num=1):
    sql=f"SELECT * FROM actlol where fileName='{num}.js';"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    if(len(data)>0):
        return False
    else:
        return True
    cursor.close()
    conn.commit()
    conn.close()

def create_connection(num=1):
    type = select_connection(num)
    if (type):

        sql = """
                   CREATE TABLE   actlol(
                   fileName text,
                   fileTime text,
                   version text,
                   skins array,
                   spells array,
                   hero object
                   )
                   """
        try:
            cursor.execute(sql)
        except Error as e:
            print(e,'数据库创建失败')
        # 测试是否连接成功
        print('连接成功')
        data = actHref(num)
        fileName=data['fileName']
        fileTime=data['fileTime']
        version=data['version']
        hero=data['hero']
        l1=[]
        l2=[]
        for i,j in enumerate(data['skins']):
            l1.append(j)
        for i,j in enumerate(data['spells']):
            l2.append(j)
        sql = "INSERT INTO actlol(fileName,fileTime,version,skins,spells,hero) VALUES(?,?,?,?,?,?)"
        data=(fileName,fileTime,version,str(l1),str(l2),str(hero))
        cursor.execute(sql,data)
        conn.commit()

        # 关闭游标
        cursor.close()
        # # 关闭连接
        conn.close()
create_connection(4)