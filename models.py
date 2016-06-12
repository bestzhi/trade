import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField, DateTimeField

class Stock(Model):
	__table__ = 'stock'
	'''
	__fk_table__ = 'stock_type'
	__fk_field__ = 'type'
	__fk_table_field__ = 'name'
	'''
	id = IntegerField(primary_key=True)
	deal_num = IntegerField()
	type = StringField(ddl='varchar(45)')
	occur_date = DateTimeField()
	occur_amount = FloatField()
	balance = FloatField()
	stock_balance = IntegerField()
	stock_code = StringField(ddl='varchar(45)')
	deal_price = FloatField()
	stamp_tax = FloatField()
	transfer_fee = FloatField()
	other_fee = FloatField()
	commission = FloatField()
	charge_fee = FloatField()
	stock_name = StringField(ddl='varchar(45)')
	memo = StringField(ddl='varchar(45)')

class Stock_citic(Model):
	__table__ = 'stock_citic'
	'''
	__fk_table__ = 'stock_type'
	__fk_field__ = 'type'
	__fk_table_field__ = 'name'
	'''
	id = IntegerField(primary_key=True)
	deal_num = IntegerField()
	type = StringField(ddl='varchar(45)')
	occur_date = DateTimeField()
	occur_amount = FloatField()
	balance = FloatField()
	stock_balance = IntegerField()
	stock_code = StringField(ddl='varchar(45)')
	deal_price = FloatField()
	stamp_tax = FloatField()
	transfer_fee = FloatField()
	other_fee = FloatField()
	commission = FloatField()
	charge_fee = FloatField()
	stock_name = StringField(ddl='varchar(45)')
	memo = StringField(ddl='varchar(45)')


class Stock_tiger(Model):
	__table__ = 'stock_tiger'
	'''
	__fk_table__ = 'stock_type'
	__fk_field__ = 'type'
	__fk_table_field__ = 'name'
	'''
	id = IntegerField(primary_key=True)
	deal_num = IntegerField()
	type = StringField(ddl='varchar(45)')
	occur_date = DateTimeField()
	occur_amount = FloatField()
	balance = FloatField()
	stock_balance = IntegerField()
	stock_code = StringField(ddl='varchar(45)')
	deal_price = FloatField()
	commission = FloatField()


class Stock_type(Model):
	__table__ = 'stock_type'
	type = StringField(primary_key=True, ddl='varchar(45)')
	name = StringField(ddl='varchar(45)')

