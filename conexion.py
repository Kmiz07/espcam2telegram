import configuracion,gc,uPYbot,utime
import camera, machine, esp32, ure
from machine import Pin
from utime import sleep
#######################################################################################
#             EVENTOS BOT (Nombres de eventos definidos al declarar el Bot            #
#######################################################################################
class camara():
    tamanyo_imagen = camera.FRAME_HD
    efecto_especial = camera.EFFECT_NONE
    balance_blancos = camera.WB_NONE
    saturacion = 0
    brillo = 0
    contraste = 0
    calidad = 10
#     camara = {
#     tamanyo_imagen : camera.FRAME_HD,
#     efecto_especial : camera.EFFECT_NONE,
#     balance_blancos : camera.WB_NONE,
#     saturacion : 0,
#     brillo : 0,
#     contraste : 0,
#     calidad : 10 }
    
tiempo_de_dormir = utime.time()
dormir = True
reiniciar = False
def evento_recepcion(datos_recibidos, miBot):
    global camara
#     pass
#         Esta funcion funciona como un evento de recepcion de get_updates.
#         En datos_recibidos, recibimos un objeto mensaje con la siguiente estructura:
#         ok = boolean que define si la respuesta fue satisfactoria.
#         vacio = boolean que dice si el mensaje es vacio 
#         indice = indice del mensaje
#         remite = nombre del remitente
#         remite_id = id del remitente
#         texto = texto del mensaje
#         chat_id = id del canal
#         chat_titulo = si venia de un canal, el titulo del mismo       
#         tipo = sera private si es mensaje privado o supergroup si viene de un canal
#         tiempo = puntero del tiempo del momento de la creacion del mensaje. esta definido desde el 1 de 1 de 2000, normalmente marcara 30 años mas
#         en miBot nos llega una referencia al bot creado.
    global tiempo_de_dormir
    tiempo_de_dormir = utime.time()#inicializa el tiempo
    print('mensaje_id : ',datos_recibidos.indice)
    if datos_recibidos.texto == 'nodormir':
        global dormir
        dormir = False
        miBot.send_message(datos_recibidos.chat_id,'Ahorro de energia desactivado')
    elif datos_recibidos.texto == 'reset':
        global reiniciar
        reiniciar= True

    elif datos_recibidos.texto == 'dormir':
        global dormir
        dormir = True
        miBot.send_message(datos_recibidos.chat_id,'Ahorro de energia activado')
    elif datos_recibidos.texto == 'hola':
        miBot.send_message(datos_recibidos.chat_id,'Soy un bot. Como estas?')
    elif datos_recibidos.texto == 'foto':
        envia_foto(miBot,'foto pedida por usuario')
    elif datos_recibidos.texto == 'ayuda':
        mensaje_ayuda = '<b><u>COMANDOS ACEPTADOS</u></b>%0a'
        mensaje_ayuda += '%0a<b>reset</b> = resetear el bot%0a'
        mensaje_ayuda += '%0a<b>dormir/nodormir</b> = activa o desactiva el sueño de ahorro de energia%0a'
        mensaje_ayuda += '%0a<b>ayuda</b> = esta ayuda%0a'
        mensaje_ayuda += '%0a<b>hola</b> = Mensaje de bienvenida%0a'
        mensaje_ayuda += '%0a<b>foto</b> = envia foto%0a'
        mensaje_ayuda += '%0a<b>camara_resolucion_[N]</b> = Configuracion de la resolucion (FRAME_96X96/0, FRAME_QQVGA/1, FRAME_QCIF/2, FRAME_HQVGA/3, FRAME_240X240/4, FRAME_QVGA/5, FRAME_CIF/6, FRAME_HVGA/7, FRAME_VGA/8, FRAME_SVGA/9, FRAME_XGA/10, FRAME_HD/11, FRAME_SXGA/12, FRAME_UXGA/13) de la camara, si no se indica N retorna el valor existente.%0a'
        mensaje_ayuda += '%0a<b>camara_brillo_[N]</b> = Configuracion del brillo (-2/2) de la camara, si no se indica N retorna el valor existente.%0a'
        mensaje_ayuda += '%0a<b>camara_contraste_[N]</b> = Configuracion del contraste (-2/2) de la camara, si no se indica N retorna el valor existente.%0a'
        mensaje_ayuda += '%0a<b>camara_saturacion_[N]</b> = Configuracion de la saturacion (-2/2) de la camara, si no se indica N retorna el valor existente.%0a'
        mensaje_ayuda += '%0a<b>camara_calidad_[N]</b> = Configuracion de la calidad (10/64) de la camara, si no se indica N retorna el valor existente.%0a'
        mensaje_ayuda += '%0a<b>camara_balance_[N]</b> = Configuracion del balance de blancos (WB_NONE/0 WB_SUNNY/1 WB_CLOUDY/2 WB_OFFICE/3 WB_HOME/4) de la camara, si no se indica N retorna el valor existente.%0a'
        miBot.send_message(datos_recibidos.chat_id,mensaje_ayuda)
        print(mensaje_ayuda)
    else:
        separa_por_comando = ure.compile('_')
        porciones = separa_por_comando.split(datos_recibidos.texto)
        if len(porciones) > 1:#cualquier comando debe se mayor que 1
            if porciones[0] == 'camara':#si es comando de camara
                if len(porciones) == 3:#existe valor por lo que se inserta
                    fallo = False
                    if porciones[1] == 'brillo':
                        if -2 <= int(porciones[2]) <= 2:
                            camara.brillo = int(porciones[2])
                        else: fallo = True
                    elif porciones[1] == 'contraste':
                        if -2 <= int(porciones[2]) <= 2:
                            camara.contraste = int(porciones[2])
                        else: fallo = True
                    elif porciones[1] == 'saturacion':
                        if -2 <= int(porciones[2]) <= 2:
                            camara.saturacion = int(porciones[2])
                        else: fallo = True
                    elif porciones[1] == 'calidad':
                        if 10 <= int(porciones[2]) <= 64:
                            camara.calidad = int(porciones[2])
                        else: fallo: True
                    elif porciones[1] == 'balance':
                        if 0 <= int(porciones[2]) <= 4:
                            camara.balance_blancos = int(porciones[2])
                        else: fallo = True
                    elif porciones[1] == 'resolucion':
                        if 0 <= int(porciones[2]) < 14:
                            camara.tamanyo_imagen = int(porciones[2])
                        else: fallo = True
                    else:
                        fallo = True
                        miBot.send_message(datos_recibidos.chat_id,porciones[1] + ' no es un comando aceptado')
                    if not fallo:
                        envia_foto(miBot,datos_recibidos.texto)
                valor_retorno = ''
                if len(porciones) == 2:#no existe valor, por lo que se retorna el valor
                    if porciones[1] == 'brillo':
                        valor_retorno = camara.brillo
                    elif porciones[1] == 'contraste':
                        valor_retorno = camara.contraste
                    elif porciones[1] == 'saturacion':
                        valor_retorno = camara.saturacion
                    elif porciones[1] == 'calidad':
                        valor_retorno = camara.calidad
                    elif porciones[1] == 'balance':
                        valor_retorno = camara.balance_blancos
                    elif porciones[1] == 'resolucion':
                        valor_retorno = camara.tamanyo_imagen
                    else:
                        miBot.send_message(datos_recibidos.chat_id,porciones[1] + ' no es un comando aceptado')
                    if valor_retorno != '':
                        miBot.send_message(datos_recibidos.chat_id,str(porciones[1]) + ' = ' + str(valor_retorno))

            
    
