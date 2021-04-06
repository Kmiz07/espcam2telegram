
import configuracion,gc,network,utime,ure,usocket,conexion
from machine import Pin
piloto = 33#pin del led rojo en esp32cam. para esp32 comun usar pin2

def crea_pagina(valores):
    pagina = '<html>\r\n<head>\r\n</head>\r\n<body>\r\n<form action="configura.html" method="post">\r\n<ul>'
    for k in valores:
        pagina += '\r\n<li>\r\n'
        pagina +='<label for="' + k + '">'+ k +':</label>'
        pagina += '<input type="text" id="' + k +'" name="' + k + '" value="' + valores[k] + '" size="60">\r\n<li/>'
    pagina += '<li class="button">\r\n<button type="submit">Actualizar</button></li>'
    pagina += '\r\n<ul/>\r\n<form/>\r\n</body>\r\n</html>'
    cabecera ='HTTP/1.1 200 OK\r\nContent-Type: text/html \r\nContent-Lengh: ' +str(len(pagina)) +' \r\nConnection: keep-alive\r\n\r\n'
    cabecera += pagina
    return cabecera  
    

                    
def main():
   
#conectamos a wifi segun configuracion en datos.dat
    configuracion.convertir()
    indice = 0
    wlan = network.WLAN(network.STA_IF)
    aplan = network.WLAN(network.AP_IF)
    aplan.active(False)
    wlan.active(True)
    if configuracion.forzar == True:
        wlan.ifconfig(configuracion.ST_CONF)
    tiempo = utime.time()
    wlan.connect(configuracion.ST_SSID,configuracion.ST_PASSW)
    while not wlan.isconnected():            
        if utime.time()-15>tiempo:
            break           
    if wlan.isconnected():
        msg_inicio= "conectado como ST en: "+ str(wlan.ifconfig()[0])   
        print(msg_inicio)
        conexion.main()



#Cuando falla sta se crea un ap y se debe conectar en el y en un navegador enviar: [192.168.4.1/<SSID>,<PASSW>]
#el chip se reseteara con la nueva configuracion, y si no es correcta, volvera al ap de nuevo para reconfigurar.
    
    else:
        separa_por_lineas = ure.compile('[\r\n]')
        separa_por_espacios = ure.compile('\s')
        separa_por_and = ure.compile('&')
        cambia_comillas = ure.compile('%27')
        cambia_abre_corchete = ure.compile('%5B')
        cambia_cierra_corchete = ure.compile('%5D')
        cambia_coma = ure.compile('%2C')
        cambia_dos_puntos = ure.compile('%3A')
        separa_k_v = ure.compile('=')
        
        tipo=[]
        motivo=[]
        valores=configuracion.lee()
        pagina= crea_pagina(valores)
        wlan.active(False)
        aplan.active(True)
        aplan.ifconfig(configuracion.AP_CONF)                
        aplan.config(essid = configuracion.AP_SSID, password = configuracion.AP_PASSW)
        print("Conectado como AP en:",aplan.ifconfig())
        p0 = Pin(piloto, Pin.OUT)
        p0.value(0)
        confserv = ("",80)
        serv_socket = usocket.socket()
        serv_socket.bind(confserv)
        serv_socket.listen(1)
        while True:
            conn, addr = serv_socket.accept()
            recepcion=''
            datos=''
            datos = conn.readline()
            while datos != b'':
                recepcion += (datos.decode())
                datos = conn.readline()
                if datos == b'\r\n':
                    break
            if recepcion != '':
                lineas=separa_por_lineas.split(recepcion)
                nombres=separa_por_espacios.split(lineas[0])
                tipo=nombres[0]#'GET' o 'POST' 
                motivo=nombres[1]# '/' o 'configura.html'
            else:
                print('no llegaron datos validos')
            a=['GET','/']
            if tipo == 'GET' and motivo =='/':
                conn.sendall(pagina)
                conn.close()
            elif tipo == 'POST' and motivo =='/configura.html':
                for linea in lineas:
                    valores_linea = separa_por_espacios.split(linea)
                    nombre_dato = valores_linea[0]
                    if nombre_dato == 'Content-Length:':
                        longitud = int(valores_linea[1])
                datos = conn.read(longitud).decode()

#         modifica respuestas para poder ingresarlas en el archivo de configuracion
                resultados = separa_por_and.split(datos)
                for resultado in resultados:
                    resultado_ok = cambia_comillas.sub("'",resultado)
                    resultado = cambia_abre_corchete.sub("[",resultado_ok)
                    resultado_ok = cambia_cierra_corchete.sub("]",resultado)
                    resultado = cambia_coma.sub(",",resultado_ok)
                    resultado_ok = cambia_dos_puntos.sub(":",resultado)
                    k,v = separa_k_v.split(resultado_ok)
                    configuracion.unir(k,v)
                conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html \r\nConnection: close \r\n\r\n<html><body>Cambios realizados</body></html>\r\n\r\n')
                conn.close()
                ahora = utime.time()
                while utime.time() - 5 > ahora:
                    pass
                break
            else:
                conn.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html \r\nConnection: close \r\n\r\n<html><body>Pagina no aceptada</body></html>\r\n\r\n')
                conn.close()
        print('saliendo y reiniciando')
        serv_socket.close()
        p0.value(1)
        configuracion.reinicia()
gc.collect()