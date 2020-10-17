# CrawlEconometricaEssay
## 功能
	自定义爬取期刊网站https://onlinelibrary.wiley.com/journal/14680262/上的期刊  
	
## 使用方法
	python main.py <command> [options]  
	其中<command>：  
	crawlHistory				爬取该期刊所有的历史文章  
	crawlLatest				爬取该期刊当前最新一期的文章  
	crawlSpecial				爬取该期刊某一特定期的文章  
	crawlSearch				爬取包含指定关键词的相关文章
	[options]  只能用在爬取特定期的文章（Crawlspecial）和包含指定关键词文章（crawlSearch）条件下，用来自定义爬取的时间(-y)和期数(-i)或者爬取包含自定义的关键词（-s)    


例1：用户向爬取最新一期的文章   
	代码：python main.py crawlLatest  


例2：用户想要爬取2015年第5期的全部文章   
	代码:python main.py crawlSpecial -y 2015 -i 5 


例2：用户想爬取关于关键词network的文章  
	代码：python main.py crawlSearch -s network  