def bucle_programa(miBot):
    if utime.time()-10 > tiempo_de_dormir:
        if reiniciar:configuracion.reinicia()#reiniciar
        if dormir: a_dormir()#ajustando consumo

    #Esta funcion es el tipico loop de programa, aqui se debe introducir el codigo de manejo de programa
    #normalmente sera utilizado para lectura de pines o sensores
    #Importante no bloquear si no es estrictamente necesario con while true o similares, ya que periodicamente esta funcion sera llamada automaticamente
    #En miBot disponemos de una referencia al bot creado
#     pass
    
################################################################################################
#                                 FIN EVENTOS BOT                                              #
################################################################################################
def main():
    print('se reinicio por (%d)' %(machine.reset_cause()))
    causa_rst = "inicio forzado"
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        if machine.wake_reason() == 2:
            causa_rst = " alarma apertura de puertas "
        elif machine.wake_reason() == 4:
            causa_rst = "tiempo reloj"
        else:
            causa_rst = str(machine.wake_reason())
        
    Bot=uPYbot.uBot(configuracion.Telegram_Bot,'api.telegram.org',  evento_recepcion, bucle_programa)
    Bot.send_message(configuracion.Chat_Id,'(%s) Se ha iniciado programa (%s segundos) por %s' %(machine.reset_cause(), utime.time(), causa_rst))
