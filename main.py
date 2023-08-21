from fastapi import FastAPI, HTTPException
import sdk
import os
from mangum import Mangum
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


##############################################################################
#   Ambiente                                                    ##############
###############################################################################
stage = os.getenv("STAGE")
if stage is None:
    stage = "dev"
else:
    stage = os.getenv("STAGE")
#### End Ambiente ##############

#app = FastAPI()
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="seed-fast-api", openapi_prefix=openapi_prefix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   


@app.get("/hello/{company}")
def hello_world(company: str):
    if company == 'JA':
        response_service = "Hello World {}".format(company)
        return {"data": response_service}
    raise HTTPException(status_code=401, detail="User not authenticate")

###############################################################################
#   Select con conx para postgrest                                                   #
###############################################################################
@app.get("/select")
def conexion_postgres():
    query = "SELECT * FROM public.test"
    response_query = sdk.executeQueryPostgresSelect(query, str(stage))
    return {"data": list(response_query)}

@app.get("/AGENCIAS")
def conexion_postgres():
    print("OpcionesOrder")
    query = "select codage ,nomage,TIPOCONS from public.AGENCIAS"
    response_query = sdk.executeQueryPostgresSelect(query, str(stage))
  
    return {"data": list(response_query)}

@app.get("/GET_OCUPACION")
def conexion_postgres():
    print("OpcionesOrder")
    query = "select * from ocupacion"
    response_query = sdk.executeQueryPostgresSelect(query, str(stage))
  
    return {"data": list(response_query)}

@app.get("/api/busqueda/paciente/{busqueda}/{tipide}")
def conexion_postgres(busqueda:str,tipide:str):
 
    query = "select * from paciente where codpac='"+str(busqueda)+"' and tipide='"+str(tipide)+"'"
    response_query = sdk.executeQueryPostgresSelect(query, str(stage))
  
    return {"data": list(response_query)}


# @app.get("/AGENCIAS")
# def conexion_postgres2():
#     # print("###########");
#     query = "select codage ,nomage  from public.agencias"
#     response_query = sdk.executeQueryPostgresSelect(query, str(stage))
#     return {"data": list(response_query)}

# ******************** cambiar un resultado *****************************************
@app.put('/resultado/update/{id}')
def update_data(data: dict,id:str):
            query="update resultado set resultado=upper(%s),usuario=upper(%s),fecha=CURRENT_TIMESTAMP where id=" + id
            sdk.updatePostgres(query, data,"prd")

@app.delete('/resultado/delete/{id}')
def delete_data(data: dict,id:str):
        query = "delete from resultado where id=" + id
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
        }
            



@app.post("/insert")
def inser_data(data: dict):

    query="INSERT INTO test(nombre,apellido) VALUES (%s, %s)"
    #data= {'nombre':'cantillo','apellido':'cantilloss'}

    sdk.insertPostgres(query, data,"prd")

@app.delete("/delete/{nombre}")
def delete_data(nombre:str):
    query = "delete FROM public.test where nombre='{}'".format(nombre)
    response_query = sdk.deletePostgres(query, str(stage))
    print(response_query)
    return {
        "statusCode": 200,
        "resultado": "success"
    }



################################### LISTAS DE VALORES ##############################
@app.get('/lovpaises/{patron}')
def conexion_postgres(patron:str):
        pat = patron.upper()
        filtro = "'%{}%'".format(pat);
        # print(filtro)
        query = "select id,nombre from paises where 1=1 and nombre like " + filtro
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}

####################################### cruds ##########################################################################33

####################################### TABLA DIAGNOSTICOS ##########################################################################33
@app.post('/diagnostico/update/{coddiagnostico}')
def update_data(data: dict,coddiagnostico:str):
        query="update diagnostico set  where coddiagnostico='{}'".format(coddiagnostico)
        sdk.insertPostgres(query, data,"prd")


@app.get('/diagnostico/select')
def conexion_postgres():
        query = 'select * from diagnostico' 
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}


@app.post('/diagnostico/insert')
def inser_data(data: dict):
        query='insert into diagnostico(coddiagnostico,nomdiagnostico) VALUES (%s,%s)'
        sdk.insertPostgres(query, data,"prd")

@app.delete('/diagnostico/delete/{coddiagnostico}')
def delete_data(coddiagnostico:str):
        query = "delete FROM test where coddiagnostico='{}'".format(coddiagnostico)
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
    }

################################### EMPRESAS ##############################
@app.put('/empresas/update/{id}')
def update_data(data: dict,id:str):
            query="update empresas set nombre=%s,pais=%s where id='{}'".format(id)
            sdk.updatePostgres(query, data,"prd")


@app.get('/empresas/select')
def conexion_postgres():
        query = 'SELECT id,nombre,pais from empresas order by 1' 
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}


@app.post('/empresas/insert')
def insert_data(data: dict):
        query='insert into empresas(id,nombre,pais) values (%s,%s,%s)'
        sdk.insertPostgres(query, data,"prd")

@app.delete('/empresas/delete/{id}')
def delete_data(id:str):
        query = "delete FROM empresas where id='{}'".format(id)
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
        }

###################### TODO SOBRE RESULTADOS ###########################################



# ********************* eliminar un item de resultado **********************************

@app.delete('/resultado/delete/{id}')
def delete_data(data: dict,id:str):
        query = "delete from resultado where id=" + id
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
        }


# ******************** cambiar un resultado *****************************************
@app.put('/resultado/update/{id}')
def update_data(data: dict,id:str):
            query="update resultado set resultado=upper(%s),usuario=upper(%s),fecha=CURRENT_TIMESTAMP where id=" + id
            sdk.updatePostgres(query, data,"prd")

# ******************** firmar un resultado *****************************************
@app.post('/resultado/firmar/{age}/{ord}')
def update_data(data: dict,age:str,ord:str):
    user =  data['user']
    tipo =  data['tipo']
    seq = data['tipo']
    medico = ''

    qry = "select codmedico,nommedico from medicos where usuario='" + user + "'"
    response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_med=''
    va_nom=''
    for obj in response_med:
        va_med = obj['codmedico']
        va_nom = obj['nommedico']
    qry = "select tipofirma from agencias where codage='" + age + "'"
    response_age = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_age:
        va_tipof = obja['tipofirma']


    if (va_med != ''):
        if (tipo=='E'):
            query="update laborden set medfirmae='" + medico + "'" 
            query = query + ",horfirmae=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
            sdk.updatePostgres(query, data,"prd")
        else:
            if (va_tipof == 'O'):
                qry = "update laborden set medfirma='" + medico + "'" 
                qry = qry + ",horfirma=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
                sdk.updatePostgres(qry, data,"prd")
            else:
                qry = "update labordendet set medfirmad='" + medico +"'"
                qry = qry + ",horfirmad=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "' and seq=" + seq
                sdk.updatePostgres(qry, data,"prd") 
        exitoso = 'SI'
        mensaje = 'Gracias por su firma, Dr(a) ' + va_nom
    else: # es un usuario sin medico asociado
        mensaje = 'Usuario No habilitado para Firmar'
        exitoso = 'NO'     
    if (exitoso == 'SI'):
         resu = 'success'
    else:
         resu = 'failure'

    return {"statusCode": 200,"resultado": resu,"mensaje":mensaje}

     
                     

####################### servicio resultados IMPRESION ##################################

@app.get('/resultado/find/{codage}/{numorden}')
def conexion_postgres(codage:str,numorden:str):


   #Direccion y telefonos sede ppal
    qry = "select texto,orden from textos where cod='PPAL' order by orden "
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    # Bolos del tope y piede la pagina
    respuesta=[]
    va_bolo_examen = ''
    va_respie = ''
    va_restop = ''
    qry = "select cod,texto from textos where cod in ('RESPIE','RESTOP')"
    response_bolo = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response_bolo:
        if (obj['cod'] == 'RESPIE'):
            va_respie = obj['texto']
       # if (obj['cod'] == 'RESTOP'):    
       #     va_restop = obj['texto']

    # Dtaos del paciente
    qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden=to_number('"+numorden+"','9999999999999999') "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
    response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
    datapac={}
    for obj in response_query0:
        va_ordenl = obj['ordenl'] 
        va_tip = obj['tipide']
        va_codpac = obj['codpac']
        va_nombre = obj['nombre']
        va_sexo = obj['sexo']
        va_edad = obj['edadf']
        va_tel = obj['tel']
        va_agencia = obj['nomage']
        va_med = obj['nommedico']
        va_fec = obj['fecorden']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_medfirma = obj['medfirma']
        va_horfirma = obj['horfirma']

        datapac = {"ordenl":va_ordenl,"codpac":va_codpac,"nombre":va_nombre,"sexo":va_sexo,"edad":va_edad,"tel":va_tel,"age":va_agencia,"medico":va_med,"empresa":va_nomemp,"fecorden":va_fecorden,"medfirma":va_medfirma,"horfirma":va_horfirma}

    # los distintos examenes de la orden de laboratorio
    qry = "select distinct r.seq,r.cdgexamen,e.nombre as nomexamen,r.usuario,medfirmad,horfirmad  "
    qry = qry + "from resultado r,examen e, labordendet d "
    qry = qry + "where r.cdgexamen=e.cdgexamen  " 
    qry = qry + "and r.codage='"+codage+"' and r.numorden=to_number('"+numorden+"','9999999999999999') "
    qry = qry +" and r.ordenl = d.ordenl and r.seq= d.seq and r.resultado is not null"    
    response_query = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    for obj in response_query:
        va_examen = obj['cdgexamen']
        va_nomexamen = obj['nomexamen']
        va_usuario = obj['usuario']
        va_seq = obj['seq']
        va_medfirmad = obj['medfirmad']
        va_horfirmad = obj['horfirmad']

        va_bolo_examen = ''
        qry = "select texto from textos where aplica like '%"+va_examen+"%'"
        response_query_textos = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_query_textos:
            va_bolo_examen = obj['texto']
        

        # los distintos analisis del examen (seq) de la orden de laboratorio            
        qry = "select r.cdganalisis, a.nombre as nomanalisis, "
        qry = qry + "r.resultado,r.fecha,r.tipores,r.resnum,r.unicodi,r.usuario  "
        qry = qry + " ,getvalnormals('"+va_fec+"','"+va_tip+"','"+va_codpac+"',r.cdgexamen,r.cdganalisis,'"+codage+"','"+numorden+"') as valnormal  "
        qry = qry + " ,resultadoant('"+va_fec+"',r.cdgexamen,r.cdganalisis,'"+va_tip+"','"+va_codpac+"') as resant  "
        qry = qry + " from resultado r,examen e,analisis a "
        qry = qry + " where r.cdgexamen=e.cdgexamen and r.cdganalisis=a.cdganalisis " 
        qry = qry + " and r.codage='"+codage+"' and r.numorden=to_number('"+numorden+"','9999999999999999') and r.seq='" + str(va_seq) + "' " 
        qry = qry + " and r.resultado is not null "

        response_query_ex = sdk.executeQueryPostgresSelect(qry, str(stage))
        dataexamen = {"examen":va_examen,"nomexamen":va_nomexamen,"usuario":va_usuario,"detalle":list(response_query_ex),"bolo":va_bolo_examen,"medfirmad":va_medfirmad,"horfirmad":va_horfirmad}
        respuesta.append(dataexamen)
    # calcular los valores de referencia
    # calcular el resultado anterior
    return {"statusCode": 200,"resultado": "success","paciente":datapac,"grupo": list(respuesta),"respie":va_respie,"sedeppal":list(response_querysp)}





####################### ecabezado del resultado ##################################

@app.get('/resultadoencabezado/find/{codage}/{numorden}')
def conexion_postgres(codage:str,numorden:str):
    try:
    #Direccion y telefonos sede ppal
        qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
        qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma,medfirmae,horfirmae "  
        qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
        qry = qry + "        where o.codage='"+codage+"' and o.numorden="+numorden+" "
        qry = qry + "        and o.codpac=p.codpac "
        qry = qry + "        and o.codemp=e.codemp "
        qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
        response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

        datapac = {};
        for obj in response_querysp:
            va_fecorden = obj['fecorden']
            va_nompac = obj['nombre']
            va_edadf = obj['edadf']
            va_sexo = obj['sexo']
            datapac = {'fecorden':va_fecorden,'nompac':va_nompac,'edadf':va_edadf,'sexo':va_sexo}
        
        qry2 = "select d.cdgexamen,e.nombre,d.seq,d.medfirmad, d.horfirmad from labordendet d,examen e "
        qry2 = qry2 + " where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999') and d.cdgexamen=e.cdgexamen "
        response_exam = sdk.executeQueryPostgresSelect(qry2, str(stage))

        # print(list(response_exam))
        
        return {"statusCode": 200,"resultado": "success","paciente":datapac,"examenes": list(response_exam) }
    except:
	    return {"statusCode": 200,"resultado": "fails"}

####################### Detalle del resultado ####################################

   # los distintos analisis del examen (seq) de la orden de laboratorio            
