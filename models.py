from peewee import *

db = PostgresqlDatabase(
    'tz_data', 
    host = 'localhost',
    port = '5432',
    user = 'saske',
    password = 'qwe123'
)

db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class Orders(BaseModel):
    order_number = IntegerField()
    price_dollar = IntegerField()
    price_rub = IntegerField(null=True)
    delivery_time = CharField()

db.create_tables([Orders])
db.close()
print('models Done!!!')