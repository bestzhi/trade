' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from aiohttp import web

from coroweb import get, post

from models import Stock, Stock_citic, Stock_tiger, User

from apis import Page, APIValueError, APIPermissionError

from config import configs

from decimal import *

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None:
        raise APIPermissionError()

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        stock = yield from Stock.find('1')
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
def index(request):
	#stocks = yield from Stock.findAll()
	return {
		'__template__': 'index.html' 
	}


@get('/api/stocks')
def api_get_stocks(request):
    stocks = yield from Stock.findAll(orderBy='id desc')
    for s in stocks:
        s.occur_date = str(s.occur_date)
    return dict(stocks=stocks)





'''添加申万交易记录页面'''
@get('/manage/create_trade_record')
def manage_save_trade_record():
	return {
		'__template__': 'save_trade_record.html',
		'action': '/api/save_trade_record'
	}	


'''添加申万交易记录'''
@post('/api/save_trade_record')
def api_save_trade_record(request, *, type, occur_date, occur_amount, balance, **kw):
	
	if not type or not type.strip():
		raise APIValueError('type', 'type cannot be empty.')
	if not occur_amount or not occur_amount.strip():
		raise APIValueError('occur_amount', 'occur_amount cannot be empty')

	if 'charge_fee' in kw:
		charge_fee = kw['charge_fee']
	else:
		charge_fee = 0
	if 'stamp_tax' in kw:
		stamp_tax = kw['stamp_tax']
	else:
		stamp_tax = 0
	if 'transfer_fee' in kw:
		transfer_fee = kw['transfer_fee']
	else:
		transfer_fee = 0
	if 'commission' in kw:
		commission = kw['commission']
	else:
		commission = 0
	if 'stock_balance' in kw:
		stock_balance = kw['stock_balance']
	else:
		stock_balance = 0
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
	else:
		stock_code = ''
	if 'deal_num' in kw:
		deal_num = kw['deal_num']
	else:
		deal_num = 0
	if 'deal_price' in kw:
		deal_price = kw['deal_price']
	else:
		deal_price = 0
	stock = Stock(type=type.strip(), occur_date=occur_date, occur_amount=occur_amount, balance=balance, stock_balance=stock_balance, stock_code=stock_code,
		deal_num=deal_num, deal_price=deal_price, stamp_tax=stamp_tax, transfer_fee=transfer_fee, commission=commission, charge_fee=charge_fee)
	yield from stock.save()
	return stock


'''添加中信交易记录页面'''
@get('/manage/create_citic_trade_record')
def manage_save_citic_trade_record():
	return {
		'__template__': 'save_citic_trade_record.html',
		'action': '/api/save_citic_trade_record'
	}	


'''添加中信交易记录'''
@post('/api/save_citic_trade_record')
def api_save_citic_trade_record(request, *, type, occur_date, occur_amount, balance, **kw):

	if not type or not type.strip():
		raise APIValueError('type', 'type cannot be empty.')
	if not occur_amount or not occur_amount.strip():
		raise APIValueError('occur_amount', 'occur_amount cannot be empty')
	if 'stamp_tax' in kw:
		stamp_tax = kw['stamp_tax']
	else:
		stamp_tax = 0
	if 'transfer_fee' in kw:
		transfer_fee = kw['transfer_fee']
	else:
		transfer_fee = 0
	if 'commission' in kw:
		commission = kw['commission']
	else:
		commission = 0
	if 'stock_balance' in kw:
		stock_balance = kw['stock_balance']
	else:
		stock_balance = 0
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
	else:
		stock_code = ''
	if 'deal_num' in kw:
		deal_num = kw['deal_num']
	else:
		deal_num = 0
	if 'deal_price' in kw:
		deal_price = kw['deal_price']
	else:
		deal_price = 0
	stock = Stock_citic(type=type.strip(), occur_date=occur_date, occur_amount=occur_amount, balance=balance, stock_balance=stock_balance, stock_code=stock_code,
		deal_num=deal_num, deal_price=deal_price, stamp_tax=stamp_tax, transfer_fee=transfer_fee, commission=commission)
	yield from stock.save()
	return stock


