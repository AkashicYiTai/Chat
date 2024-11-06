mysql_name="akashic"
mysql_passwd="123"
port="localhost:3306"
database="user_db"

SYNC_DATABASE_URL = f'mysql+pymysql://{mysql_name}:{mysql_passwd}@{port}/{database}'
ASYNC_DATABASE_URL = f'mysql+aiomysql://{mysql_name}:{mysql_passwd}@{port}/{database}'
