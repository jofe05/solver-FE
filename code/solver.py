
bolso = 150
carro = 300
velocidad = 1.4
tcarta = 120
tpaquete = 300
jornada = 21600
dcorreosA = 50
dcorreosB = 120
dcorreosC = 140
volA = 15
volB = 25
volC = 35


import numpy as np
datos  = np.loadtxt("../data/distrCartasVol.csv", dtype = int, delimiter = ',')
f=open('../data/log.txt', 'w')
#******* SJF *****************

print "Inicianilizando Variables - PARA SJF"
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
        #print "paqA",paqAc, "<", "carro",carro 
        if (paqAc < carro):
            print "Cartas acumuladas ",cartasAc
            print "Volumen acumulado ",paqAc
            print "Estoy en casa", datos[i,1]
            print "Estoy en calle", datos[i,2]
            print "Tengo que entregar ", sum(datos[i,4:7]),"cartas en esta casa"
            print "Tengo que entregar ", sum(datos[i,7:]),"paquetes en esta casa"

            
            cartasAc = sum(datos[i,4:7]) + cartasAc
        
            if ((sum(datos[i,4:7]) > 0) or (sum(datos[i,7:])>0)):
                if (datos[posAnterior,2] == datos[i,2]):   
                    tiempoDiario += (datos[i,3] - datos[posAnterior,2])/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                paqAc += datos[i,7]*volA + datos[i,8]*volB + datos[i,9]*volC
                posAnterior = i 
            
            if tiempoDiario >= jornada:            
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
print >>f," ============================================================================="            
print >>f, "***SFJ***"
print >>f, "*** Informe Diario*** "
k = 0
if len(tiempo) > 3:
    feiners=3
else:
    feiners=len(tiempo)   
while k <= feiners:
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
 
#******* PRIORIDAD *****************

print "Inicianilizando Variables - PARA Prioridad"
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
        #print "paqA",paqAc, "<", "carro",carro 
        if (paqAc < carro):
            print "Cartas acumuladas ",cartasAc
            print "Volumen acumulado ",paqAc
            print "Estoy en casa", datos[i,1]
            print "Estoy en calle", datos[i,2]
            print "Tengo que entregar ", sum(datos[i,4:7]),"cartas en esta casa"
            print "Tengo que entregar ", sum(datos[i,7:]),"paquetes en esta casa"

            
            cartasAc = sum(datos[i,4:7]) + cartasAc
        
            if ((sum(datos[i,4:7]) > 0) or (sum(datos[i,7:])>0)):
                if (datos[posAnterior,2] == datos[i,2]):   
                    tiempoDiario += (datos[i,3] - datos[posAnterior,2])/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                paqAc += datos[i,7]*volA + datos[i,8]*volB + datos[i,9]*volC
                posAnterior = i 
            
            if tiempoDiario >= jornada:            
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
print >>f," ============================================================================="            
print >>f, "***SFJ***"
print >>f, "*** Informe Diario*** "
k = 0
if len(tiempo) > 3:
    feiners=3
else:
    feiners=len(tiempo)   
while k <= feiners:
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
print "Inicianilizando Variables - FIFO"
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
        print "paqA",paqAc, "<", "carro",carro 
        if (paqAc < carro):
            print "Cartas acumuladas ",cartasAc
            print "Volumen acumulado ",paqAc
            print "Estoy en casa", datos[i,1]
            print "Estoy en calle", datos[i,2]
            print "Tengo que entregar ", sum(datos[i,4:7]),"cartas en esta casa"
            print "Tengo que entregar ", sum(datos[i,7:]),"paquetes en esta casa"

            
            cartasAc = sum(datos[i,4:7]) + cartasAc
        
            if ((sum(datos[i,4:7]) > 0) or (sum(datos[i,7:])>0)):
                if (datos[posAnterior,2] == datos[i,2]):   
                    tiempoDiario += (datos[i,3] - datos[posAnterior,2])/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 1):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosB - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                elif ((abs(datos[posAnterior,2] - datos[i,2])) == 2):
                    tiempoDiario += (datos[i,3] + datos[posAnterior,3] + dcorreosC - dcorreosA)/velocidad + sum(datos[i,4:7])*tcarta + sum(datos[i,7:])*tpaquete 
                paqAc += datos[i,7]*volA + datos[i,8]*volB + datos[i,9]*volC
                posAnterior = i 
            
            if tiempoDiario >= jornada:            
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
            #print "*****VUELVO A LA OFICINA**********"
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
        #print "*****VUELVO A LA OFICINA**********"
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

print >>f,("\n\n")
print >>f," ============================================================================="            
print >>f,"****FIFO****"
print >>f,"*** Informe Diario*** "
k = 0
if len(tiempo) > 3:
    feiners=3
else:
    feiners=len(tiempo)  
while k <= feiners:
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

f.close()