'''添加老虎交易记录页面'''
@get('/manage/create_tiger_trade_record')
def manage_save_tiger_trade_record():
	return {
		'__template__': 'save_tiger_trade_record.html',
		'action': '/api/save_tiger_trade_record'
	}	


'''添加老虎交易记录'''
@post('/api/save_tiger_trade_record')
def api_save_tiger_trade_record(request, *, type, occur_date, **kw):

	if not type or not type.strip():
		raise APIValueError('type', 'type cannot be empty.')
	
	pre_stock = yield from Stock_tiger.findAll(orderBy='id desc', limit=1)
	
	if type == 'SA' or type == 'T' or type == 'I' or type == 'D':
		if 'occur_amount' in kw:
			occur_amount = kw['occur_amount']
		else:
			occur_amount = 0
		if 'commission' in kw:
			commission = kw['commission']
		else:
			commission = 0
		stock_balance = 0
		if 'stock_code' in kw:
			stock_code = kw['stock_code']
		else:
			stock_code = ''
		deal_num = 0
		deal_price = 0
	else:
		if 'commission' in kw:
			commission = kw['commission']
		else:
			commission = 0
		if 'stock_balance' in kw:
			stock_balance = kw['stock_balance']
		else:
			stock_balance = 0
		if 'stock_code' in kw:
			stock_code = kw['stock_code']
		else:
			stock_code = ''
		if 'deal_num' in kw:
			deal_num = kw['deal_num']
		else:
			deal_num = 0
		if 'deal_price' in kw:
			deal_price = kw['deal_price']
		else:
			deal_price = 0
		occur_amount = str(Decimal(deal_price) * Decimal(deal_num) * Decimal(-1))

	stock = Stock_tiger(type=type.strip(), occur_date=occur_date, occur_amount=occur_amount, 
		balance=str(Decimal(pre_stock[0].balance) + Decimal(occur_amount) + Decimal(commission)), stock_balance=stock_balance, stock_code=stock_code,
		deal_num=deal_num, deal_price=deal_price, commission=commission)
	yield from stock.save()
	return stock


def get_page_index(page_str):
	p = 1
	try:
		p = int(page_str)
	except ValueError as e:
		pass
	if p < 1:
		p = 1
	return p


'''申万记录列表返回json'''
@get('/api/stocks_page')
def api_stocks_page(*, page='1', **kw):
	page_index = get_page_index(page)
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
		if(stock_code != '' and stock_code != '0'):
			where_clause = 'stock_code = \'' + stock_code + '\''
		else:
			where_clause = '1=1'
	else:
		where_clause = '1=1'
	num = yield from Stock.findNumber('count(id)', where=where_clause)
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock.findAll(where=where_clause, orderBy='occur_date desc, id desc', limit=(p.offset, p.limit))
	for s in stocks:
		s.occur_date = str(s.occur_date)[0:10]
		s.stamp_tax = "%.2f" % (s.stamp_tax + s.transfer_fee + s.other_fee + s.commission + s.charge_fee)
		if s.type == 'T':
			s.type = '取出'
		elif s.type == 'SA':
			s.type = '存入'
		elif s.type == 'AB':
			s.type = '申购付款'
		elif s.type == 'AS':
			s.type = '申购退款'
		elif s.type == 'B':
			s.type = '买入'
		elif s.type == 'D':
			s.type = '红利'
		elif s.type == 'FP':
			s.type = '货币基金收益'
		elif s.type == 'I':
			s.type = '利息'
		elif s.type == 'S':
			s.type = '卖出'
		elif s.type == 'TD':
			s.type = '红利税'
	return dict(page=p, stocks=stocks)