@app.get('/resultadodetalle/find/{codage}/{numorden}/{seq}')
def conexion_postgres(codage:str,numorden:str,seq:str):

   #Direccion y telefonos sede ppal
    qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden="+numorden+" "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico  "
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    datapac = {};
    for obj in response_querysp:
        va_ordenl = obj['ordenl'] 
        va_tip = obj['tipide']
        va_codpac = obj['codpac']
        va_nombre = obj['nombre']
        va_sexo = obj['sexo']
        va_edad = obj['edadf']
        va_tel = obj['tel']
        va_agencia = obj['nomage']
        va_med = obj['nommedico']
        va_fec = obj['fecorden']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_medfirma = obj['medfirma']
        va_horfirma = obj['horfirma']

        datares = [];
        regres = {}

        # los analisis del examen en esa orden
        qry = "select d.cdgexamen,d.seq,a.cdganalisis,a.nombre as nomanalisis, "
        qry = qry + " '' as resultado,'' as fecha,a.tipores ,'' as resnum,a.unicodi ,'' as usuario,'' as valnormal,'' as resant, "
        qry = qry + " '' as fechamaq,a.tiponorm,getvalayuda(a.cdgexamen,a.cdganalisis) valayuda, d.seq ,a.orden"
        qry = qry + " ,getvalnormals('"+va_fec+"','"+va_tip+"','"+va_codpac+"',d.cdgexamen,a.cdganalisis,'"+codage+"','"+numorden+"') as valnormal  "
        qry = qry + " ,resultadoant('"+va_fec+"',d.cdgexamen,a.cdganalisis,'"+va_tip+"','"+va_codpac+"') as resant "
        qry = qry + "  from labordendet d,examen e,analisis a  "
        qry = qry + " where d.cdgexamen=e.cdgexamen and e.cdgexamen=a.cdgexamen "  
        qry = qry + " and d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999999')  and d.seq="+ seq +" order by a.orden "
        response_query_det = sdk.executeQueryPostgresSelect(qry, str(stage))

        for obj in response_query_det:
            va_seq = obj['seq'] 
            va_anali = obj['cdganalisis']
            va_nomanali = obj['nomanalisis']
            va_valayuda = obj['valayuda']
            va_uni = obj['unicodi']
            va_tiponor = obj['tiponorm']
            va_examen = obj['cdgexamen']
            va_valnorm = obj['valnormal']
            va_resant = obj['resant']
            va_orden = obj['orden']

            regres = {'id':0,'cdganalisis':va_anali,'nomanalisis':va_nomanali,'orden':va_orden,
            'resultado':'','fecha':'','tipores':'','resnum':'',
            'unicodi':'','usuario':'','seq':va_seq,'valnormal':va_valnorm,
            'resant': va_resant,'fehamaq':'','tiponorm':'' , 'valayuda': va_valayuda}

            # el resultado individual de cada analisis
            qry = "select r.id,r.resultado,to_char(r.fecha,'ddmmyyyy') as fecha, "
            qry = qry + "r.tipores,r.resnum,r.unicodi,r.usuario ,r.seq,r.fechamaq  "
            qry = qry + " from resultado r "
            qry = qry + " where r.codage='"+codage+"' and r.numorden=to_number('"+numorden+"','9999999999999999') and r.seq=" + str(va_seq) 
            qry = qry +" and r.cdgexamen='"+ va_examen +"' and r.cdganalisis = '"+ va_anali +"' and r.seq="+ seq +" order by r.id" 

            response_query_an = sdk.executeQueryPostgresSelect(qry, str(stage))
            for res in response_query_an:
                va_id = res['id'] 
                va_resu = res['resultado']
                va_fecha = res['fecha']
                va_tipores = res['tipores']
                va_resnum=res['resnum']
                va_uni = res['unicodi']
                va_user = res['usuario']
                va_fechamaq = res['fechamaq']
                regres['id'] = va_id
                regres['resultado'] = va_resu
                regres['fecha'] = va_fecha
                regres['tipores'] = va_tipores
                regres['resnum'] = va_resnum
                regres['usuario'] = va_user
                regres['fechamaq']= va_fechamaq
            datares.append(regres)

    return {"statusCode": 200,"resultado": "success","analisis": list(datares) }


####################### servicio opciones por usuario  ##################################
@app.get('/usuarioopciones/find/{usuario}')
def conexion_postgres(usuario:str):

   #Carpetas
    qry = "select distinct o.carpeta "
    qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
    qry = qry+" where u.usuario='"+ usuario +"' "
    qry = qry+" and u.usuario=ur.usuario "
    qry = qry+" and ur.role = r.role  "
    qry = qry+" and r.opcion = o.opcion " 
    qry = qry+" order by 1 "
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    datamenu = {}
    listado = []

    for obj in response:
        va_carpeta = obj['carpeta'] 
        # opciones de la carpeta
        qry = "select o.opcion,o.ruta, o.nombre "
        qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
        qry = qry+" where u.usuario='"+ usuario +"' "
        qry = qry+" and u.usuario=ur.usuario "
        qry = qry+" and ur.role = r.role  "
        qry = qry+" and r.opcion = o.opcion "
        qry = qry+" and o.carpeta ='"+va_carpeta+"' and o.mostrar='S'" 
        qry = qry+" order by o.orden "    
        response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
        datamenu = {"carpeta":va_carpeta,"opciones":list(response_query0)}
        listado.append(datamenu)

    return {"statusCode": 200,"resultado": "success","carpetas": list(listado)}

####################### servicio opciones sin jerarquia  ##################################
@app.get('/usuarioopcioneslist/find/{usuario}')
def conexion_postgres(usuario:str):

   #Carpetas
    qry = "select o.opcion,o.ruta "
    qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
    qry = qry+" where u.usuario='"+ usuario +"' "
    qry = qry+" and u.usuario=ur.usuario "
    qry = qry+" and ur.role = r.role  "
    qry = qry+" and r.opcion = o.opcion "
    qry = qry+" and o.mostrar='S'" 
    qry = qry+" order by o.orden "    
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    datamenu = {}
    listado = []

    return {"statusCode": 200,"resultado": "success","opciones": list(response)}


# ********** Servicios CRUD ********* 

 # ---------------- tabla: diagnostico---------- 
# Endpoint Update 
@app.put('/diagnostico/update/{id}') 
def update_data(data: dict,id:str):  
	query="update diagnostico set nomdiagnostico=%s  where coddiagnostico='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/diagnostico/select') 
def conexion_postgres(): 
	query = 'SELECT coddiagnostico,nomdiagnostico from diagnostico order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/diagnostico/insert') 
def insert_data(data: dict): 
	query='insert into diagnostico(coddiagnostico,nomdiagnostico) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/diagnostico/delete/{id}') 
def delete_data(id: str): 
	query="delete from diagnostico where coddiagnostico='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: medicos---------- 
# Endpoint Update 
@app.put('/medicos/update/{id}') 
def update_data(data: dict,id:str):  
	query="update medicos set nommedico=%s,ccmedico=%s,espmedico=%s,perfil=%s,celular=%s,tel=%s,ciudad=%s,codundnegocio=%s,usuario=%s,firma=%s,presentacion=%s  where codmedico='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/medicos/select') 
def conexion_postgres(): 
	query = 'SELECT codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion from medicos order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/medicos/insert') 
def insert_data(data: dict): 
	query='insert into medicos(codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/medicos/delete/{id}') 
def delete_data(id: str): 
	query="delete from medicos where codmedico='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: undnegocio---------- 
# Endpoint Update 
@app.put('/undnegocio/update/{id}') 
def update_data(data: dict,id:str):  
	query="update undnegocio set nomundnegocio=%s  where codundnegocio='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/undnegocio/select') 
def conexion_postgres(): 
	query = 'SELECT codundnegocio,nomundnegocio from undnegocio order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/undnegocio/insert') 
def insert_data(data: dict): 
	query='insert into undnegocio(codundnegocio,nomundnegocio) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/undnegocio/delete/{id}') 
def delete_data(id: str): 
	query="delete from undnegocio where codundnegocio='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: vinculacion---------- 
# Endpoint Update 
@app.put('/vinculacion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update vinculacion set nomvic=%s  where vincpac='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/vinculacion/select') 
def conexion_postgres(): 
	query = 'SELECT vincpac,nomvic from vinculacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/vinculacion/insert') 
def insert_data(data: dict): 
	query='insert into vinculacion(vincpac,nomvic) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/vinculacion/delete/{id}') 
def delete_data(id: str): 
	query="delete from vinculacion where vincpac='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: tipomuestra---------- 
# Endpoint Update 
@app.put('/tipomuestra/update/{id}') 
def update_data(data: dict,id:str):  
	query="update tipomuestra set nombre=%s  where tipmues='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/tipomuestra/select') 
def conexion_postgres(): 
	query = 'SELECT tipmues,nombre from tipomuestra order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/tipomuestra/insert') 
def insert_data(data: dict): 
	query='insert into tipomuestra(tipmues,nombre) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/tipomuestra/delete/{id}') 
def delete_data(id: str): 
	query="delete from tipomuestra where tipmues='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: ocupacion---------- 
# Endpoint Update 
@app.put('/ocupacion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update ocupacion set nomocu=%s  where codocu='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/ocupacion/select') 
def conexion_postgres(): 
	query = 'SELECT codocu,nomocu from ocupacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/ocupacion/insert') 
def insert_data(data: dict): 
	query='insert into ocupacion(codocu,nomocu) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/ocupacion/delete/{id}') 
def delete_data(id: str): 
	query="delete from ocupacion where codocu='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: labseccion---------- 
# Endpoint Update 
@app.put('/labseccion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labseccion set nombre=%s,gruposeccion=%s,peso=%s  where codseccion='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labseccion/select') 
def conexion_postgres(): 
	query = 'SELECT codseccion,nombre,gruposeccion,peso from labseccion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labseccion/insert') 
def insert_data(data: dict): 
	query='insert into labseccion(codseccion,nombre,gruposeccion,peso) values (%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labseccion/delete/{id}') 
def delete_data(id: str): 
	query="delete from labseccion where codseccion='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: agencias---------- 
# Endpoint Update 
@app.put('/agencias/update/{id}') 
def update_data(data: dict,id:str):  
	query="update agencias set nomage=%s,ciuage=%s,depage=%s,dirage=%s,telage=%s,tipocons=%s,docpac=%s,resdian=%s,reqfd=%s,sinlogo=%s,predian=%s,maxfecres=%s,maxconsres=%s,tipofirma=%s,architect_prefijo=%s,proc=%s,codager=%s,domi=%s  where codage='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/agencias/select') 
def conexion_postgres(): 
	query = 'SELECT codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi from agencias order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/agencias/insert') 
def insert_data(data: dict): 
	query='insert into agencias(codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/agencias/delete/{id}') 
def delete_data(id: str): 
	query="delete from agencias where codage='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: examen---------- 
# Endpoint Update 
@app.put('/examen/update/{id}') 
def update_data(data: dict,id:str):  
	query="update examen set nombre=%s,codseccion=%s,cut=%s,soat=%s,nivexa=%s,nomcorto=%s,duracion=%s,tecnicas=%s,condiciones=%s,tipmues=%s,duraciont=%s,tiposerv=%s,inactiva=%s,entlun=%s,entmar=%s,entmie=%s,entjue=%s,entvie=%s,entsab=%s,entdom=%s,noproclun=%s,noprocmar=%s,noprocmie=%s,noprocjue=%s,noprocvie=%s,noprocsab=%s,noprocdom=%s  where cdgexamen='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/examen/select') 
def conexion_postgres(): 
	query = 'SELECT cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom from examen order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/examen/insert') 
def insert_data(data: dict): 
	query='insert into examen(cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/examen/delete/{id}') 
def delete_data(id: str): 
	query="delete from examen where cdgexamen='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: mae_unid---------- 
# Endpoint Update 
@app.put('/mae_unid/update/{id}') 
def update_data(data: dict,id:str):  
	query="update mae_unid set uni_desc=%s  where uni_codi='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/mae_unid/select') 
def conexion_postgres(): 
	query = 'SELECT uni_codi,uni_desc from mae_unid order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mae_unid/insert') 
def insert_data(data: dict): 
	query='insert into mae_unid(uni_codi,uni_desc) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/mae_unid/delete/{id}') 
def delete_data(id: str): 
	query="delete from mae_unid where uni_codi='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
# ---------------- tabla: analisis---------- 
# Endpoint Update 
@app.put('/analisis/update/{id}') 
def update_data(data: dict,id:str):  
	query="update analisis set cdgexamen=%s,cdganalisis=%s,nombre=%s,unicodi=%s,tipores=%s,cdganalisisa=%s,cdganalisisb=%s,tiponorm=%s,aplica=%s,redondear=%s,redondeo=%s,ajusta=%s,tecnica=%s,grupo=%s,orden=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/analisis/select/{exa}') 
def conexion_postgres(exa: str): 
	query = "SELECT id,cdgexamen,cdganalisis,nombre,unicodi,tipores,cdganalisisa,cdganalisisb,tiponorm,aplica,redondear,redondeo,ajusta,tecnica,grupo,orden from analisis where cdgexamen='"+ exa +"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/analisis/insert') 
def insert_data(data: dict): 
	query='insert into analisis(cdgexamen,cdganalisis,nombre,unicodi,tipores,cdganalisisa,cdganalisisb,tiponorm,aplica,redondear,redondeo,ajusta,tecnica,grupo,orden) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/analisis/delete/{id}') 
def delete_data(id: str): 
	query="delete from analisis where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))     

 # ---------------- tabla: labvalores---------- 
# Endpoint Update 
@app.put('/labvalores/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labvalores set cdgexamen=%s,cdganalisis=%s,tecla=%s,resultado=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labvalores/select') 
def conexion_postgres(): 
	query = 'SELECT id,cdgexamen,cdganalisis,tecla,resultado from labvalores order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labvalores/insert') 
def insert_data(data: dict): 
	query='insert into labvalores(id,cdgexamen,cdganalisis,tecla,resultado) values (%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labvalores/delete/{id}') 
def delete_data(id: str): 
	query="delete from labvalores where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))   
 # ---------------- tabla: feriados---------- 
# Endpoint Update 
@app.put('/feriados/update/{id}') 
def update_data(data: dict,id:str):  
	query="update feriados set per=%s,fecha=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/feriados/select') 
def conexion_postgres(): 
	query = 'SELECT id,per,fecha from feriados order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/feriados/insert') 
def insert_data(data: dict): 
	query='insert into feriados(id,per,fecha) values (%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/feriados/delete/{id}') 
def delete_data(id: str): 
	query="delete from feriados where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))


 # ---------------- tabla: labcombo---------- 
# Endpoint Update 
@app.put('/labcombo/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labcombo set nombre=%s,cdgexamen=%s  where codcombo='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labcombo/select') 
def conexion_postgres(): 
	query = 'SELECT codcombo,nombre,cdgexamen from labcombo order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombo/insert') 
def insert_data(data: dict): 
	query='insert into labcombo(codcombo,nombre,cdgexamen) values (%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labcombo/delete/{id}') 
def delete_data(id: str): 
	query="delete from labcombo where codcombo='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: labcombodet---------- 
# Endpoint Update 
@app.put('/labcombodet/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labcombodet set codcombo=%s,cdgexamen=%s,valor=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labcombodet/select') 
def conexion_postgres(): 
	query = 'SELECT id,codcombo,cdgexamen,valor from labcombodet order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombodet/insert') 
def insert_data(data: dict): 
	query='insert into labcombodet(id,codcombo,cdgexamen,valor) values (%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labcombodet/delete/{id}') 
def delete_data(id: str): 
	query="delete from labcombodet where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))    

###################### Servicios de la orden de laboratorio #############################

