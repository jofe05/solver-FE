
import numpy as np

import sys

total = len(sys.argv)


if total < 4:
    print "No se ingreso el numero correspondiente de parametros. Se toman los valores por defecto"
    inputData = "default.csv"
    inputValues = "enunciado.csv"
    outFile = "log.txt"
else:
    inputData = str(sys.argv[1])
    inputValues = str(sys.argv[2])
    outFile = str(sys.argv[3])

fifo = "FIFO"+outFile
sjf = "SFJ"+outFile
prioridad = "Prioridad"+outFile


datos  = np.loadtxt("../data/"+inputData, dtype = int, delimiter = ',')
f=open('../data/'+outFile, 'w')
f_fifo=open('../data/'+fifo, 'w')
f_sjf=open('../data/'+sjf, 'w')
f_prioridad=open('../data/'+prioridad, 'w')

enunciado = np.loadtxt("../data/"+inputValues, dtype = float, delimiter = ",")
bolso = enunciado[0]
carro = enunciado[1]
tcarta = enunciado[2]*60
tpaquete = enunciado[3]*60
jornada = enunciado[4]*3600
velocidad = enunciado[5]
dcorreosA = enunciado[6]
dcorreosB = enunciado[7]
dcorreosC = enunciado[8]
volA = enunciado[9]
volB = enunciado[10]
volC = enunciado[11]


print>>f,"================= Datos Iniciales ================= "
print>>f, "Capacidad del bolso:",bolso
print>>f, "Capacidad del carro [cm3]:",carro
print>>f,"Tiempo de entrega de carta [Segundos]:",tcarta
print>>f,"Tiempo de entrega de paquete [Segundos]:",tpaquete
print>>f,"Jornada [Segundos]:",jornada
print>>f,"Velocidad del cartero:",velocidad
print>>f,"Distancia de la calle 1 a la oficina de correos",dcorreosA
print>>f,"Distancia de la calle 2 a la oficina de correos",dcorreosB
print>>f,"Distancia de la calle 3 a la oficina de correos",dcorreosC
print>>f,"Volumen A:",volA 
print>>f,"Volumen B:",volB 
print>>f,"Volumen C:",volC 



#*****************************
#******* SJF *****************
#*****************************

print>>f_sjf, "Inicianilizando Variables - PARA SJF"
posAnterior = 0
cartasAc = 0 #cartas acumuladas
paqAc = 0
i = 0 #indice que recorre los datos
tiempoDiario = 0
j = 0
viajes = 0
dias = 0
tiempo = [] #Tiempo Total- arreglo donde cada elemento es el tiempo invertido en ese dia por el cartero
indiceNE = [] #Indice de NO Entregados - guardo el indice para saber a partir de que casa no fueron entregadas el resto de las cartas ese dia
feiners = 3 #dias laborables