'''中信记录列表返回json'''
@get('/api/stocks_citic_page')
def api_stocks_citic_page(*, page='1', **kw):
	page_index = get_page_index(page)
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
		if(stock_code != '' and stock_code != '0'):
			where_clause = 'stock_code = \'' + stock_code + '\''
		else:
			where_clause = '1=1'
	else:
		where_clause = '1=1'
	num = yield from Stock_citic.findNumber('count(id)', where=where_clause)
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock_citic.findAll(where=where_clause, orderBy='occur_date desc, id desc', limit=(p.offset, p.limit))
	for s in stocks:
		s.occur_date = str(s.occur_date)[0:10]
		s.stamp_tax = "%.2f" % (s.stamp_tax + s.transfer_fee + s.other_fee + s.commission + s.charge_fee)
		if s.type == 'T':
			s.type = '取出'
		elif s.type == 'SA':
			s.type = '存入'
		elif s.type == 'AB':
			s.type = '申购付款'
		elif s.type == 'AS':
			s.type = '申购退款'
		elif s.type == 'B':
			s.type = '买入'
		elif s.type == 'D':
			s.type = '红利'
		elif s.type == 'FP':
			s.type = '货币基金收益'
		elif s.type == 'I':
			s.type = '利息'
		elif s.type == 'S':
			s.type = '卖出'
		elif s.type == 'TD':
			s.type = '红利税'
	return dict(page=p, stocks=stocks)


'''老虎记录列表返回json'''
@get('/api/stocks_tiger_page')
def api_stocks_tiger_page(*, page='1', **kw):
	page_index = get_page_index(page)
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
		if(stock_code != '' and stock_code != '0'):
			where_clause = 'stock_code = \'' + stock_code + '\''
		else:
			where_clause = '1=1'
	else:
		where_clause = '1=1'
	num = yield from Stock_tiger.findNumber('count(id)', where=where_clause)
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock_tiger.findAll(where=where_clause, orderBy='occur_date desc, id desc', limit=(p.offset, p.limit))
	for s in stocks:
		s.occur_date = str(s.occur_date)[0:10]
		s.deal_price = str(s.deal_price)
		s.commission = str(s.commission)
		s.occur_amount = str(s.occur_amount)
		s.balance = str(s.balance)
		if s.type == 'T':
			s.type = '取出'
		elif s.type == 'SA':
			s.type = '存入'
		elif s.type == 'AB':
			s.type = '申购付款'
		elif s.type == 'AS':
			s.type = '申购退款'
		elif s.type == 'B':
			s.type = '买入'
		elif s.type == 'D':
			s.type = '红利'
		elif s.type == 'FP':
			s.type = '货币基金收益'
		elif s.type == 'I':
			s.type = '利息'
		elif s.type == 'S':
			s.type = '卖出'
		elif s.type == 'TD':
			s.type = '红利税'
	return dict(page=p, stocks=stocks)


'''申万记录查询'''
@get('/manage/stocks')
def manage_stocks(*, page='1', **kw):
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
	else:
		stock_code = '0'
	return {
		'__template__': 'manage_stocks.html',
		'page_index': get_page_index(page),
		'stock_code': stock_code
	}


'''老虎记录查询'''
@get('/manage/stocks_tiger')
def manage_stocks_tiger(*, page='1', **kw):
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
	else:
		stock_code = '0'
	return {
		'__template__': 'manage_stocks_tiger.html',
		'page_index': get_page_index(page),
		'stock_code': stock_code
	}

'''中信记录查询'''
@get('/manage/stocks_citic')
def manage_stocks_citic(*, page='1', **kw):
	if 'stock_code' in kw:
		stock_code = kw['stock_code']
	else:
		stock_code = '0'
	return {
		'__template__': 'manage_stocks_citic.html',
		'page_index': get_page_index(page),
		'stock_code': stock_code
	}


'''申万投资组合查询页面'''
@get('/manage/investment_portfolio')
def manage_portfolio():
	return {
		'__template__': 'investment_portfolio.html'
	}


'''申万投资组合查询，返回json'''
@get('/api/invest_portfolio')
def api_invest_portfolio():
	
	stocks = yield from Stock.findInvestment(tableName='stock')
	sum_amount = 0
	if len(stocks) > 0:
		for s in stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * -1.0) 
			s['current_num'] = "%.0f" % s['current_num']
		
		sum_stock = dict()
		sum_stock['stock_code'] = 'Total'
		sum_stock['current_num'] = '----'
		sum_stock['current_price'] = '----'
		sum_stock['current_amount'] = "%.2f" % (sum_amount * -1)
		stocks.append(sum_stock)

	return dict(stocks=stocks)