@app.get('/precio/find/{codemp}/{dep}/{examen}')
def conexion_postgres(codemp:str,examen:str,dep:str):

    qry = "select nombre,nivexa from examen where cdgexamen='"+examen+"'" 
    response_queryex = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_nivelex =''
    for obj in response_queryex:
        va_nivelex = obj['nivexa']
        va_nomexamen = obj['nombre']


   #obtenemos la lista de la empresa
    va_desce = 0
    qry = "select codlista,desce from labempresa where codemp ='" + codemp +"'" 
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response_querysp:
        va_codlista = obj['codlista'] 
        va_desce = obj['desce']
    if dep != '':
        qry = "select valor from labtarifasdep where codlista ='" + va_codlista +"' and cdgexamen='"+examen+"' and coddep='"+dep+"'" 
        response_querysd = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_valor = -1
        for obj in response_querysd:
            va_valor = obj['valor']    
    if (va_valor == -1):
        qry = "select valor from labtarifas where codlista ='" + va_codlista +"' and cdgexamen='"+examen+"'" 
        response_querysl = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_valor = -1
        for obj in response_querysl:
            va_valor = obj['valor']
	# busco descuento adicional x convenio empresa    
    qry = "select descc,nivel from examenemp where  codemp ='" + codemp +"' and cdgexamen='"+examen+"'" 
    response_queryse = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_descc = 0
    va_nivele =''
    for obj in response_queryse:
        va_descc = obj['descc']
        va_nivele = obj['nivel']
    if (va_nivele ==''):
        va_nivele = va_nivelex # tomamos el nivel del examen
    if (va_nivele !=''): # si ya hay nivel
        qry = "select descn from nivemp where codemp='" + codemp +"' and " + str(va_nivele) + " between nivmin and nivmax " 
        response_queryniv = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_descn = 0
        for obj in response_queryniv:
            va_descn = obj['descn']    
    va_destotal = va_desce + va_descc + va_descn

    return {"statusCode": 200,"resultado": "success", "nombre":va_nomexamen,"valor":va_valor,"descuento":va_destotal }

# ---------------- tabla: mediospago---------- 
# Endpoint Update 
@app.put('/mediospago/update/{id}') 
def update_data(data: dict,id:str):  
	query="update mediospago set desmed=%s  where codmed='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/mediospago/select') 
def conexion_postgres(): 
	query = 'SELECT codmed,desmed from mediospago order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mediospago/insert') 
def insert_data(data: dict): 
	query='insert into mediospago(codmed,desmed) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/mediospago/delete/{id}') 
def delete_data(id: str): 
	query="delete from mediospago where codmed='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: labordenpago---------- 
# Endpoint Update 
@app.put('/labordenpago/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labordenpago set fecha=CURRENT_TIMESTAMP,codage=%s,numorden=%s,codmed=%s,valor=%s,pend=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labordenpago/select/{miage}/{miord}') 
def conexion_postgres(miage:str,miord=str): 
	query = "SELECT id,codage,numorden,codmed,valor,pend,fecha from labordenpago where codage='"+ miage + "' and numorden=" + miord + " order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labordenpago/insert') 
def insert_data(data: dict): 
	query='insert into labordenpago(codage,numorden,codmed,valor,pend,fecha) values (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labordenpago/delete/{id}') 
def delete_data(id: str): 
	query="delete from labordenpago where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
	
@app.get('/lov/{lista}')
def conexion_postgres(lista:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        query0="select '' as id, 'Seleccione una opcion' as name union "
        if (lista.lower() == 'role'):
            query = "select role as id,r.nombre as name  from roles r order by 2 "
        if (lista.lower() == 'opcion'):
            query = "select opcion as id,r.nombre as name  from opciones r order by 2 "
        if (lista.lower() =='tiposerv'):
            query = "select tipo as id,tipo||'-'||nom as name from tiposerv order by 1"
        if (lista.lower() =='labseccion'):
            query = "select codseccion as id,codseccion||'-'||nombre as name from labseccion order by 1"
        if (lista.lower() =='tipomuestra'):
            query = "select tipmues as id,tipmues||'-'||nombre as name from tipomuestra order by 1"
        if (lista.lower() =='mae_unid'):
            query = "select uni_codi as id,uni_desc as name from mae_unid order by 1"
        if (lista.lower() =='departamento'):
            query = "select coddep as id,desdep as name from maedep order by 1"
        if (lista.lower() =='ciudad'):
            query = "select codciu as id,coddep||'-'||codciu||'-'||desciu as name from maeciu order by 1"
        if (lista.lower() =='agencia'):
            query = "select codage as id,codage||'-'||nomage as name from agencias order by 1"
        if (lista.lower() =='lista'):
            query = "select codlista as id,codlista||'-'||nombre as name from lablistas order by 1"
        if (lista.lower() =='claseemp'):
            query = "select codcla as id,nombre as name from labempclase l order by 1"
        if (lista.lower() =='especialidad'):
            query = "select codespecialidades as id ,nomespecialidades as name  from especialidades order by 1"
        if (lista.lower() =='unegocio'):
            query = "select codundnegocio as id,nomundnegocio as name from undnegocio order by 1"
        if (lista.lower() =='usuario'):
            query = "select usuario as id,nombre as name from usuarios order by 1"
        if (lista.lower() =='mediospago'):
            query = "select codmed as id,desmed as name from mediospago m  order by 1"
        if (lista.lower() =='color'):
            query = "select cod as id,horai || '-'|| horaf as name from color order by 1"

        response_query = sdk.executeQueryPostgresSelect(query0 + query, str(stage))
        return {"data": list(response_query)}

@app.get("/AGENCIAS2")
def conexion_postgres3():
    print("########### OpcionesSucursal");
    query2 = "select * from AGENCIAS"
    response_query3 = sdk.executeQueryPostgresSelect(query2, str(stage))
    
    print(list(response_query3))
    print("########### END OpcionesSucursal");

    return {"data": list(response_query3)}

@app.get("/Opcioneslaempresa")
def conexion_postgres2():
    print("########### Opcioneslaempresa");
    query = "select codemp, nombre  from public.LABEMPRESA"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))
    
    #print(list(response_query2))

    return {"data": list(response_query2)}

@app.get("/GET_origen")
def conexion_postgres2():
    print("########### GET_origen");
    query = "select *  from public.laborigen"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))
    
    #print(list(response_query2))

    return {"data": list(response_query2)}

@app.get("/GET_medico")
def conexion_postgres2():
    print("########### GET_medico");
    query = "select codmedico,nommedico from public.medicos"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))
    
    #print(list(response_query2))

    return {"data": list(response_query2)}

@app.get("/GET_VINCULACION")
def conexion_postgres2():
    print("########### GET_VINCULACION");
    query = "select *  from public.vinculacion"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))

    return {"data": list(response_query2)}

@app.get("/GET_diagnostico")
def conexion_postgres2():
    query = "select *  from public.diagnostico"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))

    return {"data": list(response_query2)}

@app.get("/GET_UNDNEGOCIO")
def conexion_postgres2():
    query = "select *  from public.UNDNEGOCIO;"
    response_query2 = sdk.executeQueryPostgresSelect(query, str(stage))

    return {"data": list(response_query2)}

@app.get("/select")
def conexion_postgres():
    query = "SELECT * FROM public.test"
    response_query = sdk.executeQueryPostgresSelect(query, str(stage))
    return {"data": list(response_query)}


@app.post("/insert")
def inser_data(data: dict):

    query="INSERT INTO test(nombre,apellido) VALUES (%s, %s)"
    #data= {'nombre':'cantillo','apellido':'cantilloss'}

    sdk.insertPostgres(query, data,"prd")

@app.delete("/delete/{nombre}")
def delete_data(nombre:str):
    query = "delete FROM public.test where nombre='{}'".format(nombre)
    response_query = sdk.deletePostgres(query, str(stage))
    print(response_query)
    return {
        "statusCode": 200,
        "resultado": "success"
    }

################################## REPORTES #######################################

@app.get('/reportes/find/{rep}')
def conexion_postgres(rep:str):
    #Carpetas
    ds = {}
    qry = "select consulta,filtros,columnas,medidas from zreportes where cod=" + rep
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response:
        va_query = obj['consulta']
        response_data = sdk.executeQueryPostgresSelect(va_query, str(stage))
        va_columnas = obj['columnas']
        va_medidas = obj['medidas']
    return {"statusCode": 200,"resultado": "success","columnas":va_columnas,"medidas":va_medidas,"data": list(response_data)}



################################### LISTA DE TRABAJO ################################

@app.post('/listatrabajo')
def conexion_postgres(data: dict):
    va_where = data['where']
    print('> ' +  va_where + ' <' )
    query="select x.id,o.codage,o.numorden,x.cdgexamen,e.nombre as nomexamen , x.proc, o.tipide ,o.codpac,p.nompac ||' '||p.apepac as nompac,o.edadf, o.usuario usurecep,o.medfirma,o.horfirma,to_char(o.fecent,'ddmmyyyy') fecent,o.horent ,o.prio,o.codemp,l.nombre as nomemp,o.motivo, p.antefam  ";
    query=query+" from labordendet x,examen e,laborden o,paciente p,labempresa l "
    query=query+" where x.cdgexamen=e.cdgexamen  ";
    query=query+" and x.ordenl = o.ordenl ";
    query=query+" and o.tipide=p.tipide ";
    query=query+" and o.codpac=p.codpac and o.codemp=l.codemp and " + va_where 
    response_query = sdk.executeQueryPostgresSelect(query, "prd")
    return {"data": list(response_query)}


@app.post('/listatrabajo/proc')
def conexion_postgres(data: dict):
    va_id = data['id']
    qry = "update labordendet set proc='S' where id=%s"
    sdk.updatePostgres(qry, data,"prd")

@app.post('/listatrabajo/noproc')
def conexion_postgres(data: dict):
    va_id = data['id']
    qry = "update labordendet set proc='N' where id=%s"
    sdk.updatePostgres(qry, data,"prd")


################################### LISTAS DE VALORES ##############################
@app.get('/lovpaises/{patron}')
def conexion_postgres(patron:str):
        pat = patron.upper()
        filtro = "'%{}%'".format(pat);
        # print(filtro)
        query = "select id,nombre from paises where 1=1 and nombre like " + filtro
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}


################################### LISTAS MULTIPROPOSITO ##############################

# sirve para cualquiera de las tablas ya mapeadas y siempre devuelve 2 columnas, COD, NOM
@app.get('/lov/{lista}')
def conexion_postgres(lista:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        query0="select '' as id, 'Seleccione una opcion' as name union "
        if (lista.lower() == 'role'):
            query = "select role as id,r.nombre as name  from roles r order by 2 "
        if (lista.lower() == 'opcion'):
            query = "select opcion as id,r.nombre as name  from opciones r order by 2 "
        if (lista.lower() =='tiposerv'):
            query = "select tipo as id,tipo||'-'||nom as name from tiposerv order by 1"
        if (lista.lower() =='labseccion'):
            query = "select codseccion as id,codseccion||'-'||nombre as name from labseccion order by 1"
        if (lista.lower() =='tipomuestra'):
            query = "select tipmues as id,tipmues||'-'||nombre as name from tipomuestra order by 1"
        if (lista.lower() =='mae_unid'):
            query = "select uni_codi as id,uni_desc as name from mae_unid order by 1"
        if (lista.lower() =='departamento'):
            query = "select coddep as id,desdep as name from maedep order by 1"
        if (lista.lower() =='ciudad'):
            query = "select codciu as id,coddep||'-'||codciu||'-'||desciu as name from maeciu order by 1"
        if (lista.lower() =='agencia'):
            query = "select codage as id,codage||'-'||nomage as name from agencias order by 1"
        if (lista.lower() =='lista'):
            query = "select codlista as id,codlista||'-'||nombre as name from lablistas order by 1"
        if (lista.lower() =='claseemp'):
            query = "select codcla as id,nombre as name from labempclase l order by 1"
        if (lista.lower() =='especialidad'):
            query = "select codespecialidades as id ,nomespecialidades as name  from especialidades order by 1"
        if (lista.lower() =='unegocio'):
            query = "select codundnegocio as id,nomundnegocio as name from undnegocio order by 1"
        if (lista.lower() =='usuario'):
            query = "select usuario as id,nombre as name from usuarios order by 1"
        if (lista.lower() =='mediospago'):
            query = "select codmed as id,desmed as name from mediospago m  order by 1"
        if (lista.lower() =='color'):
            query = "select cod as id,horai || '-'|| horaf as name from color order by 1"

        response_query = sdk.executeQueryPostgresSelect(query0 + query, str(stage))
        return {"data": list(response_query)}


# sirve para listas largas como examen o paciente , siempre devuelve 2 columnas, COD, NOM
@app.get('/lovl/{lista}/{patron}')
def conexion_postgres(lista:str,patron:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        patron = patron.upper()
        query=''
        if (lista.lower() =='examenes'):
            query = "select cdgexamen as id,nombre as name from examen where 1=1 and upper(cdgexamen||nombre) like '%"+ patron + "%' order by 2"
        if (lista.lower() =='pacientes'):
            query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
       
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}

# sirve para validar contra tablas de lista larga por la llave primaria
@app.get('/validate/examenes/{examen}')
def conexion_postgres(examen:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        
        query=''
        query = "select * from examen where cdgexamen = '"+ examen + "'"
        #  query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}

# sirve para validar contra tablas de lista larga por la llave primaria
@app.get('/validate/pacientes/{ide}/{pac}')
def conexion_postgres(ide:str,pac:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        query = "select * from paciente where tipide = '"+ ide + "' and codpac='" + pac + "'"
        #  query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}



####################################### cruds ##########################################################################33

####################################### TABLA DIAGNOSTICOS ##########################################################################33
@app.post('/diagnostico/update/{coddiagnostico}')
def update_data(data: dict,coddiagnostico:str):
        query="update diagnostico set  where coddiagnostico='{}'".format(coddiagnostico)
        sdk.insertPostgres(query, data,"prd")


@app.get('/diagnostico/select')
def conexion_postgres():
        query = 'select * from diagnostico' 
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}


@app.post('/diagnostico/insert')
def inser_data(data: dict):
        query='insert into diagnostico(coddiagnostico,nomdiagnostico) VALUES (%s,%s)'
        sdk.insertPostgres(query, data,"prd")

@app.delete('/diagnostico/delete/{coddiagnostico}')
def delete_data(coddiagnostico:str):
        query = "delete FROM test where coddiagnostico='{}'".format(coddiagnostico)
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
    }

################################### EMPRESAS ##############################
@app.put('/empresas/update/{id}')
def update_data(data: dict,id:str):
            query="update empresas set nombre=%s,pais=%s where id='{}'".format(id)
            sdk.updatePostgres(query, data,"prd")


@app.get('/empresas/select')
def conexion_postgres():
        query = 'SELECT id,nombre,pais from empresas order by 1' 
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        return {"data": list(response_query)}


@app.post('/empresas/insert')
def insert_data(data: dict):
        query='insert into empresas(id,nombre,pais) values (%s,%s,%s)'
        sdk.insertPostgres(query, data,"prd")

@app.delete('/empresas/delete/{id}')
def delete_data(id:str):
        query = "delete FROM empresas where id='{}'".format(id)
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
        }

