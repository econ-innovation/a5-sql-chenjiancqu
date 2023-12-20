import sqlite3
import pandas as pd

# 读取文本文件
with open('/Users/chenjian/github/a5-sql-chenjiancqu/assignment_sql/address.txt', 'r') as file:
    addresses = [line.strip() for line in file.readlines()]

# 创建DataFrame
df = pd.DataFrame(addresses, columns=['address'])

# 创建SQLite数据库
conn = sqlite3.connect('address_database.db')

# 将DataFrame写入数据库
df.to_sql('addresses', conn, index=False, if_exists='replace')

# 关闭数据库连接
conn.close()
