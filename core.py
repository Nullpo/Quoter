#!/usr/bin/python
# -*- encoding: utf-8 -*-
import urllib
import simplejson
from subprocess import check_output
import time
import logging

def buscarFrase(frase):
   query = urllib.urlencode({'q' : frase})
   url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
   search_results = urllib.urlopen(url)
   json = simplejson.loads(search_results.read())
   if json:
      if json['responseData']:
         results = json['responseData']['results']
      else:
         return False
   else:
      return False
   for i in results:
      logging.info("   - Resultado: " + i['title'])
      if i['title'].upper().find("LETRA") != -1 or i['title'].upper().find("LYRICS") != -1 or i['title'].upper().find("YOUTUBE") != -1 :
         return i['title'] + " " + i['url']
   return False


def publicarMensaje(mensaje):
   return check_output(["twidge","update ","\'" + resp + "\'"])


logging.basicConfig(filename='myapp.log', level=logging.INFO)

while(3>2):
   try:
      salida = check_output(["twidge","lsrecent","-l","-s","-u"])
   except:
      logging.info("Error al obtener mensajes")
   tweets = salida.split("\n");
   for i in tweets:
      if i != "":
         (uuid,nick,_,texto,_,_) = i.split("\t")
         logging.info("Buscar la frase: " + texto)
         data = buscarFrase(texto)
         if(data):
            data = data.replace("<b>","").replace("</b>","").replace("!","")
            logging.info(" - Encontrado en google:" + data)
            resp = "@" + nick + " " + data
            logging.info(" - Ejecutamos twidge update \'" + resp + "\'")
            try:
               x = publicarMensaje(resp)
               logging.info(" - Salida del twidge:" + x)
            except Exception as e:
               logging.info("Error al twittear el mensaje ID:" + uuid )
               logging.info(type(e))
               logging.info(e)
         else:
             logging.info(" - No se encontró nada")