###################### TODO SOBRE RESULTADOS ###########################################



# ********************* eliminar un item de resultado **********************************

@app.delete('/resultado/delete/{id}')
def delete_data(data: dict,id:str):
        query = "delete from resultado where id=" + id
        response_query = sdk.deletePostgres(query, str(stage))
        print(response_query)
        return {
            "statusCode": 200,
            "resultado": "success"
        }


# ******************** cambiar o alimentar un resultado *****************************************
@app.put('/resultado/update/{id}')
def update_data(data: dict,id:str):
    # resultado: results[matriz[pos]],
    # usuario: user,
    # age: agencia,
    # ord: numorden,
    # seq: seq,
    # examen: miexamen[pos],
    # anali: mianalisis[pos],
    # tipores: mitipores[pos],
    # unicodi: miunicodi[pos]
    va_resultado = data['resultado']
    va_usuario = data['usuario']
    va_age = data['age']
    va_ord = data['ord']
    va_seq = data['seq']
    va_examen = data['examen']
    va_anali = data['anali']
    va_tipores = data['tipores']
    if data['unicodi'] == '*':
        va_unidad = ''
    else:
        va_unidad = data['unicodi']
    va_resuformula = 0
    query = ''
    if (id != '0'):            
        query="update resultado set resultado='"+va_resultado+"',usuario='"+va_usuario+"',fecha=CURRENT_TIMESTAMP where id=" + id
        sdk.updatePostgres(query, data,"prd")
    else:
        query ="insert into resultado (resultado,usuario,codage,numorden,seq,cdgexamen,cdganalisis,tipores,unicodi) "
        query=query + " values ('"+va_resultado+"','"+va_usuario+"','"+va_age+"','"+va_ord+"','"+va_seq+"','"+va_examen+"','"+va_anali+"','"+va_tipores+"','"+va_unidad+"') "
        sdk.insertPostgres(query, data,"prd")
	# Acto seguido se verifica si ese analisis es insumo para calcular otros
    qry = "select count(*) as esparam from analisisparam where cdganalisis='" + va_anali + "'"
    response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_esparam = 0
    for obj in response_med:
        va_esparam = obj['esparam']
    if (va_esparam > 0):
        # busco todos los anilisis tipo formula de ese examen
        va_analisisform = ''
        qry = "select a.cdganalisis,a.unicodi from analisis a where a.cdgexamen='" + va_examen + "' and a.tipores='F'"
        response_fml = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_analisisform = ''
        for objf in response_fml:
            va_analisisform = objf['cdganalisis']
            va_unicodif = objf['unicodi']
            va_resuformula = calcula_formula(va_age,va_ord,va_anali) # se debe llamar para cada analisis formula de la orden
            if (va_resuformula != ''):
                qry = "select count(*) tot from resultado where codage='"+va_age+"' and numorden="+va_ord+" and cdganalisis='" + va_anali+"' and seq="+va_seq
                response_r = sdk.executeQueryPostgresSelect(qry, str(stage))
                va_resu_prev = 0
                for objr in response_r:
                    va_resu_prev = objr['tot']
                    if (va_resu_prev == 0): # no esta el res de fmla aun
                        qry = "update resultado set resultado = "+va_resuformula+",resnum="+ va_resuformula +" where codage='"+va_age+"' and numorden="+va_ord+" and cdganalisis='" + va_analisisform +"' and seq="+va_seq
                        sdk.updatePostgres(qry, data,"prd")
                    else:
                        qry="insert into resultado (resultado,usuario,codage,numorden,seq,cdgexamen,cdganalisis,tipores,unicodi) "
                        query=query + " values ('"+ va_resuformula +"','"+ va_usuario +"','"+ va_age + "',"+ va_ord + ","+ va_seq +",'" + va_examen + "' ,'"+ va_analisisform +"','F','" + va_unicodif + "') "
                        sdk.insertPostgres(qry, data,"prd")
    return {"statusCode": 200, "resultado": "success","esparam":va_esparam}

