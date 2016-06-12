' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import Stock, Stock_citic, Stock_tiger

from apis import Page, APIValueError

from decimal import *

@get('/')
def index(request):
	stocks = yield from Stock.findAll()
	return {
		'__template__': 'index.html',
		'stocks': stocks 
	}


@get('/api/stocks')
def api_get_stocks():
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
def api_stocks_page(*, page='1'):
	page_index = get_page_index(page)
	num = yield from Stock.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock.findAll(orderBy='occur_date desc', limit=(p.offset, p.limit))
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
def api_stocks_citic_page(*, page='1'):
	page_index = get_page_index(page)
	num = yield from Stock_citic.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock_citic.findAll(orderBy='occur_date desc', limit=(p.offset, p.limit))
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
def api_stocks_tiger_page(*, page='1'):
	page_index = get_page_index(page)
	num = yield from Stock_tiger.findNumber('count(id)')
	p = Page(num, page_index)
	if num == 0:
		return dict(page=p, stocks=())
	stocks = yield from Stock_tiger.findAll(orderBy='occur_date desc', limit=(p.offset, p.limit))
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
def manage_stocks(*, page='1'):
	return {
		'__template__': 'manage_stocks.html',
		'page_index': get_page_index(page)
	}


'''老虎记录查询'''
@get('/manage/stocks_tiger')
def manage_stocks_tiger(*, page='1'):
	return {
		'__template__': 'manage_stocks_tiger.html',
		'page_index': get_page_index(page)
	}

'''中信记录查询'''
@get('/manage/stocks_citic')
def manage_stocks_citic(*, page='1'):
	return {
		'__template__': 'manage_stocks_citic.html',
		'page_index': get_page_index(page)
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
		sum_stock['current_amount'] = sum_amount * -1
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
		sum_stock['current_amount'] = sum_amount * -1
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
	all_sum_stock['current_amount'] = "%.2f" % (sum_stock['current_amount'] + citic_temp_sum_stock)
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
