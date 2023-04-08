#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import argparse
import socket
import time
import threading
try :
 import Queue
except :
 import queue as Queue
socket . setdefaulttimeout ( 15 )
queue = Queue . Queue ( )
def IiII1IiiIiI1 ( thread_function , args = ( ) ) :
 try :
  thread_function ( * args )
 except KeyboardInterrupt :
  raise
 except :
  pass
def IIiIiII11i ( num_threads , thread_function , args = ( ) ) :
 o0oOOo0O0Ooo = [ ]
 for num_threads in range ( num_threads ) :
  I1ii11iIi11i = threading . Thread ( target = IiII1IiiIiI1 , name = str ( num_threads ) ,
 args = ( thread_function , args ) )
  I1ii11iIi11i . setDaemon ( True )
  try :
   I1ii11iIi11i . start ( )
  except :
   break
  o0oOOo0O0Ooo . append ( I1ii11iIi11i )
 I1IiI = True
 while I1IiI :
  I1IiI = False
  for I1ii11iIi11i in o0oOOo0O0Ooo :
   if I1ii11iIi11i . isAlive ( ) :
    I1IiI = True
    time . sleep ( 0.1 )
def O00ooOO ( port_range ) :
 I1iII1iiII = [ ]
 for iI1Ii11111iIi in port_range . split ( ',' ) :
  if '-' in iI1Ii11111iIi :
   i1i1II , O0oo0OO0 = iI1Ii11111iIi . split ( '-' )
   for I1i1iiI1 in range ( int ( i1i1II ) , int ( O0oo0OO0 ) + 1 ) :
    I1iII1iiII . append ( str ( I1i1iiI1 ) )
  else :
   I1iII1iiII . append ( iI1Ii11111iIi )
 return I1iII1iiII
def Ii1iI ( ip_range ) :
 def Oo ( num ) :
  return '%s.%s.%s.%s' % ( ( num >> 24 ) & 0xff , ( num >> 16 ) & 0xff , ( num >> 8 ) & 0xff , ( num & 0xff ) )
 def Oo0o0000o0o0 ( ip ) :
  oOo0oooo00o = [ int ( oO0o0o0ooO0oO ) for oO0o0o0ooO0oO in ip . split ( '.' ) ]
  return oOo0oooo00o [ 0 ] << 24 | oOo0oooo00o [ 1 ] << 16 | oOo0oooo00o [ 2 ] << 8 | oOo0oooo00o [ 3 ]
 OOooO , OOoO00o = [ Oo0o0000o0o0 ( oO0o0o0ooO0oO ) for oO0o0o0ooO0oO in ip_range . split ( '-' ) ]
 return [ Oo ( II111iiiiII ) for II111iiiiII in range ( OOooO , OOoO00o + 1 ) if II111iiiiII & 0xff ]
def o0oOo0Ooo0O ( host_port ) :
 OO00O0O0O00Oo , iI1Ii11111iIi = host_port . split ( ':' )
 try :
  IIIiiiiiIii = socket . socket ( socket . AF_INET , socket . SOCK_STREAM )
  IIIiiiiiIii . connect ( ( str ( OO00O0O0O00Oo ) , int ( iI1Ii11111iIi ) ) )
 except :
  return host_port , 'close' , ''
 try :
  OO = IIIiiiiiIii . recv ( 512 )
  if len ( OO ) > 2 :
   return host_port , 'open' , OO . decode ( 'utf8' , errors = 'ignore' ) . strip ( )
  else :
   IIIiiiiiIii . send ( 'a\n\n' )
   OO = IIIiiiiiIii . recv ( 512 )
   IIIiiiiiIii . close ( )
   if len ( OO ) > 2 :
    return host_port , 'open' , OO . decode ( 'utf8' , errors = 'ignore' ) . strip ( )
   else :
    return host_port , 'open' , ''
 except :
  IIIiiiiiIii . close ( )
  return host_port , 'open' , ''
def OoO000 ( ) :
 while not queue . empty ( ) :
  IIiiIiI1 = queue . get ( )
  try :
   IIiiIiI1 , iiIiIIi , ooOoo0O = o0oOo0Ooo0O ( IIiiIiI1 )
   sys . stdout . write ( '[{}] {}\t{}\t{}\n' . format ( '+' if iiIiIIi == 'open' else '-' , IIiiIiI1 , iiIiIIi , ooOoo0O ) )
  except :
   pass
def OooO0 ( ) :
 II11iiii1Ii = argparse . ArgumentParser ( description = u'socket tcp portscan' )
 II11iiii1Ii . add_argument ( '-i' , "--input" , dest = 'hosts' , help = 'targets, IP (192.168.1.1), IP range(192.18.1.1-192.168.1.3), txt file(xxx.txt), ip:port(192.168.1.1:80)' )
 II11iiii1Ii . add_argument ( '-p' , "--port" , dest = 'ports' , default = '21-23,80,443,445,1433,1521,3306,3389,6379,7001,8080,8443' , help = 'ports, default \'21-23,80,443,445,1433,1521,3306,3389,6379,7001,8080,8443\'' )
 II11iiii1Ii . add_argument ( '-t' , "--thread" , dest = 'threadnum' , type = int , default = 20 , help = 'threadnum, default 20' )
 OO0o = II11iiii1Ii . parse_args ( )
 if not OO0o . hosts :
  II11iiii1Ii . print_help ( )
  sys . exit ( "[*] need -i" )
 else :
  if os . path . isfile ( OO0o . hosts ) :
   Ooo = [ O0o0Oo . strip ( ) for O0o0Oo in open ( OO0o . hosts , 'r' , encoding = 'utf8' ) . readlines ( ) ]
  else :
   Ooo = [ OO0o . hosts ]
  for OO00O0O0O00Oo in Ooo :
   if ':' in OO00O0O0O00Oo :
    queue . put ( OO00O0O0O00Oo )
   else :
    if '-' in OO00O0O0O00Oo :
     for Oo00OOOOO in Ii1iI ( OO00O0O0O00Oo ) :
      for iI1Ii11111iIi in O00ooOO ( OO0o . ports ) :
       queue . put ( '{}:{}' . format ( Oo00OOOOO , iI1Ii11111iIi ) )
    else :
     for iI1Ii11111iIi in O00ooOO ( OO0o . ports ) :
      queue . put ( '{}:{}' . format ( OO00O0O0O00Oo , iI1Ii11111iIi ) )
  IIiIiII11i ( OO0o . threadnum , OoO000 )
if __name__ == '__main__' :
 OooO0 ( )