#     envia_foto(Bot)
    z=Bot.inicia()
def envia_foto(Bot,mensaje=''):
    global camara
#------------------ejemplo envio de foto-------------------------------------------------------
#     camera.init(0, format=camera.JPEG)
    try:
        camera.init(0, format=camera.JPEG)
    except OSError as exc:
        camera.deinit()
        Bot.send_message(Bot.canal,exc.args[0])
        print(exc.args)
        return

    Led = Pin(4, Pin.OUT)    # define flash
    Led.on()  #enciende flash   
    # girar vertical
    camera.flip(0)
    # giro horizontal
    camera.mirror(0)

    camera.framesize(camara.tamanyo_imagen)
    #'FRAME_240X240'/4, 'FRAME_96X96'/0, 'FRAME_CIF'/6, 'FRAME_FHD'/14, 'FRAME_HD'/11, 'FRAME_HQVGA'/3, 'FRAME_HVGA'/7, 'FRAME_P_3MP'/16, 'FRAME_P_FHD'/20, 'FRAME_P_HD'/15, 'FRAME_QCIF'/2, 'FRAME_QHD'/18, 'FRAME_QQVGA'/1, 'FRAME_QSXGA'/21, 'FRAME_QVGA'/5, 'FRAME_QXGA'/17, 'FRAME_SVGA'/9, 'FRAME_SXGA'/12, 'FRAME_UXGA'/13, 'FRAME_VGA'/8, 'FRAME_WQXGA'/19, 'FRAME_XGA'/10

    # efectos especiales
    camera.speffect(camara.efecto_especial)
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

    # white balance
    camera.whitebalance(camara.balance_blancos)
    # The options are the following:
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

    # saturation
    camera.saturation(camara.saturacion)
    # -2,2 (default 0). -2 grayscale 

    # brightness
    camera.brightness(camara.brillo)
    # -2,2 (default 0). 2 brightness

    # contrast
    camera.contrast(camara.contraste)
    #-2,2 (default 0). 2 highcontrast

    # quality
    camera.quality(camara.calidad)
    # 10-63 lower number means higher quality
    bufer=camera.capture()
    print('captura realizada')
    Led.off() #apaga flash
    with open('file.jpg','w') as k:
        k.write(bufer)
    bufer = None
    camera.deinit()
    Bot.envia_archivo_multipart(configuracion.Chat_Id, 'file.jpg', 'sendPhoto', 'photo',mensaje)
# ---------------------------------------------------------------------------------------------
def a_dormir(alarma = 14, despertar_ms = 60000):
        despertador = Pin(alarma, mode = Pin.IN)
        esp32.wake_on_ext0(pin = despertador, level = esp32.WAKEUP_ALL_LOW)
        print('durmiendo')
        machine.deepsleep(despertar_ms)


                    