#************************* funcion para calcular formulas de una orden
def calcula_formula(age: str,ord:str, anali:str):
        
        qry = "select round((fecorden - fecnac)/365) edad,p.sexo "
        qry = qry + " from laborden o,paciente p where  o.codage='"+age+"' and o.numorden=" + ord 
        qry = qry + " and o.tipide = p.tipide and o.codpac = p.codpac "
        response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_edad = 0
        va_sexo = ''
        for obj in response_med:
            va_edad = obj['edad']
            va_sexo = obj['sexo']


        r24660010 = 0
        r24660015 = 0
        r24660020 = 0
        r24630010 = 0
        r24630015 = 0
        r24630020 = 0
        r24630030 = 0
        r24630060 = 0
        r24630260 = 0
        r24640010 = 0
        r24640015 = 0
        r24640020 = 0
        r24640030 = 0
        r24640060 = 0
        r24640260 = 0
        r24650010 = 0
        r24650015 = 0
        r24650020 = 0
        r24650030 = 0
        r24650060 = 0
        r24650260 = 0
        r24660030 = 0
        r24660260 = 0
        r34100010 = 0
        r34100025 = 0
        r34100015 = 0
        r34100020 = 0
        r34100060 = 0
        r34100035 = 0
        r34100045 = 0
        r34170010 = 0
        r34170025 = 0
        r34170015 = 0
        r34170020 = 0
        r34170060 = 0
        r34170035 = 0
        r34170045 = 0
        r50340005 = 0
        r50350010 = 0
        r50350020 = 0
        r50700004 = 0
        r50700010 = 0
        r50900005 = 0
        r50900004 = 0
        r50900010 = 0
        r50900015 = 0
        r50900020 = 0
        r50900025 = 0
        r25300020 = 0
        r51350005 = 0
        r51350010 = 0
        r50250050 = 0
        r51600010 = 0
        r50300005 = 0
        r50300015 = 0
        r31150100 = 0
        r31150110 = 0
        r31150080 = 0
        r50390010 = 0
        r51270020 = 0
        r51270030 = 0
        r51270010 = 0
        r51280010 = 0
        r51280020 = 0
        r52350010 = 0
        r52350020 = 0
        r52350003 = 0
        r25300005 = 0
        r25300010 = 0
        r51850005 = 0
        r51850010 = 0
        r34250010 = 0
        r34250025 = 0
        r34250015 = 0
        r34250035 = 0
        r34250060 = 0
        r34250045 = 0
        r22010021 = 0
        r22010004 = 0


        qry = "select sum( CASE WHEN cdganalisis='24660010' THEN coalesce(resnum,0) else NULL END ) r24660010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24660015' THEN coalesce(resnum,0) else NULL end) r24660015, "
        qry = qry + " sum( CASE WHEN cdganalisis='24660020' THEN coalesce(resnum,0) else NULL end) r24660020,  "
        qry = qry + " sum(  CASE WHEN cdganalisis='24630010' THEN coalesce(resnum,0) else NULL END ) r24630010,  "
        qry = qry + " sum( CASE WHEN cdganalisis='24630015' THEN coalesce(resnum,0) else null END ) r24630015,  "
        qry = qry + " sum(  CASE WHEN cdganalisis='24630020' THEN coalesce(resnum,0) else NULL end ) r24630020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24630030' THEN coalesce(resnum,0) else NULL END ) r24630030, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24630060' THEN coalesce(resnum,0) else NULL END ) r24630060, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24630260' THEN coalesce(resnum,0) else NULL END ) r24630260, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640010' THEN coalesce(resnum,0) else NULL END ) r24640010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640015' THEN coalesce(resnum,0) else NULL END ) r24640015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640020' THEN coalesce(resnum,0) else NULL end )  r24640020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640030' THEN coalesce(resnum,0) else NULL END ) r24640030, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640060' THEN coalesce(resnum,0) else NULL END ) r24640060, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24640260' THEN coalesce(resnum,0) else null END ) r24640260, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650010' THEN coalesce(resnum,0) else NULL END ) r24650010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650015' THEN coalesce(resnum,0) else null END) r24650015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650020' THEN coalesce(resnum,0) else null END) r24650020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650030' THEN coalesce(resnum,0) else null END) r24650030, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650060' THEN coalesce(resnum,0) else NULL end) r24650060, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24650260' THEN coalesce(resnum,0) else NULL END ) r24650260, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24660030' THEN coalesce(resnum,0) else NULL end) r24660030, "
        qry = qry + " sum(  CASE WHEN cdganalisis='24660260' THEN coalesce(resnum,0) else NULL end ) r24660260, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100010' THEN coalesce(resnum,0) else NULL END ) r34100010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100025' THEN coalesce(resnum,0) else NULL END ) r34100025, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100015' THEN coalesce(resnum,0) else NULL END ) r34100015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100020' THEN coalesce(resnum,0) else NULL END ) r34100020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100060' THEN coalesce(resnum,0) else NULL END ) r34100060, "
        qry = qry + " sum( CASE WHEN cdganalisis='34100035' THEN coalesce(resnum,0) else NULL END ) r34100035, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34100045' THEN coalesce(resnum,0) else NULL END ) r34100045, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170010' THEN coalesce(resnum,0) else NULL END ) r34170010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170025' THEN coalesce(resnum,0) else NULL end ) r34170025, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170015' THEN coalesce(resnum,0) else NULL end ) r34170015,  "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170020' THEN coalesce(resnum,0) else null end ) r34170020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170060' THEN coalesce(resnum,0) else null END) r34170060, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170035' THEN coalesce(resnum,0) else null end ) r34170035, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34170045' THEN coalesce(resnum,0) else null end ) r34170045, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50340005' THEN coalesce(resnum,0) else null end ) r50340005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50350010' THEN coalesce(resnum,0) else null END) r50350010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50350020' THEN coalesce(resnum,0) else null END ) r50350020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50700004' THEN coalesce(resnum,0) else null end ) r50700004, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50700010' THEN coalesce(resnum,0) else null END) r50700010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50900005' THEN coalesce(resnum,0) else null end ) r50900005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50900004' THEN coalesce(resnum,0) else null END) r50900004, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50900010' THEN coalesce(resnum,0) else null end ) r50900010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50900015' THEN coalesce(resnum,0) else null end ) r50900015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50900020' THEN coalesce(resnum,0) else null end ) r50900020, " 
        qry = qry + " sum(  CASE WHEN cdganalisis='50900025' THEN coalesce(resnum,0) else null end ) r50900025, "
        qry = qry + " sum(  CASE WHEN cdganalisis='25300020' THEN coalesce(resnum,0) else null end ) r25300020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51350005' THEN coalesce(resnum,0) else null end ) r51350005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51350010' THEN coalesce(resnum,0) else NULL end) r51350010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51350050' THEN coalesce(resnum,0) else NULL end) r50250050, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51600010' THEN coalesce(resnum,0) else NULL end) r51600010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50300005' THEN coalesce(resnum,0) else NULL end) r50300005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50300015' THEN coalesce(resnum,0) else NULL end) r50300015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='31150100' THEN coalesce(resnum,0) else NULL end) r31150100, "
        qry = qry + " sum(  CASE WHEN cdganalisis='31150110' THEN coalesce(resnum,0) else NULL end) r31150110, "
        qry = qry + " sum(  CASE WHEN cdganalisis='31150080' THEN coalesce(resnum,0) else NULL end) r31150080, "
        qry = qry + " sum(  CASE WHEN cdganalisis='50390010' THEN coalesce(resnum,0) else NULL end) r50390010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51270020' THEN coalesce(resnum,0) else NULL end) r51270020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51270030' THEN coalesce(resnum,0) else NULL end) r51270030, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51270010' THEN coalesce(resnum,0) else NULL end) r51270010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51280010' THEN coalesce(resnum,0) else NULL end) r51280010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51280020' THEN coalesce(resnum,0) else NULL end) r51280020, "
        qry = qry + " sum(  CASE WHEN cdganalisis='52350010' THEN coalesce(resnum,0) else NULL end) r52350010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='52350020' THEN coalesce(resnum,0) else NULL end ) r52350020, " 
        qry = qry + " sum(  CASE WHEN cdganalisis='52350003' THEN coalesce(resnum,0) else null  end) r52350003, "
        qry = qry + " sum(  CASE WHEN cdganalisis='52350005' THEN coalesce(resnum,0) else NULL end ) r25300005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='52350010' THEN coalesce(resnum,0) else null  end) r25300010,  "
        qry = qry + " sum(  CASE WHEN cdganalisis='51850005' THEN coalesce(resnum,0) else NULL end ) r51850005, "
        qry = qry + " sum(  CASE WHEN cdganalisis='51850010' THEN coalesce(resnum,0) else NULL END ) r51850010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250010' THEN coalesce(resnum,0) else NULL END ) r34250010, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250025' THEN coalesce(resnum,0) else NULL END ) r34250025, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250015' THEN coalesce(resnum,0) else NULL END ) r34250015, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250035' THEN coalesce(resnum,0) else NULL END ) r34250035, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250060' THEN coalesce(resnum,0) else NULL END ) r34250060, "
        qry = qry + " sum(  CASE WHEN cdganalisis='34250045' THEN coalesce(resnum,0) else NULL END ) r34250045, "
        qry = qry + " sum(  CASE WHEN cdganalisis='22010021' THEN coalesce(resnum,0) else null END) r22010021, "
        qry = qry + " sum(  CASE WHEN cdganalisis='22010004' THEN coalesce(resnum,0) else NULL end) r22010004 "
        qry = qry + " from resultado where codage='"+age+"' and numorden=" + ord
   
        response_par = sdk.executeQueryPostgresSelect(qry, str(stage))
        for objp in response_par:
            r24660010=objp['24660010']
            r24660015=objp['24660015']
            r24660020=objp['24660020']
            r24630010=objp['24630010']
            r24630015=objp['24630015']
            r24630020=objp['24630020']
            r24630030=objp['24630030']
            r24630060=objp['24630060']
            r24630260=objp['24630260']
            r24640010=objp['24640010']
            r24640015=objp['24640015']
            r24640020=objp['24640020']
            r24640030=objp['24640030']
            r24640060=objp['24640060']
            r24640260=objp['24640260']
            r24650010=objp['24650010']
            r24650015=objp['24650015']
            r24650020=objp['24650020']
            r24650030=objp['24650030']
            r24650060=objp['24650060']
            r24650260=objp['24650260']
            r24660030=objp['24660030']
            r24660260=objp['24660260']
            r34100010=objp['34100010']
            r34100025=objp['34100025']
            r34100015=objp['34100015']
            r34100020=objp['34100020']
            r34100060=objp['34100060']
            r34100035=objp['34100035']
            r34100045=objp['34100045']
            r34170010=objp['34170010']
            r34170025=objp['34170025']
            r34170015=objp['34170015']
            r34170020=objp['34170020']
            r34170060=objp['34170060']
            r34170035=objp['34170035']
            r34170045=objp['34170045']
            r50340005=objp['50340005']
            r50350010=objp['50350010']
            r50350020=objp['50350020']
            r50700004=objp['50700004']
            r50700010=objp['50700010']
            r50900005=objp['50900005']
            r50900004=objp['50900004']
            r50900010=objp['50900010']
            r50900015=objp['50900015']
            r50900020=objp['50900020']
            r50900025=objp['50900025']
            r25300020=objp['25300020']
            r51350005=objp['51350005']
            r51350010=objp['51350010']
            r50250050=objp['50250050']
            r51600010=objp['51600010']
            r50300005=objp['50300005']
            r50300015=objp['50300015']
            r31150100=objp['31150100']
            r31150110=objp['31150110']
            r31150080=objp['31150080']
            r50390010=objp['50390010']
            r51270020=objp['51270020']
            r51270030=objp['51270030']
            r51270010=objp['51270010']
            r51280010=objp['51280010']
            r51280020=objp['51280020']
            r52350010=objp['52350010']
            r52350020=objp['52350020']
            r52350003=objp['52350003']
            r25300005=objp['25300005']
            r25300010=objp['25300010']
            r51850005=objp['51850005']
            r51850010=objp['51850010']
            r34250010=objp['34250010']
            r34250025=objp['34250025']
            r34250015=objp['34250015']
            r34250035=objp['34250035']
            r34250060=objp['34250060']
            r34250045=objp['34250045']
            r22010021=objp['22010021']
            r22010004=objp['22010004']

            # resolver formulas

            v34100020 = r34100010*r34100015 / 100
            v34100030 = v34100020*r34100025 / 100
            v34100040 = v34100020*r34100035 / 100
            v34100050 = (v34100020 * r34100045) / 100
            if ( v34100050 != 0 ):
                v34100055 = v34100040 / v34100050
            else:
                v34100055 = 0
            
            v34100065 = v34100020 * r34100060/100
            # cd4-CD8  3417
            v34170020 = r34170010*r34170015/100
            v34170030 = v34170020*r34170025 / 100
            v34170040 = v34170020*r34170035 / 100
            v34170050 = (v34170020 * r34170045) / 100
            if ( v34170050 != 0 ):
                v34170055 = v34170040 / v34170050
            else:
                v34170055 = 0
            
            v34170065 = v34170020*r34170060/100
            # cd4 3425
            v34250020 = r34250010*r34250015/100
            v34250030 = v34250020*r34250025 / 100
            v34250040 = v34250020*r34250035 / 100
            v34250050 = (v34250020 * r34250045) / 100
            if ( v34250050 != 0 ):
                v34250055 = v34250040 / v34250050
            else:
                v34250055 = 0
            
            v34250065 = v34250020*r34250060/100
            #ISOENZIMAS CPK
            v51350015 = ifnull(r51350005,0) - ifnull(r51350010,0)
            #UREA
            v50250060 = r50250050 * 2.14
            v51600015 = r51600010 * 2.14
            # BILIRRUBINA
            v50300010 = ifnull(r50300015,0) - ifnull(r50300005,0)
            # PROTEINAS
            v51850015 = ifnull(r51850005,0) - ifnull(r51850010,0)
            #  COLESTEROLES Y trig.
            v31150120 = ifnull(r31150100,0) - ifnull(r31150110,0) - (ifnull(r31150080,0)/5)
            v31150130 = ifnull(r31150080,0)/5
            if ( ifnull(r31150110,0) != 0 ):
                v31150150 = ifnull(r31150100,0)/ifnull(r31150110,0)
            else:
                v31150150 = 0
            
            v50390020 = ifnull(r50390010,0)/5
            v51270040 = ifnull(r51270020,0)-ifnull(r51270030,0) - (ifnull(r51270010,0)/5)
            v51270050 = ifnull(r51270010,0)/5
            if ( ifnull(r51280020,0) != 0 ):
                v51280030 = ifnull(r51280010,0)/ifnull(r51280020,0)
            else:
                v51280030 = 0
            
            V52350021 = ifnull(r52350010,0) - ifnull(r52350020,0) - (ifnull(r52350003,0)/5)
            V52350022 = ifnull(r52350003,0) /5
            if ( ifnull(r52350020,0) != 0 ):
                v52350023 = ifnull(r52350010,0) / ifnull(r52350020,0)
            else:
                v52350023 = 0
            
            # HEMOGRAMAS *********************************************************************************
            # 2466
            if ( r24660010 != 0 ):
                v24660260 = (r24660020 / r24660010)*10
            else:
                v24660260 = 0
            
            if ( r24660010 != 0 ):
                v24660265 = (r24660015 / r24660010)*10
            else:
                v24660265 =0
            
            if ( r24660020 != 0 ):
                v24660267 = (r24660015/r24660020)*100
            else:
                v24660267 = 0
            
            if ( r24660010 != 0 ):
                v24661025 = (r24660260/r24660010)*1
            else:
                v24661025 = 0
            
            # 2463
            if ( r24630010 !=0  ):
                v24630260 = (r24630020 / r24630010)*10
            else:
                v24630260 = 0
            
            if ( r24630010 != 0 ):
                v24630265 = (r24630015 / r24630010)*10
            else:
                v24630265 =0
            
            if ( r24630020 != 0 ):
                v24630267 = (r24630015/r24630020)*100
            else:
                v24630267 = 0
            
            if ( r24630010 != 0 ):
                v24639994 = (r24630260/r24630010)*1
            else:
                v24639994 = 0
            
            # 2465
            if ( r24650010 != 0 ):
                v24650260 = (r24650020 / r24650010)*10
            else:
                v24650260 = 0
            
            if ( r24650010 != 0 ):
                v24650265 = (r24650015 / r24650010)*10
            else:
                v24650265 =0
            
            if ( r24650020 != 0 ):
                v24650267 = (r24650015/r24650020)*100
            else:
                v24650267 = 0
            
            if ( r24650010 != 0 ):
                v24659994 = (r24650260/r24650010)*1
            else:
                v24659994 = 0
            
            # 2464
            if ( r24640010 != 0 ):
                v24640260 = (r24640020 / r24640010)*10
            else:
                v24640260 = 0
            
            if ( r24640010 != 0 ):
                v24640265 = (r24640015 / r24640010)*10
            else:
                v24640265 = 0
            
            if ( r24640020 != 0 ):
                v24640267 = (r24640015/r24640020)*100
            else:
                v24640267 = 0
            
            if ( r24640010 != 0 ):
                v24649994 = (r24640260/r24640010)*1
            else:
                v24649994 = 0
            
            #FIN DE HEMOGRAMAS ************************************************************************************************
            
            # RETICULOCITOS
            v25300015 = ifnull(r25300005,0)* ifnull(r25300010,0) /100
            if ( va_sexo == 'F' ):
                v25300025 = ifnull(r25300005,0) * ifnull(r25300020,0) / 42
            else:
                v25300025 = ifnull(r25300005,0) * ifnull(r25300020,0) / 45
            
            v25300030 = v25300025 / 2.5
            if ( va_edad >= 0 and  r50700010 > 0 ):
                if ( va_sexo=='M' ):
                    v50950005 = 186*(  r50700010 ** -1.154 ) * (va_edad ** -0.203) 	#	hombre
                else:
                    v50950005 = 186*(  r50700010 ** -1.154 ) * (va_edad ** -0.203) * 0.742 	# mujer
                
            else:
                v50950005 = 0
            
            if ( r50900015  > 0 and  r50900020 > 0 ):
                v50900030 = (r50900020 ** 0.425) * (r50900015 ** 0.725) * 0.007184 
            else:
                v50900030 = 0
            
            if ( r50900010 != 0 and v50900030  != 0 ):
                v50900035 = (( r50900004  *  r50900025  )/( r50900010 * 1440  ))*(1.73 /  v50900030 ) 
            else:
                v50900035 = 0

            # nuevos examenes hierro dra sofi

            v22010001 = r22010021 * 1.25
            v22010002 = v22010001 - r22010004
            if ( v22010001 > 0 ):
                v22010005 = (r22010004 * 100) / v22010001
            else:
                v22010005 = 0

            if ( anali=='34100020' ):
                return(round(v34100020,3))
            if ( anali=='34100030' ):
                return(round(v34100030,3))
            if ( anali=='34100040' ):
                return(round(v34100040,3))
            if ( anali=='34100050' ):
                return(round(v34100050,3))
            if ( anali=='34100055' ):
                return(round(v34100055,3))
            if ( anali=='34170020' ):
                return(round(v34170020,3))
            if ( anali=='34170030' ):
                return(round(v34170030,3))
            if ( anali=='34170040' ):
                return(round(v34170040,3))
            if ( anali=='34170050' ):
                return(round(v34170050,3))
            if ( anali=='34170055' ):
                return(round(v34170055,3))
            if ( anali=='34250020' ):
                return(round(v34250020,3))
            if ( anali=='34250030' ):
                return(round(v34250030,3))
            if ( anali=='34250040' ):
                return(round(v34250040,3))
            if ( anali=='34250050' ):
                return(round(v34250050,3))
            if ( anali=='34250055' ):
                return(round(v34250055,3))
            if ( anali=='24660260' ):
                return(round(v24660260,3))
            if ( anali=='24660265' ):
                return(round(v24660265,3))
            if ( anali=='24660267' ):
                return(round(v24660267,3))
            if ( anali=='24630260' ):
                return(round(v24630260,3))
            if ( anali=='24630265' ):
                return(round(v24630265,3))
            if ( anali=='24630267' ):
                return(round(v24630267,3))
            if ( anali=='24640260' ):
                return(round(v24640260,3))
            if ( anali=='24640265' ):
                return(round(v24640265,3))
            if ( anali=='24640267' ):
                return(round(v24640267,3))
            if ( anali=='24650260' ):
                return(round(v24650260,3))
            if ( anali=='24650265' ):
                return(round(v24650265,3))
            if ( anali=='24650267' ):
                return(round(v24650267,3))
            #if ( anali=='50350022' ):
            #    return(round(v50350022,3))
            #if ( anali=='50350021' ):
            #    return(round(v50350021,3))
            if ( anali=='50950005' ):
                return(round(v50950005,3))
            if ( anali=='50900030' ):
                return(round(v50900030,3))
            if ( anali=='50900035' ):
                return(round(v50900035,3))
            if ( anali=='25300015' ):
                return(round(v25300015,3))
            if ( anali=='25300025' ):
                return(round(v25300025,3))
            if ( anali=='25300030' ):
                return(round(v25300030,3))
            if (  anali=='51350015' ):
                return(round(v51350015,3))
            if ( anali== '50250060' ):
                return(round(v50250060,3))
            if ( anali== '51600015' ):
                return(round(v51600015,3))
            if ( anali== '50300010' ):
                 return(round(v50300010,3))
            if ( anali== '31150120' ):
                return(round(v31150120,3))
            if ( anali== '31150130' ):
                return(round(v31150130,3))
            if  (anali== '31150150' ):
                return(round(v31150150,3))
            if ( anali== '50390020' ):
                return(round(v50390020,3))
            if ( anali== '51270040' ):
                return(round(v51270040,3))
            if ( anali== '51270050' ):
                return(round(v51270050,3))
            if ( anali== '51280030' ):
                return(round(v51280030,3))
            #if ( anali== '52350021' ):
            #    return(round(v52350021,3))
            #if ( anali== '52350022' ):
            #    return(round(v52350022,3))
            if ( anali== '52350023' ):
                return(round(v52350023,3))
            if ( anali== '25300015' ):
                return(round(v25300015,3))
            if ( anali== '25300025' ):
                return(round(v25300025,3))
            if ( anali== '25300030' ):
                return(round(v25300030,3))
            if ( anali== '51850015' ):
                return(round(v51850015,3))
            if ( anali== '34100065' ):
                return(round(v34100065,3))
            if ( anali== '34170065' ):
                return(round(v34170065,3))
            if ( anali== '34250065' ):
                return(round(v34250065,3))
            if ( anali== '24639994' ):
                return(round(v24639994,3))
            if ( anali== '24649994' ):
                return(round(v24649994,3))
            if ( anali== '24659994' ):
                return(round(v24659994,3))
            if ( anali== '22010001' ):
                return(round(v22010001,3))
            if ( anali== '22010002' ):
                return(round(v22010002,3))
            if ( anali== '22010005' ):
                return(round(v22010005,3))
            if ( anali== '24661025' ):
                return(round(v24661025,3))
            else:
                return(0)


# ******************** firmar un resultado *****************************************
@app.post('/resultado/firmar/{age}/{ord}')
def update_data(data: dict,age:str,ord:str):
    user =  data['user']
    tipo =  data['tipo']
    seq = data['seq']
    medico = ''

    qry = "select codmedico,nommedico from medicos where usuario='" + user + "'"
    response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_med=''
    va_nom=''
    for obj in response_med:
        va_med = obj['codmedico']
        va_nom = obj['nommedico']
    
   
    qry = "select tipofirma from agencias where codage='" + age + "'"
    response_age = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_age:
        va_tipof = obja['tipofirma']


    if (va_med != ''):
        if (tipo=='E'):
            query="update laborden set medfirmae='" + va_med + "'" 
            query = query + ",horfirmae=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
            sdk.updatePostgres(query, data,"prd")
        else:
            if (va_tipof == 'O'):
                qry = "update laborden set medfirma='" + va_med + "'" 
                qry = qry + ",horfirma=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
                sdk.updatePostgres(qry, data,"prd")
            else:
                qry = "update labordendet set medfirmad='" + va_med +"'"
                qry = qry + ",horfirmad=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "' and seq=" + seq
                sdk.updatePostgres(qry, data,"prd") 
        exitoso = 'SI'
        mensaje = 'Gracias por su firma, Dr(a) ' + va_nom
    else: # es un usuario sin medico asociado
        mensaje = 'Usuario No habilitado para Firmar'
        exitoso = 'NO'     
    if (exitoso == 'SI'):
         resu = 'success'
    else:
         resu = 'failure'
         mensaje = 'Usuario no corresponde a ningun medico registrado'
    return {"statusCode": 200,"resultado": resu,"mensaje":mensaje}

     
                     