'''中信投资组合查询页面'''
@get('/manage/investment_portfolio_citic')
def manage_portfolio_citic():
	return {
		'__template__': 'investment_portfolio_citic.html'
	}


'''中信投资组合查询，返回json'''
@get('/api/invest_portfolio_citic')
def api_invest_portfolio_citic():
	
	stocks = yield from Stock_citic.findInvestment(tableName='stock_citic')
	sum_amount = 0
	if len(stocks) > 0:
		for s in stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * -1.0) 
			s['current_num'] = "%.0f" % s['current_num']
		
		sum_stock = dict()
		sum_stock['stock_code'] = 'Total'
		sum_stock['current_num'] = '----'
		sum_stock['current_price'] = '----'
		sum_stock['current_amount'] = "%.2f" % (sum_amount * -1)
		stocks.append(sum_stock)

	return dict(stocks=stocks)


'''老虎投资组合查询页面'''
@get('/manage/investment_portfolio_tiger')
def manage_portfolio_tiger():
	return {
		'__template__': 'investment_portfolio_tiger.html'
	}


'''老虎投资组合查询，返回json'''
@get('/api/invest_portfolio_tiger')
def api_invest_portfolio_tiger():
	
	stocks = yield from Stock_tiger.findInvestment(tableName='stock_tiger')
	sum_amount = 0
	if len(stocks) > 0:
		for s in stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * Decimal(-1.0)) 
			s['current_num'] = "%.0f" % s['current_num']
		
		sum_stock = dict()
		sum_stock['stock_code'] = 'Total'
		sum_stock['current_num'] = '----'
		sum_stock['current_price'] = '----'
		sum_stock['current_amount'] = str(sum_amount * -1)
		stocks.append(sum_stock)

	return dict(stocks=stocks)


'''全部投资组合查询页面'''
@get('/manage/investment_portfolio_all')
def manage_portfolio_all():
	return {
		'__template__': 'investment_portfolio_all.html'
	}


'''全部投资组合查询，返回json'''
@get('/api/invest_portfolio_all')
def api_invest_portfolio_all():
	
	all_stocks = []
	'申万组合'
	stocks = yield from Stock.findInvestment(tableName='stock')
	sum_amount = 0
	if len(stocks) > 0:
		for s in stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * -1.0) 
			s['current_num'] = "%.0f" % s['current_num']
	
		sum_stock = dict()
		sum_stock['stock_code'] = '申万总计'
		sum_stock['current_num'] = '--￥--'
		
		temp_sum_stock = sum_amount * -1
		
		sum_stock['current_amount'] = "%.2f" % temp_sum_stock
		stocks.append(sum_stock)

		split_stock = dict()
		split_stock['stock_code'] = ''
		split_stock['current_num'] = ''
		split_stock['current_amount'] = ''
		stocks.append(split_stock)

		all_stocks.append(sum_stock)

	'中信组合'
	citic_stocks = yield from Stock_citic.findInvestment(tableName='stock_citic')
	sum_amount = 0
	if len(citic_stocks) > 0:
		for s in citic_stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * -1.0) 
			s['current_num'] = "%.0f" % s['current_num']
	
	
		citic_sum_stock = dict()
		citic_sum_stock['stock_code'] = '中信总计'
		citic_sum_stock['current_num'] = '--￥--'
		
		citic_temp_sum_stock = sum_amount * -1
		citic_sum_stock['current_amount'] = "%.2f" % citic_temp_sum_stock
		citic_stocks.append(citic_sum_stock)

		for s in citic_stocks:
			stocks.append(s)

		stocks.append(split_stock)

		all_stocks.append(citic_sum_stock)

	all_sum_stock = dict()
	all_sum_stock['stock_code'] = 'A股总计'
	all_sum_stock['current_num'] = '--￥--'
	all_sum_stock['current_amount'] = "%.2f" % (temp_sum_stock + citic_temp_sum_stock)
	stocks.append(all_sum_stock)

	stocks.append(split_stock)

	all_stocks.append(all_sum_stock)

	'老虎组合'
	tiger_stocks = yield from Stock_tiger.findInvestment(tableName='stock_tiger')
	sum_amount = 0
	if len(tiger_stocks) > 0:
		for s in tiger_stocks:
			sum_amount += s['current_amount']
			s['current_amount'] = "%.2f" % (s['current_amount'] * Decimal(-1.0)) 
			s['current_num'] = "%.0f" % s['current_num']
	
		tiger_sum_stock = dict()
		tiger_sum_stock['stock_code'] = '老虎总计'
		tiger_sum_stock['current_num'] = '---$---'
		tiger_sum_stock['current_amount'] = str(sum_amount * -1)
		tiger_stocks.append(tiger_sum_stock)

		for s in tiger_stocks:
			stocks.append(s)

		all_stocks.append(tiger_sum_stock)

	'查询总计stock=all_stocks,查询明细stocks=stocks'
	return dict(stocks=all_stocks)
	