while i < len(datos):

    while ((cartasAc < bolso) and (i < len(datos))):
        #print>>f_sjf, "paqA",paqAc, "<", "carro",carro 
        if (paqAc < carro):
            print>>f_sjf, "Cartas acumuladas ",cartasAc
            print>>f_sjf, "Volumen acumulado ",paqAc
            print>>f_sjf, "Analizo la casa", datos[i,1]
            print>>f_sjf, "Estoy en calle", datos[i,2]
            print>>f_sjf, "Tengo que entregar ", sum(datos[i,4:7]),"cartas en esta casa"
            print>>f_sjf, "Tengo que entregar ", sum(datos[i,7:]),"paquetes en esta casa"
            print>>f_sjf, "Tiempo acumulado", tiempoDiario

            
            cartasAc = sum(datos[i,4:7]) + cartasAc
        
            if ((sum(datos[i,4:7]) > 0) or (sum(datos[i,7:])>0)):
                if posAnterior == 0: 
                    if datos[posAnterior,2] == 1:
                        tiempoDiario = dcorreosA/velocidad
                    elif datos[posAnterior,2] == 2:
                        tiempoDiario = dcorreosB/velocidad
                    elif datos[posAnterior,2] == 3:
                        tiempoDiario = dcorreosB/velocidad
                if (datos[posAnterior,2] == datos[i,2]):   
                    tiempoDiario += (datos[i,3] - datos[posAnterior,3])/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                paqAc += datos[i,7]*volA + datos[i,8]*volB + datos[i,9]*volC
                posAnterior = i 
            
            if tiempoDiario >= jornada:
                print>>f_sjf, "===================CARTERO:VUELVO A LA OFICINA: FIN DE JORNADA============================="
                if (datos[i,2] == 0):
                    tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
                elif (datos[i,2] == 1):
                    tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
                elif (datos[i,2] == 2):
                    tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2    
                tiempo.append(tiempoDiario)
                indiceNE.append(i)
                tiempoDiario=0
                dias += 1
       
        else: #Se queda sin paquetes: vuelve el cartero a la oficina
            print>>f_sjf, "===================CARTERO:VUELVO A LA OFICINA POR MAS PAQUETES============================="
            cartasAc = 0 #De paso carga cartas
            paqAc= paqAc - carro #Siempre va a haber mas paquetes acumulados que espacio en el carro.
            viajes += 1
            if (datos[i,2] == 0):
                tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
            elif (datos[i,2] == 1):
                tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
            elif (datos[i,2] == 2):
                tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
        
            
        i += 1    
    if i<len(datos): #Se queda sin cartas: vuelve el cartero a la oficina
        print>>f_sjf, "===================CARTERO:VUELVO A LA OFICINA POR MAS CARTAS============================="
        paqAc=0 #De paso carga paquetes
        cartasAc = cartasAc - bolso #Siempre va a haber mas cartas acumulados que espacio en el bolso.
        if (datos[i,2] == 0): #Depende la calle en la que esta el cartero -> el tiempo de ida y vuelta cambia.
            tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
        elif (datos[i,2] == 1):
            tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
        elif (datos[i,2] == 2):
            tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
    else:   
        break
        	    
    viajes += 1

tiempo.append(tiempoDiario)
indiceNE.append(i)
f_sjf.close()
#print "LEN(tiempo)", len(tiempo)
print >>f," ============================================================================="            
print >>f, "***SFJ***"
print >>f, "*** Informe Diario*** "
k = 0
if len(tiempo) > 4:
    feiners=4
else:
    feiners=len(tiempo)   
while k < feiners:
    print >>f,("\n")
    print >>f,"Dia ",k+1
    print >>f,"Tiempo: ", tiempo[k],"[segundos]", tiempo[k]/3600, "[horas]"
    print >>f,"Cartas sin entregar\n P1:", sum(datos[indiceNE[k]:,4]), " P2:",  sum(datos[indiceNE[k]:,5]), " P3:",  sum(datos[indiceNE[k]:,6])
    print >>f,"Paquetes sin entregar\n V1:", sum(datos[indiceNE[k]:,7]), " V2:",  sum(datos[indiceNE[k]:,8]), " V3:",  sum(datos[indiceNE[k]:,9])
    k += 1

print>>f,("\n")
print>>f,("\n")
if len(tiempo) > 4:
    print >>f,"Se necesitan", len(tiempo), "dias para entregar todas las cartas"  
print >>f,"Tiempo total para los dias laborables", sum(tiempo[0:feiners+1]), "[segundos]", sum(tiempo[0:feiners+1])/3600,"[horas]"
print >>f,"Dias trabajado (dias necesarios)", feiners, "(",dias +1,")"
print >>f,"Viajes realizados", viajes
 
#******* PRIORIDAD *****************

print>>f_prioridad,"Inicianilizando Variables - Prioridad"
posAnterior = 0
cartasAc = 0 #cartas acumuladas
paqAc = 0
i = 0 #indice que recorre los datos
tiempoDiario = 0
j = 0
viajes = 0
dias = 0
tiempo = [] #Tiempo Total- arreglo donde cada elemento es el tiempo invertido en ese dia por el cartero
indiceNE = [] #Indice de NO Entregados - guardo el indice para saber a partir de que casa no fueron entregadas el resto de las cartas ese dia
feiners = 3 #dias laborables


