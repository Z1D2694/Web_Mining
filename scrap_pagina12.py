# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerProcess
from urllib import parse
from os import path
from scrapy.http.response.html import HtmlResponse
import sys    



# Se crean la listas de url a scrapear.
economia = []
sociedad = []
elmundo = []
elpais = []

lista_temas = [economia, sociedad, elmundo, elpais]
temas = ['economia', 'sociedad' , 'el-mundo','el-pais']

# lista_temas = [elpais]
# temas = ['el-pais']


for posicion, tema in enumerate(temas):
    for i in range(1,7):
        lista_temas[posicion].append(f"https://www.pagina12.com.ar/secciones/{tema}?page={i}")



class NewsSpider(CrawlSpider):

    name = 'crawler_pagina12'
    # solo descargar paginas desde estos dominios
    allowed_domains = ('www.pagina12.com.ar','pagina12.com.ar')
    
    
    # URL ejemplo: https://www.pagina12.com.ar/478007-afip-incauto-mas-maiz
    # EXPRESIONES REGULARES: https://docs.python.org/3/library/re.html#regular-expression-syntax
    # Página para explicar/armar una expresión regular: https://regexr.com/
    
    rules = (
        # solo bajar las paginas cuya url incluye "/secciones", pero no aquellas cuya url include "/catamarca12" o "/dialogo"
        # normaliza las urls para no descargarlas 2 veces la misma pagina con distinta url.
        
        Rule(LinkExtractor(allow = r'.+([0-9]{6,}).+', # Se detalla las características del url que sigue a ('http://www.pagina12.com.ar/')
                           deny='.+(/catamarca12|/dialogo).+',
                           deny_domains=['auth.pagina12.com.ar'], canonicalize=True,
                           deny_extensions=['7z', '7zip', 'apk', 'bz2', 'cdr,' 'dmg', 'ico,' 'iso,' 'tar', 'tar.gz','pdf','docx', 'jpg', 'png', 'css', 'js']),
                           callback='parse_response', follow=True),
     )
     
    # configuracion de scrappy, ver https://docs.scrapy.org/en/latest/topics/settings.html
    custom_settings = {
     
    # mentir el user agent. Es lo más básico para detectar a un scraper.
     'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
     'LOG_ENABLED': True,
     'LOG_LEVEL': 'INFO',
     
    # no descargar mas de 1 link desde la pagina de origen (Valor profesor = 2).
     'DEPTH_LIMIT': 1,
      
    # ignorar robots.txt (que feo).
     'ROBOTSTXT_OBEY': False,
     
    # # esperar entre 0.5*DOWNLOAD_DELAY y 1.5*DOWNLOAD_DELAY segundo entre descargas.
     'DOWNLOAD_DELAY': 0.75,
     'RANDOMIZE_DOWNLOAD_DELAY': True
    }

    def __init__(self, save_pages_in_dir='.', *args, **kwargs):
          super().__init__(*args, **kwargs)
          # guardar el directorio en donde vamos a descargar las paginas
          self.basedir = save_pages_in_dir
    
    def parse_response(self, response:HtmlResponse):
          """
          Este metodo es llamado por cada url que descarga Scrappy.
          response.url contiene la url de la pagina,
          response.body contiene los bytes del contenido de la pagina.
          """
          # el nombre de archivo es lo que esta luego de la ultima "/"
          print(type(response))
          html_filename = path.join(self.basedir,parse.quote(response.url[response.url.rfind("/")+1:]))
          if not html_filename.endswith(".html"):
              html_filename+=".html"
          print("URL:",response.url, "Pagina guardada en:", html_filename)
          with open(html_filename, "wt", encoding="utf-8") as html_file: # el encoding hace que los acentos no sean decodificados como caracteres raros.
              html_file.write(response.body.decode("utf-8"))
          
directorio_guardado = r'C:/Users/nacho/My Drive/3.- MCD/3.- Materias/18.- Web Mining/Práctica/TP1/Articulos_test_ultima_semana'

# En esta sección se define la página a scrapear y el directorio donde se guardan los archivos.
# if __name__ == "__main__":
#   crawler = CrawlerProcess()
#   crawler.crawl(NewsSpider, save_pages_in_dir= directorio_guardado, start_urls = ['http://www.pagina12.com.ar/secciones/economia?page=1'])
#   crawler.start()
 

if __name__ == "__main__":
   
    for posicion, tema in enumerate(temas):
    
        crawler = CrawlerProcess()
    
        if "twisted.internet.reactor" in sys.modules:
            del sys.modules["twisted.internet.reactor"]
    
        crawler.crawl(NewsSpider, save_pages_in_dir= f"{directorio_guardado}/{tema}", start_urls = lista_temas[posicion])
        crawler.start()