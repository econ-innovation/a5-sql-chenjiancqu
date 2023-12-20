import sqlite3
import requests
from tqdm import tqdm


def query_geocode(address):
    url = 'https://restapi.amap.com/v3/assistant/inputtips?parameters'
    key = 'b4537c9eafbf7a8a9d489a12531499d0'
    parameters = {'key': key, 'keywords': address}

    # 发送 GET 请求
    response = requests.get(url, params=parameters)

    # 获取响应的内容
    data = response.json()
        
    location = data['tips'][0]['location']
    print(location)
        
    try:
        longitude, latitude = map(float, location.split(","))
    except:
        longitude, latitude = 0, 0  # location为空时，将经纬度设置为0
    return longitude, latitude

# 连接SQLite数据库
conn = sqlite3.connect('/Users/chenjian/github/a5-sql-chenjiancqu/address_database.db')
cursor = conn.cursor()

# 从数据库中读取地址
cursor.execute('SELECT address FROM addresses')
addresses = cursor.fetchall()

# 为了储存地理信息，创建一个新表
cursor.execute('CREATE TABLE IF NOT EXISTS address_info (address TEXT, longitude REAL, latitude REAL)')

# 对每个地址进行处理
for address in addresses:
    # 获取地址的地理信息
    print(address)
    longitude, latitude = query_geocode(address)
    
    # 将地址和地理信息储存进数据库
    cursor.execute('INSERT INTO address_info (address, longitude, latitude) VALUES (?, ?, ?)', (address[0], longitude, latitude))

# 提交更改并关闭数据库连接
conn.commit()
conn.close()