for j in 1,2,3:
    print>>f_prioridad,"****ENTREGA DE CARTAS P:", j
    cartasAc=0
    paqAc=0
    i=0
    while i < len(datos):
        if j==1:
            A=1
            B=0
            C=0
        if j==2:
            A=0
            B=1
            C=0
        if j==3:
            A=0
            B=0
            C=1
        while ((cartasAc < bolso) and (i < len(datos))):
            #print>>f_prioridad,"paqA",paqAc, "<", "carro",carro 
            if (paqAc < carro):
                print>>f_prioridad,"Cartas acumuladas ",cartasAc
                print>>f_prioridad,"Volumen acumulado ",paqAc
                print>>f_prioridad,"Analizo la casa", datos[i,1]
                print>>f_prioridad,"Estoy en calle", datos[i,2]
                print>>f_prioridad,"Tengo que entregar ", datos[i,j+3],"cartas de P",j,"en esta casa"
                print>>f_prioridad,"Tengo que entregar ", datos[i,j+6],"paquetes de V",j,"en esta casa"
                print>>f_prioridad,"Tiempo acumulado", tiempoDiario
                print>>f_prioridad,"TIEMPO TOTAL",tiempo
                print>>f_prioridad,"Dia:", dias

                cartasAc = datos[i,j+3] + cartasAc
        
                if (datos[i,j+3]> 0) or (datos[i,j+6]>0):
                    if posAnterior == 0: #Chequea si es el primer viaje. En caso afirmativo se debe sumar la dist. a la ofi de correos.
                        if datos[posAnterior,2] == 1:
                           tiempoDiario = dcorreosA/velocidad
                        elif datos[posAnterior,2] == 2:
                           tiempoDiario = dcorreosB/velocidad
                        elif datos[posAnterior,2] == 3:
                           tiempoDiario = dcorreosB/velocidad
                    if (datos[posAnterior,2] == datos[i,2]):   
                        tiempoDiario += (datos[i,3] - datos[posAnterior,3])/velocidad + datos[i,j+3]*tcarta + datos[i,j+6]*tpaquete
                    elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                        tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + datos[i,j+3]*tcarta + datos[i,j+6]*tpaquete
                    elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                        tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + datos[i,j+3]*tcarta + datos[i,j+6]*tpaquete
                    paqAc += A*datos[i,j+6]*volA + B*datos[i,j+6]*volB + C*datos[i,j+6]*volC
                    print>>f_prioridad,"Volumen acumulado2 ",paqAc
                    posAnterior = i 
            
                if tiempoDiario >= jornada:
                    print>>f_prioridad,"===================CARTERO:VUELVO A LA OFICINA: FIN DE JORNADA============================="
                    if (datos[i,2] == 0):
                        tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
                    elif (datos[i,2] == 1):
                        tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
                    elif (datos[i,2] == 2):
                        tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2    
                    tiempo.append(tiempoDiario)
                    indiceNE.append(i)
                    tiempoDiario=0
                    dias += 1
            else: #Se queda sin paquetes: vuelve el cartero a la oficina
                print>>f_prioridad,"===================CARTERO :VUELVO A LA OFICINA POR MAS PAQUETES============================="
                cartasAc = 0 #De paso carga cartas
                paqAc= paqAc - carro #Siempre va a haber mas paquetes acumulados que espacio en el carro.
                viajes += 1
                if (datos[i,2] == 0):
                    tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
                elif (datos[i,2] == 1):
                    tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
                elif (datos[i,2] == 2):
                    tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
        
            
            i += 1    
        if i<len(datos): #Se queda sin cartas: vuelve el cartero a la oficina
            print>>f_prioridad,"===================CARTERO:VUELVO A LA OFICINA POR MAS CARTAS============================="
            paqAc=0 #De paso carga paquetes
            cartasAc = cartasAc - bolso #Siempre va a haber mas cartas acumulados que espacio en el bolso.
            if (datos[i,2] == 0): #Depende la calle en la que esta el cartero -> el tiempo de ida y vuelta cambia.
                tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
            elif (datos[i,2] == 1):
                tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
            elif (datos[i,2] == 2):
                tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
        else:   
            break
        viajes += 1