'''资金查询，返回json'''
@get('/api/fund_all')
def api_fund_all():
	
	fund = yield from Stock.findFund(tableName='stock')
	fund[0]['broker'] = '申万宏源'
	fund[0]['currency'] = '￥'
	citic_fund = yield from Stock_citic.findFund(tableName='stock_citic')
	citic_fund[0]['broker'] = '中信证券'
	citic_fund[0]['currency'] = '￥'
	fund.append(citic_fund[0])

	a_fund = dict()
	a_fund['broker'] = 'A股总计'
	a_fund['currency'] = '￥'
	a_fund['sum_amount'] = fund[0]['sum_amount'] + citic_fund[0]['sum_amount']

	fund.append(a_fund)

	tiger_fund = yield from Stock_tiger.findFund(tableName='stock_tiger')
	tiger_fund[0]['sum_amount'] = '%.2f' % tiger_fund[0]['sum_amount']
	tiger_fund[0]['broker'] = '老虎证券'
	tiger_fund[0]['currency'] = '$'
	fund.append(tiger_fund[0])
	
	return dict(funds=fund)



'''全部资金查询页面'''
@get('/manage/fund_all')
def manage_fund_all():
	return {
		'__template__': 'fund_all.html'
	}


'''申万盈亏查询，返回json'''
@get('/api/profit')
def api_profit():

	stocks = yield from Stock.findProfit(tableName='stock')
	total_amount = 0

	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']
		
	t_stock = dict()
	t_stock['stock_code'] = '总计'
	t_stock['sum_amount'] = total_amount
	stocks.append(t_stock)

	return dict(stocks=stocks)

'''申万盈亏查询页面'''
@get('/manage/profit')
def manage_profit():
	return {
		'__template__': 'profit.html'
	}


'''中信盈亏查询，返回json'''
@get('/api/profit_citic')
def api_profit_citic():

	total_amount = 0
	stocks = yield from Stock_citic.findProfit(tableName='stock_citic')
	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']
	
	t_stock = dict()
	t_stock['stock_code'] = '总计'
	t_stock['sum_amount'] = '%.2f' % total_amount
	stocks.append(t_stock)
	return dict(stocks=stocks)

'''中信盈亏查询页面'''
@get('/manage/profit_citic')
def manage_profit_citic():
	return {
		'__template__': 'profit_citic.html'
	}


'''老虎盈亏查询，返回json'''
@get('/api/profit_tiger')
def api_profit_tiger():

	total_amount = 0
	stocks = yield from Stock_tiger.findProfitWithCommission(tableName='stock_tiger')
	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']

	t_stock = dict()
	t_stock['stock_code'] = '总计'
	t_stock['sum_amount'] = '%.2f' % total_amount
	stocks.append(t_stock)
	return dict(stocks=stocks)

'''老虎盈亏查询页面'''
@get('/manage/profit_tiger')
def manage_profit_tiger():
	return {
		'__template__': 'profit_tiger.html'
	}


