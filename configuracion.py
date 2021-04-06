import ujson,uos,machine

fileconf='datos.dat'
def escribe(datos):
    with open(fileconf,'w') as f:
        ujson.dump(datos,f)
def lee():
    with open(fileconf,'r') as f:
        return ujson.load(f)
def reinicia():
    machine.reset()
def unir(variable,texto):
    z=lee()
    z[variable]=texto
#     print(z)
    escribe(z)
def eliminar(clave):
    z=lee()
    try:
        del z[clave]
#         print(z)
    except:
        print("No existe la clave:valor")
    escribe(z)
def convertir():
    z=lee()
    for k in z:
        linea='global '+k+';'+k + '=' +z[k]
#         print(linea)
        exec(linea)
    