tiempo.append(tiempoDiario)
indiceNE.append(i)
f_prioridad.close()    
print >>f," ============================================================================="            
print >>f, "***Prioridad***"
print >>f, "*** Informe Diario*** "
#print "len(tiempo)", len(tiempo)
#print "tiempo", tiempo
k = 0
if len(tiempo) > 4:
    feiners=4
else:
    feiners=len(tiempo)   
while k < feiners:
    print >>f,("\n")
    print >>f,"Dia ",k+1
    print >>f,"Tiempo: ", tiempo[k],"[segundos]", tiempo[k]/3600, "[horas]"
    print >>f,"Cartas sin entregar\n P1:", sum(datos[indiceNE[k]:,4]), " P2:",  sum(datos[indiceNE[k]:,5]), " P3:",  sum(datos[indiceNE[k]:,6])
    print >>f,"Paquetes sin entregar\n V1:", sum(datos[indiceNE[k]:,7]), " V2:",  sum(datos[indiceNE[k]:,8]), " V3:",  sum(datos[indiceNE[k]:,9])
    k += 1

print>>f,("\n")
print>>f,("\n")
if len(tiempo) > 4:
    print >>f,"Se necesitan", len(tiempo), "dias para entregar todas las cartas"
print("\n")    
print >>f,"Tiempo total para los dias laborables", sum(tiempo[0:feiners+1]), "[segundos]", sum(tiempo[0:feiners+1])/3600,"[horas]"
print >>f,"Dias trabajado (dias necesarios)", feiners, "(",dias +1,")"
print >>f,"Viajes realizados", viajes



#************** FIFO ******************


datos=datos[datos[:,0].argsort()]

print("\n\n")
print>>f_fifo,"Inicianilizando Variables - FIFO"
posAnterior = 0
cartasAc = 0 #cartas acumuladas
paqAc = 0
i = 0 #indice que recorre los datos
tiempoDiario = 0
j = 0
viajes = 0
dias = 0
tiempo = [] #Tiempo Total- arreglo donde cada elemento es el tiempo invertido en ese dia por el cartero
indiceNE = [] #Indice de NO Entregados - guardo el indice para saber a partir de que casa no fueron entregadas el resto de las cartas ese dia
feiners = 3 #dias laborables