####################### servicio resultados IMPRESION ##################################

@app.get('/resultado/find/{codage}/{numorden}')
def conexion_postgres(codage:str,numorden:str):


   #Direccion y telefonos sede ppal
    qry = "select texto,orden from textos where cod='PPAL' order by orden "
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    # Bolos del tope y piede la pagina
    respuesta=[]
    va_bolo_examen = ''
    va_respie = ''
    va_restop = ''
    qry = "select cod,texto from textos where cod in ('RESPIE','RESTOP')"
    response_bolo = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response_bolo:
        if (obj['cod'] == 'RESPIE'):
            va_respie = obj['texto']
       # if (obj['cod'] == 'RESTOP'):    
       #     va_restop = obj['texto']

    # to_number('"+numorden+"','9999999999999999')
    # Dtaos del paciente
    qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden= " + numorden
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
    response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
    datapac={}
    for obj in response_query0:
        va_ordenl = obj['ordenl'] 
        va_tip = obj['tipide']
        va_codpac = obj['codpac']
        va_nombre = obj['nombre']
        va_sexo = obj['sexo']
        va_edad = obj['edadf']
        va_tel = obj['tel']
        va_agencia = obj['nomage']
        va_med = obj['nommedico']
        va_fec = obj['fecorden']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_medfirma = obj['medfirma']
        va_horfirma = obj['horfirma']

        datapac = {"ordenl":va_ordenl,"codpac":va_codpac,"nombre":va_nombre,"sexo":va_sexo,"edad":va_edad,"tel":va_tel,"age":va_agencia,"medico":va_med,"empresa":va_nomemp,"fecorden":va_fecorden,"medfirma":va_medfirma,"horfirma":va_horfirma}

    # los distintos examenes de la orden de laboratorio
    qry = "select distinct r.seq,r.cdgexamen,e.nombre as nomexamen,r.usuario,medfirmad,horfirmad  "
    qry = qry + "from resultado r,examen e, labordendet d "
    qry = qry + "where r.cdgexamen=e.cdgexamen  " 
    qry = qry + "and r.codage='"+codage+"' and r.numorden="+numorden+" "
    qry = qry +" and r.ordenl = d.ordenl and r.seq= d.seq and r.resultado is not null"    
    response_query = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    for obj in response_query:
        va_examen = obj['cdgexamen']
        va_nomexamen = obj['nomexamen']
        va_usuario = obj['usuario']
        va_seq = obj['seq']
        va_medfirmad = obj['medfirmad']
        va_horfirmad = obj['horfirmad']

        va_bolo_examen = ''
        qry = "select texto from textos where aplica like '%"+va_examen+"%'"
        response_query_textos = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_query_textos:
            va_bolo_examen = obj['texto']
        

        # los distintos analisis del examen (seq) de la orden de laboratorio            
        qry = "select r.cdganalisis, a.nombre as nomanalisis, "
        qry = qry + "r.resultado,r.fecha,r.tipores,r.resnum,r.unicodi,r.usuario  "
        qry = qry + " ,getvalnormals('"+va_fec+"','"+va_tip+"','"+va_codpac+"',r.cdgexamen,r.cdganalisis,'"+codage+"','"+numorden+"') as valnormal  "
        qry = qry + " ,resultadoant('"+va_fec+"',r.cdgexamen,r.cdganalisis,'"+va_tip+"','"+va_codpac+"') as resant  "
        qry = qry + " from resultado r,examen e,analisis a "
        qry = qry + " where r.cdgexamen=e.cdgexamen and r.cdganalisis=a.cdganalisis " 
        qry = qry + " and r.codage='"+codage+"' and r.numorden="+numorden+" and r.seq='" + str(va_seq) + "' " 
        qry = qry + " and r.resultado is not null "

        response_query_ex = sdk.executeQueryPostgresSelect(qry, str(stage))
        dataexamen = {"examen":va_examen,"nomexamen":va_nomexamen,"usuario":va_usuario,"detalle":list(response_query_ex),"bolo":va_bolo_examen,"medfirmad":va_medfirmad,"horfirmad":va_horfirmad}
        respuesta.append(dataexamen)
    # calcular los valores de referencia
    # calcular el resultado anterior
    return {"statusCode": 200,"resultado": "success","paciente":datapac,"grupo": list(respuesta),"respie":va_respie,"sedeppal":list(response_querysp)}





####################### ecabezado del resultado ##################################

@app.get('/resultadoencabezado/find/{codage}/{numorden}')
def conexion_postgres(codage:str,numorden:str):

   #Direccion y telefonos sede ppal
    qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma,medfirmae,horfirmae "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden="+numorden+" "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    datapac = {}
    for obj in response_querysp:
        va_fecorden = obj['fecorden']
        va_nompac = obj['nombre']
        va_edadf = obj['edadf']
        va_sexo = obj['sexo']
        datapac = {'fecorden':va_fecorden,'nompac':va_nompac,'edadf':va_edadf,'sexo':va_sexo}
    
    qry = "select d.cdgexamen,e.nombre,d.seq,d.medfirmad, d.horfirmad from labordendet d,examen e "
    qry = qry + " where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999') and d.cdgexamen=e.cdgexamen "
    response_exam = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    return {"statusCode": 200,"resultado": "success","paciente":datapac,"examenes": list(response_exam) }

####################### Detalle del resultado ####################################

# los distintos analisis del examen (seq) de la orden de laboratorio            
@app.get('/resultadodetalle/find/{codage}/{numorden}/{seq}')
def conexion_postgres(codage:str,numorden:str,seq:str):

   #Direccion y telefonos sede ppal
    qry = "select ordenl,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden="+numorden+" "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico  "
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    datapac = {};
    for obj in response_querysp:
        va_ordenl = obj['ordenl'] 
        va_tip = obj['tipide']
        va_codpac = obj['codpac']
        va_nombre = obj['nombre']
        va_sexo = obj['sexo']
        va_edad = obj['edadf']
        va_tel = obj['tel']
        va_agencia = obj['nomage']
        va_med = obj['nommedico']
        va_fec = obj['fecorden']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_medfirma = obj['medfirma']
        va_horfirma = obj['horfirma']

        datares = [];
        regres = {}

        # los analisis del examen en esa orden
        qry = "select d.cdgexamen,d.seq,a.cdganalisis,a.nombre as nomanalisis, "
        qry = qry + " '' as resultado,'' as fecha,a.tipores ,'' as resnum,a.unicodi ,'' as usuario,'' as valnormal,'' as resant, "
        qry = qry + " '' as fechamaq,a.tiponorm,getvalayuda(a.cdgexamen,a.cdganalisis) valayuda, d.seq ,a.orden"
        qry = qry + " ,getvalnormals('"+va_fec+"','"+va_tip+"','"+va_codpac+"',d.cdgexamen,a.cdganalisis,'"+codage+"','"+numorden+"') as valnormal  "
        qry = qry + " ,resultadoant('"+va_fec+"',d.cdgexamen,a.cdganalisis,'"+va_tip+"','"+va_codpac+"') as resant ,a.tipores "
        qry = qry + "  from labordendet d,examen e,analisis a  "
        qry = qry + " where d.cdgexamen=e.cdgexamen and e.cdgexamen=a.cdgexamen "  
        qry = qry + " and d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999999')  and d.seq="+ seq +" order by a.orden "
        response_query_det = sdk.executeQueryPostgresSelect(qry, str(stage))

        for obj in response_query_det:
            va_seq = obj['seq'] 
            va_anali = obj['cdganalisis']
            va_nomanali = obj['nomanalisis']
            va_valayuda = obj['valayuda']
            va_uni = obj['unicodi']
            va_tiponor = obj['tiponorm']
            va_examen = obj['cdgexamen']
            va_valnorm = obj['valnormal']
            va_resant = obj['resant']
            va_orden = obj['orden']
            va_tipores = obj['tipores']

            regres = {'id':0,'cdgexamen':va_examen,'cdganalisis':va_anali,'nomanalisis':va_nomanali,'orden':va_orden,
            'resultado':'','fecha':'','tipores':va_tipores,'resnum':'',
            'unicodi':'','usuario':'','seq':va_seq,'valnormal':va_valnorm,
            'resant': va_resant,'fehamaq':'','tiponorm':'' , 'valayuda': va_valayuda}

            # el resultado individual de cada analisis
            qry = "select r.id,r.resultado,to_char(r.fecha,'ddmmyyyy') as fecha, "
            qry = qry + "r.tipores,r.resnum,r.unicodi,r.usuario ,r.seq,r.fechamaq  "
            qry = qry + " from resultado r "
            qry = qry + " where r.codage='"+codage+"' and r.numorden=to_number('"+numorden+"','9999999999999999') and r.seq=" + str(va_seq) 
            qry = qry +" and r.cdgexamen='"+ va_examen +"' and r.cdganalisis = '"+ va_anali +"' and r.seq="+ seq +" order by r.id" 

            response_query_an = sdk.executeQueryPostgresSelect(qry, str(stage))
            va_id = 0 # no existe el resultado aun 
            for res in response_query_an:
                va_id = res['id'] 
                va_resu = res['resultado']
                va_fecha = res['fecha']
                va_tipores = res['tipores']
                va_resnum=res['resnum']
                va_uni = res['unicodi']
                va_user = res['usuario']
                va_fechamaq = res['fechamaq']
                regres['id'] = va_id
                regres['resultado'] = va_resu
                regres['fecha'] = va_fecha
                regres['tipores'] = va_tipores
                regres['resnum'] = va_resnum
                regres['usuario'] = va_user
                regres['fechamaq']= va_fechamaq
            datares.append(regres)

    return {"statusCode": 200,"resultado": "success","analisis": list(datares) }


###################### Servicios de la orden de laboratorio #############################

# servicio para obtener consecutivo de documentos
@app.get('/ipsconsec/next/{dep}/{doc}')
def conexion_postgres(dep:str,doc:str):
    data = {}
    qry = "select num+1 as proximo from ipsconsec where docu='"+doc+"' and codage='" + dep +"'" 
    response_queryex = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_proximo = 0    
    for obj in response_queryex:
        va_proximo = obj['proximo']
    if (va_proximo == 0):
        query = "insert into ipsconsec (docu,codage,num) values ('" +doc +"','"+dep+"',0)"
        sdk.insertPostgres(query, data,'prd') 
		 
    query="update ipsconsec set num=num+1 where docu='"+doc+"' and codage='" + dep +"'"   
    sdk.updatePostgres(query, data,'prd') 
    return {"statusCode": 200,"resultado": "success", "consecutivo":va_proximo}

# servicio para encontrar el precio de un examen
@app.get('/precio/find/{codemp}/{dep}/{examen}')
def conexion_postgres(codemp:str,examen:str,dep:str):

    qry = "select nombre,nivexa from examen where cdgexamen='"+examen+"'" 
    response_queryex = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_nivelex =''
    for obj in response_queryex:
        va_nivelex = obj['nivexa']
        va_nomexamen = obj['nombre']


   #obtenemos la lista de la empresa
    va_desce = 0
    qry = "select codlista,desce from labempresa where codemp ='" + codemp +"'" 
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response_querysp:
        va_codlista = obj['codlista'] 
        va_desce = obj['desce']
    if dep != '':
        qry = "select valor from labtarifasdep where codlista ='" + va_codlista +"' and cdgexamen='"+examen+"' and coddep='"+dep+"'" 
        response_querysd = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_valor = 0
        for obj in response_querysd:
            va_valor = obj['valor']    
    if (va_valor ==0):
        qry = "select valor from labtarifas where codlista ='" + va_codlista +"' and cdgexamen='"+examen+"'" 
        response_querysl = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_valor = 0
        for obj in response_querysl:
            va_valor = obj['valor']
	# busco descuento adicional x convenio empresa    
    qry = "select descc,nivel from examenemp where  codemp ='" + codemp +"' and cdgexamen='"+examen+"'" 
    response_queryse = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_descc = 0
    va_nivele =''
    for obj in response_queryse:
        va_descc = obj['descc']
        va_nivele = obj['nivel']
    if (va_nivele ==''):
        va_nivele = va_nivelex # tomamos el nivel del examen
    if (va_nivele !=''): # si ya hay nivel
        qry = "select descn from nivemp where codemp='" + codemp +"' and " + str(va_nivele) + " between nivmin and nivmax " 
        response_queryniv = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_descn = 0
        for obj in response_queryniv:
            va_descn = obj['descn']    
    va_destotal = va_desce + va_descc + va_descn

    return {"statusCode": 200,"resultado": "success", "nombre":va_nomexamen,"valor":va_valor,"descuento":va_destotal }


####################### servicio orden de laboratorio IMPRESION ##################################

