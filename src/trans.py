#-*-encoding:utf-8-*-

from googletrans import Translator

# 要翻墙，不然这个网站进不去
# translator = Translator(service_urls=['translate.google.cn'])
def transAb(tex):
	translator = Translator()
	return translator.translate(tex, src = 'en',dest='zh-CN').text
	