while i < len(datos):

    while ((cartasAc < bolso) and (i < len(datos))):
        #print>>f_fifo,"paqA",paqAc, "<", "carro",carro 
        if (paqAc < carro):
            print>>f_fifo,"Cartas acumuladas ",cartasAc
            print>>f_fifo,"Volumen acumulado ",paqAc
            print>>f_fifo,"Analizo la casa", datos[i,1]
            print>>f_fifo,"De la calle", datos[i,2]
            print>>f_fifo,"Tengo que entregar ", sum(datos[i,4:7]),"cartas en esta casa"
            print>>f_fifo,"Tengo que entregar ", sum(datos[i,7:]),"paquetes en esta casa"

            
            cartasAc = sum(datos[i,4:7]) + cartasAc
        
            if ((sum(datos[i,4:7]) > 0) or (sum(datos[i,7:])>0)):
                print>>f_fifo, "Me muevo"
                if posAnterior == 0: #Chequea si es el primer viaje. En caso afirmativo se debe sumar la dist. a la ofi de correos.
                        if datos[posAnterior,2] == 1:
                           tiempoDiario = dcorreosA/velocidad
                        elif datos[posAnterior,2] == 2:
                           tiempoDiario = dcorreosB/velocidad
                        elif datos[posAnterior,2] == 3:
                           tiempoDiario = dcorreosB/velocidad
                if (datos[posAnterior,2] == datos[i,2]):   
                    tiempoDiario += (datos[i,3] - datos[posAnterior,3])/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                paqAc += datos[i,7]*volA + datos[i,8]*volB + datos[i,9]*volC
                posAnterior = i 
            
            if tiempoDiario >= jornada:
                print>>f_fifo,"===================CARTERO:VUELVO A LA OFICINA: FIN DE JORNADA============================="
                if (datos[i,2] == 0):
                    tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
                elif (datos[i,2] == 1):
                    tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
                elif (datos[i,2] == 2):
                    tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2    
                tiempo.append(tiempoDiario)
                indiceNE.append(i)
                tiempoDiario=0
                dias += 1
        else: #Se queda sin paquetes: vuelve el cartero a la oficina
            print>>f_fifo,"===================CARTERO :VUELVO A LA OFICINA POR MAS PAQUETES============================="
            cartasAc = 0 #De paso carga cartas
            paqAc= paqAc - carro #Siempre va a haber mas paquetes acumulados que espacio en el carro.
            viajes += 1
            if (datos[i,2] == 0):
                tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
            elif (datos[i,2] == 1):
                tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
            elif (datos[i,2] == 2):
                tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
        
            
        i += 1    
    if i<len(datos): #Se queda sin cartas: vuelve el cartero a la oficina
        print>>f_fifo,"===================CARTERO:VUELVO A LA OFICINA POR MAS CARTAS============================="
        paqAc=0 #De paso carga paquetes
        cartasAc = cartasAc - bolso #Siempre va a haber mas cartas acumulados que espacio en el bolso.
        if (datos[i,2] == 0): #Depende la calle en la que esta el cartero -> el tiempo de ida y vuelta cambia.
            tiempoDiario += ((datos[i,3] + dcorreosA)/velocidad )*2
        elif (datos[i,2] == 1):
            tiempoDiario += ((datos[i,3] + dcorreosB)/velocidad )*2
        elif (datos[i,2] == 2):
            tiempoDiario += ((datos[i,3] + dcorreosC)/velocidad )*2
    else:   
        break
        	    
    viajes += 1

tiempo.append(tiempoDiario)
indiceNE.append(i)

#print >>f,("\n\n")
print >>f," ============================================================================="            
print >>f,"****FIFO****"
print >>f,"*** Informe Diario*** "
k = 0
if len(tiempo) > 4:
    feiners=4
else:
    feiners=len(tiempo)  
while k < feiners:
    print >>f,("\n")
    print >>f,"Dia ",k+1
    print >>f,"Tiempo: ", tiempo[k],"[segundos]", tiempo[k]/3600, "[horas]"
    print >>f,"Cartas sin entregar\n P1:", sum(datos[indiceNE[k]:,4]), " P2:",  sum(datos[indiceNE[k]:,5]), " P3:",  sum(datos[indiceNE[k]:,6])
    print >>f,"Paquetes sin entregar\n V1:", sum(datos[indiceNE[k]:,7]), " V2:",  sum(datos[indiceNE[k]:,8]), " V3:",  sum(datos[indiceNE[k]:,9])
    k += 1

print >>f,("\n")
print >>f,("\n")

if len(tiempo) > 4:
    print >>f,"Se necesitan", len(tiempo), "dias para entregar todas las cartas"
    
print >>f,"Tiempo total para los dias laborables", sum(tiempo[0:feiners+1]), "[segundos]", sum(tiempo[0:feiners+1])/3600,"[horas]"
print >>f,"Dias trabajado (dias necesarios)", feiners, "(",dias +1,")"
print >>f,"Viajes realizados", viajes

print "===================================================================================================="
print "========================================SUCCESFULL EXECUTION========================================"
print "Files generated:"
print "*** output:",outFile
print "*** FIFO (Log):",fifo
print "*** SFJ (Log):",sjf
print "*** Priority (Log):", prioridad
print "===================================================================================================="
print "===================================================================================================="

f.close()
f_fifo.close()