@app.get('/orden/find/{codage}/{numorden}')
def conexion_postgres(codage:str,numorden:str):


   #Direccion y telefonos sede ppal
   # qry = "select texto,orden from textos where cod='ORDTOP' order by orden "
   # response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    # Bolos del tope y piede la pagina
  
    qry = "select cod,texto from textos where cod in ('ORDPIE','ORDFIRMA','ORDTOP')"
    response_bolo = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_ordtop = ''
    va_ordfir=''
    va_ordpie =''
    va_bono = 0
    va_copago = 0
    va_cuotam = 0
    va_descpac = 0
    for obj in response_bolo:
        if obj['cod'] == 'ORDPIE':
            va_ordpie = obj['texto']
        else:
            if obj['cod'] == 'ORDFIRMA':
                va_ordfir = obj['texto']
            else:
                va_ordtop = obj['texto']
       # if (obj['cod'] == 'RESTOP'):    
       #     va_restop = obj['texto']

    # Dtaos del paciente
    qry = "select ordenl,o.numorden,o.tipide, o.codpac,concat(p.nompac,' ',p.apepac) nombre,p.fecnac, "
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,o.hora,medfirma,horfirma,p.contpac as contrato, p.dir,o.fecentr as entrega,o.usuario as elaborado "  
    qry = qry + " ,a.predian,a.resdian, o.bono, o.copago, o.cuotam ,o.descpac "
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden=to_number('"+numorden+"','9999999999999999') "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
    response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
    datapac={}
    for obj in response_query0:
        va_predian = obj['predian']
        va_resdian = obj['resdian'] 
        va_ordenl = obj['ordenl'] 
        va_tip = obj['tipide']
        va_codpac = obj['codpac']
        va_nombre = obj['nombre']
        va_sexo = obj['sexo']
        va_edad = obj['edadf']
        va_tel = obj['tel']
        va_agencia = obj['nomage']
        va_med = obj['nommedico']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_horaorden = obj['hora']
        va_direccion = obj['dir']
        va_contrato = obj['contrato']
        va_elab = obj['elaborado']
        va_entrega = obj['entrega']
        va_bono = obj['bono']
        va_copago = obj['copago']
        va_cuotam = obj['cuotam']
        va_descpac = obj['descpac']

        datapac = {"tipide":va_tip, "codpac":va_codpac,"nombre":va_nombre,"sexo":va_sexo,"edad":va_edad,"tel":va_tel,"medico":va_med,"empresa":va_nomemp,"dir":va_direccion,"contrato":va_contrato}

    # los distintos examenes de la orden de laboratorio
    qry = "select distinct d.seq,d.cdgexamen,e.nombre as nomexamen,d.valor,d.desc1,d.desc2,d.partic,d.corte,d.pend  "
    qry = qry + "from examen e, labordendet d "
    qry = qry + "where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999999') "
    qry = qry +" and d.cdgexamen=e.cdgexamen "    
    response_query = sdk.executeQueryPostgresSelect(qry, str(stage))

    va_subtotal = 0
    va_desc2    = 0
    va_abo      = 0
    va_desc3    = 0
    #--------- los subtotales de la orden ----------------------------------
    qry = "select sum(valor) as subtotal, sum(valor*coalesce(desc2,0)/100) as desc2, sum( valor*(1-desc2/100)*(coalesce(desc3,0)/100 )) as desc3 "
    qry = qry + " from labordendet d where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999999') "
    
    response_queryt = sdk.executeQueryPostgresSelect(qry, str(stage))
    for objt in response_queryt:
        va_subtotal = objt['subtotal']
        va_desc2 = objt['desc2']
        va_desc3 = objt['desc3']
    #--------- los pagos de la orden ----------------------------------
    qry = "select sum(valor) as abonos "
    qry = qry + " from labordenpago d where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999999') "
    
    response_queryab = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_queryab:
        va_abo = obja['abonos']
        
    # subtotal => va_subtotal    
    # bono, copago, cuotam
    va_otroscargos = va_bono + va_cuotam + va_copago
    va_descpaci = va_descpac + va_desc2 #dcto autorizado
    va_total = va_subtotal - va_descpaci + va_otroscargos + va_desc3
    # abono => va_abo
    va_saldo = va_total - va_abo

    return {"statusCode": 200,"resultado": "success","ordenl":va_ordenl,"age":va_agencia,"numorden":numorden,"fecorden":va_fecorden,"entrega":va_entrega,"ordtop":va_ordtop,"ordpie":va_ordpie,"ordfir":va_ordfir,"predian":va_predian,"resdian":va_resdian,"elab":va_elab,"hora":va_horaorden,"paciente":datapac,"detalle": list(response_query),"subtotal":va_subtotal,"bono":va_bono,"cuotam":va_cuotam,"copago":va_copago,"descauto":va_descpaci,"total":va_total,"abono":va_abo,"saldo":va_saldo}



####################### servicio opciones por usuario  ##################################
@app.get('/usuarioopciones/find/{usuario}')
def conexion_postgres(usuario:str):

   #Carpetas
    qry = "select distinct o.carpeta "
    qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
    qry = qry+" where u.usuario='"+ usuario +"' "
    qry = qry+" and u.usuario=ur.usuario "
    qry = qry+" and ur.role = r.role  "
    qry = qry+" and r.opcion = o.opcion " 
    qry = qry+" order by 1 "
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    datamenu = {}
    listado = []

    for obj in response:
        va_carpeta = obj['carpeta'] 
        # opciones de la carpeta
        qry = "select o.opcion,o.ruta, o.nombre "
        qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
        qry = qry+" where u.usuario='"+ usuario +"' "
        qry = qry+" and u.usuario=ur.usuario "
        qry = qry+" and ur.role = r.role  "
        qry = qry+" and r.opcion = o.opcion "
        qry = qry+" and o.carpeta ='"+va_carpeta+"' and o.mostrar='S'" 
        qry = qry+" order by o.orden "    
        response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
        datamenu = {"carpeta":va_carpeta,"opciones":list(response_query0)}
        listado.append(datamenu)

    return {"statusCode": 200,"resultado": "success","carpetas": list(listado)}

####################### servicio opciones sin jerarquia  ##################################
@app.get('/usuarioopcioneslist/find/{usuario}')
def conexion_postgres(usuario:str):

   #Carpetas
    qry = "select o.opcion,o.ruta "
    qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
    qry = qry+" where u.usuario='"+ usuario +"' "
    qry = qry+" and u.usuario=ur.usuario "
    qry = qry+" and ur.role = r.role  "
    qry = qry+" and r.opcion = o.opcion "
    qry = qry+" and o.mostrar='S'" 
    qry = qry+" order by o.orden "    
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    datamenu = {}
    listado = []

    return {"statusCode": 200,"resultado": "success","opciones": list(response)}


# ********** inicio servicios CRUD ********* 

 # ---------------- tabla: diagnostico---------- 
# Endpoint Update 
@app.put('/diagnostico/update/{id}') 
def update_data(data: dict,id:str):  
	query="update diagnostico set nomdiagnostico=%s  where coddiagnostico='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/diagnostico/select') 
def conexion_postgres(): 
	query = 'SELECT coddiagnostico,nomdiagnostico from diagnostico order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/diagnostico/insert') 
def insert_data(data: dict): 
	query='insert into diagnostico(coddiagnostico,nomdiagnostico) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/diagnostico/delete/{id}') 
def delete_data(id: str): 
	query="delete from diagnostico where coddiagnostico='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: medicos---------- 
# Endpoint Update 
@app.put('/medicos/update/{id}') 
def update_data(data: dict,id:str):  
	query="update medicos set nommedico=%s,ccmedico=%s,espmedico=%s,perfil=%s,celular=%s,tel=%s,ciudad=%s,codundnegocio=%s,usuario=%s,firma=%s,presentacion=%s  where codmedico='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/medicos/select') 
def conexion_postgres(): 
	query = 'SELECT codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion from medicos order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/medicos/insert') 
def insert_data(data: dict): 
	query='insert into medicos(codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/medicos/delete/{id}') 
def delete_data(id: str): 
	query="delete from medicos where codmedico='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: undnegocio---------- 
# Endpoint Update 
@app.put('/undnegocio/update/{id}') 
def update_data(data: dict,id:str):  
	query="update undnegocio set nomundnegocio=%s  where codundnegocio='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/undnegocio/select') 
def conexion_postgres(): 
	query = 'SELECT codundnegocio,nomundnegocio from undnegocio order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/undnegocio/insert') 
def insert_data(data: dict): 
	query='insert into undnegocio(codundnegocio,nomundnegocio) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/undnegocio/delete/{id}') 
def delete_data(id: str): 
	query="delete from undnegocio where codundnegocio='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: vinculacion---------- 
# Endpoint Update 
@app.put('/vinculacion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update vinculacion set nomvic=%s  where vincpac='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/vinculacion/select') 
def conexion_postgres(): 
	query = 'SELECT vincpac,nomvic from vinculacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/vinculacion/insert') 
def insert_data(data: dict): 
	query='insert into vinculacion(vincpac,nomvic) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/vinculacion/delete/{id}') 
def delete_data(id: str): 
	query="delete from vinculacion where vincpac='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: tipomuestra---------- 
# Endpoint Update 
@app.put('/tipomuestra/update/{id}') 
def update_data(data: dict,id:str):  
	query="update tipomuestra set nombre=%s  where tipmues='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/tipomuestra/select') 
def conexion_postgres(): 
	query = 'SELECT tipmues,nombre from tipomuestra order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/tipomuestra/insert') 
def insert_data(data: dict): 
	query='insert into tipomuestra(tipmues,nombre) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/tipomuestra/delete/{id}') 
def delete_data(id: str): 
	query="delete from tipomuestra where tipmues='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: ocupacion---------- 
# Endpoint Update 
@app.put('/ocupacion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update ocupacion set nomocu=%s  where codocu='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/ocupacion/select') 
def conexion_postgres(): 
	query = 'SELECT codocu,nomocu from ocupacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/ocupacion/insert') 
def insert_data(data: dict): 
	query='insert into ocupacion(codocu,nomocu) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/ocupacion/delete/{id}') 
def delete_data(id: str): 
	query="delete from ocupacion where codocu='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: labseccion---------- 
# Endpoint Update 
@app.put('/labseccion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labseccion set nombre=%s,gruposeccion=%s,peso=%s  where codseccion='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labseccion/select') 
def conexion_postgres(): 
	query = 'SELECT codseccion,nombre,gruposeccion,peso from labseccion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labseccion/insert') 
def insert_data(data: dict): 
	query='insert into labseccion(codseccion,nombre,gruposeccion,peso) values (%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labseccion/delete/{id}') 
def delete_data(id: str): 
	query="delete from labseccion where codseccion='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: agencias---------- 
# Endpoint Update 
@app.put('/agencias/update/{id}') 
def update_data(data: dict,id:str):  
	query="update agencias set nomage=%s,ciuage=%s,depage=%s,dirage=%s,telage=%s,tipocons=%s,docpac=%s,resdian=%s,reqfd=%s,sinlogo=%s,predian=%s,maxfecres=%s,maxconsres=%s,tipofirma=%s,architect_prefijo=%s,proc=%s,codager=%s,domi=%s  where codage='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/agencias/select') 
def conexion_postgres(): 
	query = 'SELECT codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi from agencias order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/agencias/insert') 
def insert_data(data: dict): 
	query='insert into agencias(codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/agencias/delete/{id}') 
def delete_data(id: str): 
	query="delete from agencias where codage='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: examen---------- 
# Endpoint Update 
@app.put('/examen/update/{id}') 
def update_data(data: dict,id:str):  
	query="update examen set nombre=%s,codseccion=%s,cut=%s,soat=%s,nivexa=%s,nomcorto=%s,duracion=%s,tecnicas=%s,condiciones=%s,tipmues=%s,duraciont=%s,tiposerv=%s,inactiva=%s,entlun=%s,entmar=%s,entmie=%s,entjue=%s,entvie=%s,entsab=%s,entdom=%s,noproclun=%s,noprocmar=%s,noprocmie=%s,noprocjue=%s,noprocvie=%s,noprocsab=%s,noprocdom=%s  where cdgexamen='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/examen/select') 
def conexion_postgres(): 
	query = 'SELECT cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom from examen order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/examen/insert') 
def insert_data(data: dict): 
	query='insert into examen(cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/examen/delete/{id}') 
def delete_data(id: str): 
	query="delete from examen where cdgexamen='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: mae_unid---------- 
# Endpoint Update 
@app.put('/mae_unid/update/{id}') 
def update_data(data: dict,id:str):  
	query="update mae_unid set uni_desc=%s  where uni_codi='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/mae_unid/select') 
def conexion_postgres(): 
	query = 'SELECT uni_codi,uni_desc from mae_unid order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mae_unid/insert') 
def insert_data(data: dict): 
	query='insert into mae_unid(uni_codi,uni_desc) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/mae_unid/delete/{id}') 
def delete_data(id: str): 
	query="delete from mae_unid where uni_codi='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
# ---------------- tabla: analisis---------- 
# Endpoint Update 
@app.put('/analisis/update/{id}') 
def update_data(data: dict,id:str):  
	query="update analisis set cdgexamen=%s,cdganalisis=%s,nombre=%s,unicodi=%s,tipores=%s,cdganalisisa=%s,tiponorm=%s,aplica=%s,redondear=%s,redondeo=%s,tecnica=%s,grupo=%s,orden=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/analisis/select/{exa}') 
def conexion_postgres(exa: str): 
	query = "SELECT id,cdgexamen,cdganalisis,nombre,unicodi,tipores,cdganalisisa,tiponorm,aplica,redondear,redondeo,tecnica,grupo,orden from analisis where cdgexamen='"+ exa +"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/analisis/insert') 
def insert_data(data: dict): 
    #cdgexamen: `${miexamen}`,
    #cdganalisis:'',
    #Nombre:'',
    #unicodi:'',
    #tipores:'',
    #cdganalisisa:'S',
    #cdganalisisb:'',
    #tiponorm:'',
    #aplica:'',
    #redondear:'0',
    #redondeo:'0',
    #tecnica:'0',
    #grupo:'1',
    #orden:'99'    
	#print('examen ' + data['cdgexamen'] + ' analisis ' + data['cdganalisis'] + ' nombre ' + data['nombre'] + ' unidad ' + data['unicodi']  )
    va_examen = data['cdgexamen']
    va_anali = data['cdganalisis']
    va_nombre = data['nombre']
    va_uni = data['unicodi']
    va_tipores = data['tipores']
    va_cdganalisisa = data['cdganalisisa']
    va_tiponorm = data['tiponorm']
    va_aplica = data['aplica']
    va_redondear = data['redondear']
    va_redondeo = data['redondeo']
    va_tec = data['tecnica']
    va_grup = data['grupo']
    va_orden = data['orden']
   
    
    query="insert into analisis(cdgexamen,cdganalisis,nombre,unicodi,tipores,cdganalisisa,tiponorm,aplica,redondear,redondeo,tecnica,grupo,orden) "
    query = query + " values ('"+va_examen+"','"+va_anali+"','"+va_nombre+"','"+va_uni+"','"+va_tipores+"','"+va_cdganalisisa+"','"+va_tiponorm+"','"+va_aplica+"','"+va_redondear+"','"+va_redondeo+"','"+va_tec+"','"+va_grup+"','"+va_orden+"')" 
    sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/analisis/delete/{id}') 
def delete_data(id: str): 
	query="delete from analisis where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))     

 # ---------------- tabla: labvalores---------- 
# Endpoint Update 
@app.put('/labvalores/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labvalores set cdgexamen=%s,cdganalisis=%s,tecla=%s,resultado=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labvalores/select') 
def conexion_postgres(): 
	query = 'SELECT id,cdgexamen,cdganalisis,tecla,resultado from labvalores order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labvalores/insert') 
def insert_data(data: dict): 
	query='insert into labvalores(id,cdgexamen,cdganalisis,tecla,resultado) values (%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labvalores/delete/{id}') 
