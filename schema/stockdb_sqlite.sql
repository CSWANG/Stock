create table daily_quotes_ALLEN (
	stock_date varchar(8) not null,
	security_code varchar(10) not null,
	stock_name varchar(20),
	trading_volume int,
	trans_amount int,
	trading_value int,
	open_price decimal(5,2),
	highest_price decimal(5,2),
	lowest_price decimal(5,2),
	closing_price decimal(5,2),
	dir char(1),
	change decimal(5,2),
	last_best_bid_price decimal(5,2),
	last_best_bid_volume int,
	last_best_ask_price decimal(5,2),
	last_best_ask_volume int,
	price_earning_ratio decimal(5,2),
	constraint daily_quotes_pk primary key (securitycode)
);

create index sqlite_autoindex_daily_quotes_1_ALLEN on daily_quotes (stockdate,securitycode);

CREATE TABLE dailyQuotes (
	StockDate VARCHAR(8) NOT NULL,
	SecurityCode VARCHAR(10) NOT NULL,
	StockName VARCHAR(20),
	TradingVolume INT,
	TransAmount INT,
	TradingValue INT,
	OpenPrice DECIMAL(5,2),
	HighestPrice DECIMAL(5,2),
	LowestPrice DECIMAL(5,2),
	ClosingPrice DECIMAL(5,2),
	Dir CHAR(1),
	"Change" DECIMAL(5,2),
	LastBestBidPrice DECIMAL(5,2),
	LastBestBidVolume INT,
	LastBestAskPrice DECIMAL(5,2),
	LastBestAskVolume INT,
	PriceEarningRatio DECIMAL(5,2),
	CONSTRAINT DAILYQUOTES_PK PRIMARY KEY (SecurityCode)
);

CREATE INDEX sqlite_autoindex_dailyQuotes_1 ON dailyQuotes (StockDate,SecurityCode);