'''全部盈亏查询，返回json'''
@get('/api/profit_all')
def api_profit_all():

	total_amount = 0
	all_stocks = []

	stocks = yield from Stock.findProfit(tableName='stock')

	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']
		
	s_stock = dict()
	s_stock['stock_code'] = '申万总计'
	s_stock['sum_amount'] = total_amount
	all_stocks.append(s_stock)

	stocks = yield from Stock_citic.findProfit(tableName='stock_citic')
	total_amount = 0
	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']
	
	z_stock = dict()
	z_stock['stock_code'] = '中信总计'
	z_stock['sum_amount'] = '%.2f' % total_amount
	all_stocks.append(z_stock)

	a_stock = dict()
	a_stock['stock_code'] = 'A股总计'
	a_stock['sum_amount'] = '%.2f' % (s_stock['sum_amount'] + total_amount)
	all_stocks.append(a_stock)
	
	stocks = yield from Stock_tiger.findProfitWithCommission(tableName='stock_tiger')
	total_amount = 0
	for s in stocks:
		total_amount += s['sum_amount']
		s['sum_amount'] = '%.2f' % s['sum_amount']
		s['sum_num'] = '%.0f' % s['sum_num']

	t_stock = dict()
	t_stock['stock_code'] = '老虎总计'
	t_stock['sum_amount'] = '%.2f' % total_amount
	all_stocks.append(t_stock)

	return dict(stocks=all_stocks)

'''全部盈亏查询页面'''
@get('/manage/profit_all')
def manage_profit_all():
	return {
		'__template__': 'profit_all.html'
	}

'''历史收益'''
@get('/api/old_profit_citic')
def api_old_profit_citic():

	stocks = yield from Stock_citic.findProfitWithOldProfit(tableName='stock_citic', broker='citic')
	return dict(stocks=stocks)


@get('/manage/old_profit_citic')
def manage_old_profit_citic():
	return {
		'__template__': 'old_profit_citic.html'
	}


@get('/api/old_profit')
def api_old_profit():

	stocks = yield from Stock.findProfitWithOldProfit(tableName='stock', broker='swhy')
	return dict(stocks=stocks)


@get('/manage/old_profit')
def manage_old_profit():
	return {
		'__template__': 'old_profit.html'
	}


@get('/api/old_profit_tiger')
def api_old_profit_tiger():

	stocks = yield from Stock_tiger.findProfitWithOldProfit(tableName='stock_tiger', broker='tiger')
	for s in stocks:
		s['sum_amount'] = '%.2f' % s['sum_amount']
	return dict(stocks=stocks)


@get('/manage/old_profit_tiger')
def manage_old_profit_tiger():
	return {
		'__template__': 'old_profit_tiger.html'
	}

'''当前组合'''
@get('/api/current_investment_citic')
def api_current_investment_citic():

	stocks = yield from Stock_citic.findCurrentInvestment(tableName='stock_citic', broker='citic')
	for s in stocks:
		s['current_price'] = '%.2f' % s['current_price']
		s['current_num'] = '%.2f' % s['current_num']
		s['current_amount'] = '%.2f' % s['current_amount']
	return dict(stocks=stocks)


@get('/manage/current_investment_citic')
def manage_current_investment_citic():
	return {
		'__template__': 'current_investment_citic.html'
	}


@get('/api/current_investment')
def api_current_investment():

	stocks = yield from Stock.findCurrentInvestment(tableName='stock', broker='swhy')
	for s in stocks:
		s['current_price'] = '%.2f' % s['current_price']
		s['current_num'] = '%.2f' % s['current_num']
		s['current_amount'] = '%.2f' % s['current_amount']
	return dict(stocks=stocks)


@get('/manage/current_investment')
def manage_current_investment():
	return {
		'__template__': 'current_investment.html'
	}

@get('/manage/current_investment_tiger')
def manage_current_investment_tiger():
	return {
		'__template__': 'current_investment_tiger.html'
	}

@get('/api/current_investment_tiger')
def api_current_investment_tiger():

	stocks = yield from Stock_tiger.findCurrentInvestment(tableName='stock_tiger', broker='tiger')
	for s in stocks:
		s['current_price'] = '%.2f' % s['current_price']
		s['current_num'] = '%.2f' % s['current_num']
		s['current_amount'] = '%.2f' % s['current_amount']
	return dict(stocks=stocks)


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@post('/authenticate')
def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
	# check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    logging.info('sha1 ' + sha1.hexdigest())
    logging.info('passwd ' + user.passwd)
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 计算加密cookie:
def user2cookie(user, max_age):
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)