def delete_data(id: str): 
	query="delete from labvalores where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))   
 # ---------------- tabla: feriados---------- 
# Endpoint Update 
@app.put('/feriados/update/{id}') 
def update_data(data: dict,id:str):  
	query="update feriados set per=%s,fecha=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/feriados/select') 
def conexion_postgres(): 
	query = 'SELECT id,per,fecha from feriados order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/feriados/insert') 
def insert_data(data: dict): 
	query='insert into feriados(id,per,fecha) values (%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/feriados/delete/{id}') 
def delete_data(id: str): 
	query="delete from feriados where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))


 # ---------------- tabla: labcombo---------- 
# Endpoint Update 
@app.put('/labcombo/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labcombo set nombre=%s,cdgexamen=%s  where codcombo='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labcombo/select') 
def conexion_postgres(): 
	query = 'SELECT codcombo,nombre,cdgexamen from labcombo order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombo/insert') 
def insert_data(data: dict): 
	query='insert into labcombo(codcombo,nombre,cdgexamen) values (%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labcombo/delete/{id}') 
def delete_data(id: str): 
	query="delete from labcombo where codcombo='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
 # ---------------- tabla: labcombodet---------- 
# Endpoint Update 
@app.put('/labcombodet/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labcombodet set codcombo=%s,cdgexamen=%s,valor=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labcombodet/select') 
def conexion_postgres(): 
	query = 'SELECT id,codcombo,cdgexamen,valor from labcombodet order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombodet/insert') 
def insert_data(data: dict): 
	query='insert into labcombodet(id,codcombo,cdgexamen,valor) values (%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labcombodet/delete/{id}') 
def delete_data(id: str): 
	query="delete from labcombodet where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))                  

 # ---------------- tabla: lablistas---------- 
# Endpoint Update 
@app.put('/lablistas/update/{id}') 
def update_data(data: dict,id:str):  
	query="update lablistas set nombre=%s  where codlista='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/lablistas/select') 
def conexion_postgres(): 
	query = 'SELECT codlista,nombre from lablistas order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/lablistas/insert') 
def insert_data(data: dict): 
	query='insert into lablistas(codlista,nombre) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/lablistas/delete/{id}') 
def delete_data(id: str): 
	query="delete from lablistas where codlista='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
	
 # ---------------- tabla: examenemp---------- 
# Endpoint Update 
@app.put('/examenemp/update/{id}') 
def update_data(data: dict,id:str):  
	query="update examenemp set codemp=%s,cdgexamen=%s,descc=%s,nivel=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/examenemp/select') 
def conexion_postgres(): 
	query = 'SELECT id,codemp,cdgexamen,descc,nivel from examenemp order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/examenemp/insert') 
def insert_data(data: dict): 
	query='insert into examenemp(id,codemp,cdgexamen,descc,nivel) values (%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/examenemp/delete/{id}') 
def delete_data(id: str): 
	query="delete from examenemp where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))    
	
 # ---------------- tabla: labdepend---------- 
# Endpoint Update 
@app.put('/labdepend/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labdepend set codemp=%s,coddep=%s,nombre=%s,desc0=%s,pyp=%s,nofac=%s,domi=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labdepend/select') 
def conexion_postgres(): 
	query = 'SELECT id,codemp,coddep,nombre,desc0,pyp,nofac,domi from labdepend order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labdepend/insert') 
def insert_data(data: dict): 
	query='insert into labdepend(id,codemp,coddep,nombre,desc0,pyp,nofac,domi) values (%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labdepend/delete/{id}') 
def delete_data(id: str): 
	query="delete from labdepend where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: labempresa---------- 
# Endpoint Update 
@app.put('/labempresa/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labempresa set nombre=%s,n_ide=%s,dir=%s,tel=%s,ciudad=%s,codcla=%s,codlista=%s,desce=%s,codadm=%s,itemsfac=%s,codcob=%s,contacto=%s,fax=%s,coddep=%s,ciclofac=%s,repbono=%s,repcumo=%s,repcopa=%s,repdesc=%s,repmode=%s,inactiva=%s,informacion=%s,nithelisa=%s,codlista2=%s,requisitos=%s,ccosto=%s,codempt=%s,prefijorip=%s,digitosfac=%s,tipcon=%s  where codemp='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labempresa/select') 
def conexion_postgres(): 
	query = 'SELECT codemp,nombre,n_ide,dir,tel,ciudad,codcla,codlista,desce,codadm,itemsfac,codcob,contacto,fax,coddep,ciclofac,repbono,repcumo,repcopa,repdesc,repmode,inactiva,informacion,nithelisa,codlista2,requisitos,ccosto,codempt,prefijorip,digitosfac,tipcon from labempresa order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labempresa/insert') 
def insert_data(data: dict): 
	query='insert into labempresa(codemp,nombre,n_ide,dir,tel,ciudad,codcla,codlista,desce,codadm,itemsfac,codcob,contacto,fax,coddep,ciclofac,repbono,repcumo,repcopa,repdesc,repmode,inactiva,informacion,nithelisa,codlista2,requisitos,ccosto,codempt,prefijorip,digitosfac,tipcon) values (%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%,%)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labempresa/delete/{id}') 
def delete_data(id: str): 
	query="delete from labempresa where codemp='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
        
 # ---------------- tabla: medicos---------- 
# Endpoint Update 
@app.put('/medicos/update/{id}') 
def update_data(data: dict,id:str):  
	query="update medicos set nommedico=%s,ccmedico=%s,espmedico=%s,perfil=%s,celular=%s,tel=%s,ciudad=%s,codundnegocio=%s,usuario=%s,firma=%s,presentacion=%s  where codmedico='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/medicos/select') 
def conexion_postgres(): 
	query = 'SELECT codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion from medicos order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/medicos/insert') 
def insert_data(data: dict): 
	query='insert into medicos(codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion) values (%,%,%,%,%,%,%,%,%,%,%,%)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/medicos/delete/{id}') 
def delete_data(id: str): 
	query="delete from medicos where codmedico='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))        

# ---------------- tabla: usuarios---------- 
# Endpoint Update 
@app.put('/usuarios/update/{id}') 
def update_data(data: dict,id:str):  
	query="update usuarios set nombre=%s,tipo=%s,estado=%s  where usuario='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/usuarios/select') 
def conexion_postgres(): 
	query = 'SELECT usuario,nombre,tipo,estado from usuarios order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/usuarios/insert') 
def insert_data(data: dict): 
	query='insert into usuarios (usuario,nombre,tipo,estado) values (%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/usuarios/delete/{id}') 
def delete_data(id: str): 
	query="delete from usuarios where usuario='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))	
	
 # ---------------- tabla: ipsconsec---------- 
# Endpoint Update 
@app.put('/ipsconsec/update/{id}') 
def update_data(data: dict,id:str):  
	query="update ipsconsec set docu=%s,codage=%s,num=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/ipsconsec/select') 
def conexion_postgres(): 
	query = 'SELECT id,docu,codage,num from ipsconsec order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/ipsconsec/insert') 
def insert_data(data: dict): 
	query='insert into ipsconsec(docu,codage,num) values (%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/ipsconsec/delete/{id}') 
def delete_data(id: str): 
	query="delete from ipsconsec where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))	
	
 # ---------------- tabla: mediospago---------- 
# Endpoint Update 
@app.put('/mediospago/update/{id}') 
def update_data(data: dict,id:str):  
	query="update mediospago set desmed=%s  where codmed='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/mediospago/select') 
def conexion_postgres(): 
	query = 'SELECT codmed,desmed from mediospago order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mediospago/insert') 
def insert_data(data: dict): 
	query='insert into mediospago(codmed,desmed) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/mediospago/delete/{id}') 
def delete_data(id: str): 
	query="delete from mediospago where codmed='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: labordenpago---------- 
# Endpoint Update 
@app.put('/labordenpago/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labordenpago set fecha=CURRENT_TIMESTAMP,codage=%s,numorden=%s,codmed=%s,valor=%s,pend=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labordenpago/select/{miage}/{miord}') 
def conexion_postgres(miage:str,miord=str): 
	query = "SELECT id,codage,numorden,codmed,valor,pend,fecha from labordenpago where codage='"+ miage + "' and numorden=" + miord + " order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labordenpago/insert') 
def insert_data(data: dict): 
	query='insert into labordenpago(codage,numorden,codmed,valor,pend,fecha) values (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labordenpago/delete/{id}') 
def delete_data(id: str): 
	query="delete from labordenpago where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
        
 # ---------------- tabla: opciones---------- 
# Endpoint Update 
@app.put('/opciones/update/{id}') 
def update_data(data: dict,id:str):  
	query="update opciones set opcion=%s,nombre=%s,ruta=%s,mostrar=%s,orden=%s,carpeta=%s  where opcion='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/opciones/select') 
def conexion_postgres(): 
	query = 'SELECT opcion,nombre,ruta,mostrar,orden,carpeta from opciones order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/opciones/insert') 
def insert_data(data: dict): 
	query='insert into opciones(opcion,nombre,ruta,mostrar,orden,carpeta) values (%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/opciones/delete/{id}') 
def delete_data(id: str): 
	query="delete from opciones where opcion='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: roles---------- 
# Endpoint Update 
@app.put('/roles/update/{id}') 
def update_data(data: dict,id:str):  
	query="update roles set role=%s,nombre=%s  where role='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/roles/select') 
def conexion_postgres(): 
	query = 'SELECT role,nombre from roles order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/roles/insert') 
def insert_data(data: dict): 
	query='insert into roles(role,nombre) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/roles/delete/{id}') 
def delete_data(id: str): 
	query="delete from roles where role='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: roleopcion---------- 
# Endpoint Update 
@app.put('/roleopcion/update/{id}') 
def update_data(data: dict,id:str):  
	query="update roleopcion set role=%s,opcion=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/roleopcion/select') 
def conexion_postgres(): 
	query = 'SELECT id,role,opcion from roleopcion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/roleopcion/insert') 
def insert_data(data: dict): 
	query='insert into roleopcion(role,opcion) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/roleopcion/delete/{id}') 
def delete_data(id: str): 
	query="delete from roleopcion where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: usuariorole---------- 
# Endpoint Update 
@app.put('/usuariorole/update/{id}') 
def update_data(data: dict,id:str):  
	query="update usuariorole set usuario=%s,role=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/usuariorole/select') 
def conexion_postgres(): 
	query = 'SELECT id,usuario,role from usuariorole order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/usuariorole/insert') 
def insert_data(data: dict): 
	query='insert into usuariorole(usuario,role) values (%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/usuariorole/delete/{id}') 
def delete_data(id: str): 
	query="delete from usuariorole where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))



 # ---------------- tabla: laborden---------- 
# Endpoint Update 
@app.put('/laborden/update/{id}') 
def update_data(data: dict,id:str):  
	query="update laborden set fecorden=%s,estado=%s,codage=%s,numorden=%s,agefaccli=%s,numfaccli=%s,numfaccli=%s,tipide=%s,codpac=%s,codemp=%s,contpac=%s,contpac=%s,interlab=%s,prio=%s,codmedico=%s,nivpac=%s,copago=%s,cuotam=%s,bono=%s,descpac=%s,abopac=%s,coddiagnostico=%s,empcodi=%s,percodi=%s,totemp=%s,codpac=%s,usuario=%s,dur=%s,descpacp=%s,factura=%s,edadf=%s,facturar=%s,pendaprob=%s,embar=%s,fechasol=%s,usuvbo=%s,horvbo=%s,idbono=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/laborden/select') 
def conexion_postgres(): 
	query = 'SELECT id,fecorden,estado,codage,numorden,agefaccli,numfaccli,numfaccli,tipide,codpac,codemp,contpac,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,empcodi,percodi,totemp,codpac,usuario,dur,descpacp,factura,edadf,facturar,pendaprob,embar,fechasol,usuvbo,horvbo,idbono from laborden order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/laborden/insert') 
def insert_data(data: dict):
        
	query='insert into laborden(fecorden,codage,numorden,agefaccli,numfaccli,tipide,codpac,codemp,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,totemp,usuario,dur,descpacp,factura,fechasol,usuvbo,horvbo,idbono,totpac) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/laborden/delete/{id}') 
def delete_data(id: str): 
	query="delete from laborden where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: labordendet---------- 
# Endpoint Update 
@app.put('/labordendet/update/{id}') 
def update_data(data: dict,id:str):  
	query="update labordendet set cdgexamen=%s,valor=%s,coddep=%s,desc1=%s,desc2=%s,desc3=%s,cuotam=%s,ordenam=%s,partic=%s,corte=%s,pend=%s,codcombo=%s,subtemp=%s,seq=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/labordendet/select') 
def conexion_postgres(): 
	query = 'SELECT id,cdgexamen,valor,coddep,desc1,desc2,desc3,cuotam,ordenam,partic,corte,pend,codcombo,subtemp,seq from labordendet order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labordendet/insert') 
def insert_data(data: dict): 
	query='insert into labordendet(cdgexamen,valor,coddep,desc1,desc2,desc3,cuotam,ordenam,partic,corte,pend,codcombo,subtemp,seq,codage,numorden,subtpac) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/labordendet/delete/{id}') 
def delete_data(id: str): 
	query="delete from labordendet where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))

 # ---------------- tabla: paciente---------- 
# Endpoint Update 
@app.put('/paciente/update/{id}') 
def update_data(data: dict,id:str):  
	query="update paciente set tipide=%s,codpac=%s,nompac=%s,nompac2=%s,apepac=%s,apepac2=%s,sexo=%s,vincpac=%s,fecnac=%s,fecing=%s,codocu=%s,deppac=%s,ciupac=%s,gruposang=%s,codemp=%s,coddiagnostico=%s,contpac=%s,planben=%s,codundnegocio=%s,nivpac=%s,obs=%s,dir=%s,tel=%s,remite=%s,cedaco=%s,nomaco=%s,apeaco=%s,telaco=%s,diraco=%s,empcodi=%s,celular=%s,acofam=%s  where id='"+id+"'"  
	sdk.updatePostgres(query, data,'prd') 
# Endpoint Select 
@app.get('/paciente/select') 
def conexion_postgres(): 
	query = 'SELECT id,tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,empcodi,celular,acofam from paciente order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/paciente/insert') 
def insert_data(data: dict): 
	query='insert into paciente(tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,celular,acofam,id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
	sdk.insertPostgres(query, data,'prd') 
# Endpoint delete 
@app.delete('/paciente/delete/{id}') 
def delete_data(id: str): 
	query="delete from paciente where id='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))


# ******************** fin CRUD ********************************************


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
