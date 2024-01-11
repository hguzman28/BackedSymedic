import datetime
from fastapi import FastAPI, HTTPException
import sdk
import os
from mangum import Mangum
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json
import re

#
#class User(BaseModel):
#    name: str
#    age: int

#@app.post("/user")
#async def create_user(user: User):
    # Validate the user input
#    if user.name is None:
#        raise HTTPException(status_code=400, detail="Name is required")
#     else:
#        return {"statusCode": 200,"resultado": "success"}



#importar pydantic
from pydantic import BaseModel, Field, EmailStr

#importar servicios dao para parametros generales
# import dao_parametros


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
app = FastAPI(title="seed-fast-api", root_path = openapi_prefix)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

def ifnull(var, val):
  if var is None:
    return val
  return var

###############################################################################
#   Select con conx para postgrest                                                   #
###############################################################################

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
    va_tamano = 0
    for obj in response:
        va_query = obj['consulta']
        response_data = sdk.executeQueryPostgresSelect(va_query, str(stage))
        response_copia = response_data 
        va_columnas = obj['columnas']
        va_medidas = obj['medidas']
             
        """      
        # ----------------- ahora pasarlo a array ------------------------
        va_campos = va_columnas + ',' + va_medidas
        campos_lista = va_campos.split(',')
        campos_lista = [campo.strip() for campo in campos_lista]
        
        arreglo_final = []
        num_columnas = 0
        contador = 1
        for obj2 in response_data: #obj2 es cada registro del array de resultados
            registro = []
            if (contador==1): # la primera vez
                num_columnas = len(campos_lista)
                arreglo_final.append(campos_lista)
            for campo in campos_lista: #['campo1','campo2','campo3']
                registro.append(obj2[campo])
            contador = contador + 1
            arreglo_final.append(registro)        
        """
    return {"statusCode": 200,"resultado": "success","filas": 1000 ,"columnas":va_columnas,"medidas":va_medidas,"data": list(response_copia) }


@app.get('/reportes/findarray/{rep}') # con formato para googlecharts sin parametros
def conexion_postgres( rep:str):
    #Carpetas
    ds = {}
    qry = "select consulta,filtros,columnas,medidas from zreportes where cod=" + rep
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_tamano = 0
    for obj in response:
        va_query = obj['consulta']
        va_tokens =  re.split(r"\W+", va_query)
        va_columnas = obj['columnas']
        va_medidas =  obj['medidas']

        va_campos = va_columnas + ',' + va_medidas
        campos_lista = va_campos.split(',')
        campos_lista = [campo.strip() for campo in campos_lista]
        response_data = sdk.executeQueryPostgresSelect(va_query, str(stage))
        arreglo_final = []
        arreglo_columnas = []
        num_columnas = 0
        contador = 1
        for obj2 in response_data: #obj2 es cada registro del array de resultados
            registro = []
            if (contador==1): # la primera vez
                num_columnas = len(campos_lista)
                arreglo_final.append(campos_lista)
            for campo in campos_lista: #['campo1','campo2','campo3']
                #print('insertanto '+campo + ' =>' + obj2[campo] )
                registro.append(obj2[campo])
            contador = contador + 1
            arreglo_final.append(registro) 
        
    return {"statusCode": 200,"resultado": "success","filas": contador ,"columnas":va_columnas,"medidas":va_medidas,"data": list(arreglo_final)}

@app.post('/reportes/findarrayparam/{rep}') # con formato para googlecharts con parametros
def conexion_postgres( data:dict, rep:str):
    #Carpetas
    #ds = {}
    #print('parametros que llegan al backend **************')
    #print( data['parametros'][0]['titulo']);
    #print( data['parametros'][0]['valor']);
    
    param = data['parametros']  # [{tipo:pt,titulo:empresa, orden:0},{tipo:pf,titulo:fecha_ini, orden:1}]
    qry = "select consulta,filtros,columnas,medidas from zreportes where cod=" + rep
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_tamano = 0
    for obj in response:
        va_query = obj['consulta']
        qry_tmp = ''
        comillas = ''
        for item in data['parametros']:
            if item['tipo'] == 'pn':
                comillas=""
            else:
                comillas = chr(39)
            valor_viejo = item['tipo']+ ":" + item['titulo']
            valor_nuevo = comillas + item['valor'] + comillas
            qry_tmp =  va_query.replace(valor_viejo , valor_nuevo )
            va_query = qry_tmp
        print(va_query)

        va_tokens =  re.split(r"\W+", va_query)
        va_columnas = obj['columnas']
        va_medidas =  obj['medidas']

        va_campos = va_columnas + ',' + va_medidas
        campos_lista = va_campos.split(',')
        campos_lista = [campo.strip() for campo in campos_lista]
        response_data = sdk.executeQueryPostgresSelect(va_query, str(stage))
        arreglo_final = []
        arreglo_columnas = []
        num_columnas = 0
        contador = 1
        for obj2 in response_data: #obj2 es cada registro del array de resultados
            registro = []
            if (contador==1): # la primera vez
                num_columnas = len(campos_lista)
                arreglo_final.append(campos_lista)
            for campo in campos_lista: #['campo1','campo2','campo3']
                registro.append(obj2[campo])
            contador = contador + 1
            arreglo_final.append(registro) 
        
    return {"statusCode": 200,"resultado": "success","filas": contador ,"columnas":va_columnas,"medidas":va_medidas,"data": list(arreglo_final)}


@app.get('/reportes/getparam/{rep}') # trae los parametros necesarios para correr el reporte
def conexion_postgres(rep:str):
    qry = "select consulta,filtros,columnas,medidas from zreportes where cod=" + rep
    response = sdk.executeQueryPostgresSelect(qry, str(stage))
    parametros = []
    params = {}
    for obj in response:
        va_query = obj['consulta']
        va_tokens =  re.split(r"\W+", va_query)
        pos = 0
        pos_abs = 0
        for token in va_tokens:
            #print(token.lower())
            if (token.lower() == 'pt' or token.lower() == 'pf' or token.lower() == 'pn' ):
                params = {"tipo":token.lower(), "titulo": va_tokens[pos+1],"pos": pos_abs }
                parametros.append(params)
                pos_abs = pos_abs +1
            pos = pos + 1    
    return {"statusCode": 200,"resultado": "success","parametros": parametros}

################################### LISTA DE TRABAJO ################################

@app.post('/listatrabajo')
def conexion_postgres(data: dict):
    va_where = data['where']
    va_orderby = " order by x.cdgexamen "#data['orden']
    print('> ' +  va_where + ' <' )
    #row_number() OVER ("+ va_orderby +")
    query="select row_number() OVER ("+ va_orderby +") AS consec,x.id,o.codage,o.numorden,x.cdgexamen,e.nombre as nomexamen , x.proc, o.tipide ,o.codpac,p.nompac ||' '||p.apepac as nompac,o.edadf, o.usuario usurecep,o.medfirma,o.horfirma,to_char(o.fecent,'ddmmyyyy') fecent,o.horent ,o.prio,o.codemp,l.nombre as nomemp,o.motivo, p.antefam,x.medfirmad, x.horfirmad  ";
    query=query+" from labordendet x,examen e,laborden o,paciente p,labempresa l "
    query=query+" where x.cdgexamen=e.cdgexamen  "
    query=query+" and x.ordenl = o.ordenl "
    query=query+" and o.tipide=p.tipide "
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

@app.post('/listatrabajo/firmar')
def conexion_postgres(data: dict):
# se usa para firmar rangos de examenes en al lista de trabajo, solo para firma de orden    
    va_usuario = data['usuario']
    va_listado = data['listado']
    print('listado a firmar en servicio')
    print( va_listado)
    qry = "select codmedico,nommedico from medicos where usuario='" + va_usuario + "'"
    response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_med=''
    va_nom=''
    for obj in response_med:
        va_med = obj['codmedico']
        va_nom = obj['nommedico']
    
    print (" medico "+va_med)

    va_items = 0
    for ob in va_listado: # para cada uno de los labordendet
        print (ob)
        if (ob != None):
            va_codage = ''
            qry="select codage,numorden from labordendet where id="+ str(ob)
            response_det = sdk.executeQueryPostgresSelect(qry, str(stage))
            for obja in response_det:
                va_codage = obja['codage']
                va_ord = obja['numorden']


            qry = "select tipofirma,to_char(current_timestamp,'yyyymmdd:hh24miss') as ts from agencias where codage='" + va_codage + "'"
            response_age = sdk.executeQueryPostgresSelect(qry, str(stage))
            for obja in response_age:
                va_tipof = obja['tipofirma']
                va_ts = obja['ts']

            print (" tipofirma "+va_tipof)

            if (va_med != ''):
                print (" firmar la orden")
                if (va_tipof == 'O'):
                    print (" firmar encabezado")
                    qry = "update laborden set medfirma='" + va_med + "'" 
                    qry = qry + ",horfirma=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + va_codage +"' and numorden=" + str(va_ord) 
                    sdk.updatePostgres(qry, data,"prd")
                else:
                    #print (" firmar solo el examen, seq=> "+ (ob)) 
                    qry = "update labordendet set medfirmad ='" + va_med +"' "
                    qry = qry + ",horfirmad =to_char(current_timestamp,'yyyymmdd:hh24miss') where id =" + str(ob)
                    sdk.updatePostgres(qry, data,"prd") 
                exitoso = 'SI'
                mensaje = "Gracias por sus firma Dr(a) " + va_nom
            else: # es un usuario sin medico asociado
                mensaje = 'Usuario No habilitado para Firmar'
                exitoso = 'NO'     
                #except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
            if (exitoso == 'SI'):
                resu = 'success'
            else:
                resu = 'failure'
                mensaje = 'Usuario no corresponde a ningun medico registrado'
    print(mensaje)
    return {"statusCode": 200,"resultado": "ok","mensaje":mensaje,"medico":va_med,"ts":va_ts}

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
            query = "select opcion as id,opcion ||'-'|| r.nombre as name  from opciones r order by 2 "
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
        if (lista.lower() =='roles'):
            query = "select role as id,nombre as name from roles order by 1"
        if (lista.lower() =='mediospago'):
            query = "select codmed as id,desmed as name from mediospago m  order by 1"
        if (lista.lower() =='color'):
            query = "select cod as id,horai || '-'|| horaf as name from color order by 1"
        if (lista.lower() =='labempresa'):
            query = "select codemp as id, codemp ||'-'|| nombre as name from labempresa order by 2"    
        if (lista.lower() =='tipoident'):
            query = "select id, nombre as name from tipoident order by 2"    
        if (lista.lower() =='ocupacion'):
            query = "select codocu as id, nomocu as name from ocupacion order by 2"    
        if (lista.lower() =='vinculacion'):
            query = "select vincpac as id, nomvic as name from vinculacion order by 2"    
        if (lista.lower() =='labcombo'):
            query = "select codcombo as id, nombre as name from labcombo order by 2"        


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
            query = "select cdgexamen as id,'('||cut||') '||nombre as name from examen where 1=1 and upper(cdgexamen||cut||nombre) like '%"+ patron + "%' order by 2"
        if (lista.lower() =='pacientes'):
            query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
        if (lista.lower() =='diagnosticos'):
            query = "select coddiagnostico as id,nomdiagnostico as name from diagnostico where upper(coddiagnostico) like '%"+ patron + "%' or upper(nomdiagnostico) like '%"+ patron + "%' order by 2"
        if (lista.lower() =='medicos'):
            query = "select codmedico as id,nommedico as name from medicos where 1=1 and upper(codmedico||nommedico) like '%"+ patron + "%' order by 2"
       

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

# sirve para validar contra tablas de lista larga por la llave primaria
@app.get('/validate/diagnosticos/{dia}')
def conexion_postgres(dia:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        if (dia != '' and dia != None):
            va_nombre = ''
            query=''
            query = "select nomdiagnostico as name from diagnostico where coddiagnostico = '"+ dia + "'"
            #  query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
            response_query = sdk.executeQueryPostgresSelect(query, str(stage))
            for obj in response_query:
                va_nombre = obj['name']
                return {'name':va_nombre}
        else:
            return {'name':''}
# sirve para validar contra tablas de lista larga por la llave primaria
@app.get('/validate/medicos/{med}')
def conexion_postgres(med:str):
        #pat = patron.upper()
        #filtro = "'%{}%'".format(pat);
        # print(filtro)
        va_nombre = ''
        query=''
        query = "select nommedico as name from medicos where codmedico = '"+ med + "'"
        #  query = "select codpac as id,nompac||' '|| apepac||' '||apepac2 as name from paciente where upper(codpac) like '%"+ patron + "%' or upper(nompac) like '%"+ patron + "%' or upper(apepac) like '%"+ patron + "%' or upper(apepac2) like '%"+ patron + "%'  order by 2"
        response_query = sdk.executeQueryPostgresSelect(query, str(stage))
        for obj in response_query:
            va_nombre = obj['name']
        return {'name':va_nombre}



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

# funcion para validar si la cadena digitada se puede almacenar en resnum
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

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
    print("resultado/update/" + id)
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
    cadresnum = ''
    if (isfloat(va_resultado)):
         cadresnum = ",resnum="+va_resultado
    query = ''
    # en 202311 se establece que los id no pueden ser todos cero, entonces se adopta la nomenclatura 0_1 0_2 0_3 ...
    print(" subcadena de id " + id[0:2]);
    if (id[0:2] != "0_"):            
        query="update resultado set resultado='"+va_resultado + cadresnum + "',usuario='"+va_usuario+"',fecha=CURRENT_TIMESTAMP where id=" + id
        print(query)
        sdk.updatePostgres(query, data,"prd")
    else:
        if (not isfloat(va_resultado)):
            query ="insert into resultado (resultado,usuario,codage,numorden,seq,cdgexamen,cdganalisis,tipores,unicodi) "
            query=query + " values ('"+va_resultado+"','"+va_usuario+"','"+va_age+"','"+va_ord+"','"+va_seq+"','"+va_examen+"','"+va_anali+"','"+va_tipores+"','"+va_unidad+"') "
        else:
            query ="insert into resultado (resultado,resnum,usuario,codage,numorden,seq,cdgexamen,cdganalisis,tipores,unicodi) "
            query=query + " values ('"+va_resultado+"'," + va_resultado + ",'"+va_usuario+"','"+va_age+"','"+va_ord+"','"+va_seq+"','"+va_examen+"','"+va_anali+"','"+va_tipores+"','"+va_unidad+"') "
        print(query)
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
    posfirma = data['posfirma'] # 1 o 2, primera o segunda

    print (" seq =  ")
    print(seq  )

    medico = ''
    campofirma='medfirmad'
    campohora = 'horfirmad'
    if (posfirma == '1'):
        campofirma='medfirmad'
        campohora = 'horfirmad'
    if (posfirma == '2'):
        campofirma='medfirmad2'
        campohora = 'horfirmad2'

    qry = "select codmedico,nommedico from medicos where usuario='" + user + "'"
    response_med = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_med=''
    va_nom=''
    for obj in response_med:
        va_med = obj['codmedico']
        va_nom = obj['nommedico']
    
    print (" medico "+va_med)

    qry = "select tipofirma,to_char(current_timestamp,'yyyymmdd:hh24miss') as ts from agencias where codage='" + age + "'"
    response_age = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_age:
        va_tipof = obja['tipofirma']
        va_ts = obja['ts']

    print (" tipofirma "+va_tipof)


    if (va_med != ''):
        if (tipo=='E'):
            print (" firmar elaborado")
            query="update laborden set medfirmae='" + va_med + "'" 
            query = query + ",horfirmae=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
            sdk.updatePostgres(query, data,"prd")
        else:
            print (" firmar la orden")
            if (va_tipof == 'O'):
                print (" firmar encabezado")
                qry = "update laborden set medfirma='" + va_med + "'" 
                qry = qry + ",horfirma=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age+"' and numorden='" + ord + "'"
                sdk.updatePostgres(qry, data,"prd")
            else:
                print (" firmar solo el examen, seq=> "+ str(seq) + "orden =>" + ord + "campohora=>"+ campohora)
                qry = "update labordendet set " + campofirma + "='" + va_med +"' "
                qry = qry + "," + campohora + "=to_char(current_timestamp,'yyyymmdd:hh24miss') where codage='" + age + "' and numorden='" + ord + "' and seq=" + str(seq)
                sdk.updatePostgres(qry, data,"prd") 
        exitoso = 'SI'
        mensaje = "Gracias por su firma ("+ posfirma +"), Dr(a) " + va_nom
    else: # es un usuario sin medico asociado
        mensaje = 'Usuario No habilitado para Firmar'
        exitoso = 'NO'     
    if (exitoso == 'SI'):
         resu = 'success'
    else:
         resu = 'failure'
         mensaje = 'Usuario no corresponde a ningun medico registrado'
    return {"statusCode": 200,"resultado": resu,"mensaje":mensaje,"medico":va_med,"ts":va_ts}



# ******************** esta firmada una orden ? *****************************************

def orden_firmada(age:str,ord:str):
  
    va_tipof = ''
    # tipo de firma
    qry = "select tipofirma from agencias where codage='" + age + "'"
    response_age = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_age:
        va_tipof = obja['tipofirma']

    va_firma_e = ''
    va_firmada = False
    if (va_tipof=='O'):
        qry="select medfirma from laborden where codage='" + age+"' and numorden='" + ord + "'" 
        response_t = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_t:
            va_firma_e = obj['medfirma']
            if ((va_firma_e!="") and (va_firma_e != None)):
                va_firmada = True      
    else: # tipo E
        va_totales = 0
        va_firmados = 0
        qry = "select count(*) as tot from labordendet where codage='" + age+ "' and numorden='" + ord + "'" 
        response_tot = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_tot:
            va_totales = obj['tot']
        qry = "select count(*) as tot from labordendet d,examen e where d.codage='" + age+ "' and d.numorden='" + ord + "' " 
        qry = qry +" and d.cdgexamen=e.cdgexamen and ((d.medfirmad is not null and d.medfirmad <>'' and e.numfirmas=1) or (d.medfirmad is not null and d.medfirmad2 is not null and d.medfirmad <>'' and d.medfirmad2 <>'' and e.numfirmas=2)) " 
        response_fir = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj2 in response_fir:
            va_firmados = obj2['tot']
        if ((va_totales>0) and (va_totales == va_firmados)):
            va_firmada = True
        else:
            va_firmada = False

    return va_firmada


@app.get('/orden/firmada/{age}/{ord}')
def orden_firmadas(age:str,ord:str):
    va_firmada = orden_firmada(age,ord)
    return {"statusCode": 200,"firmada": va_firmada}
                     

####################### servicio resultados IMPRESION ##################################
# Este servicio suministra la totalidad de los campos necesarios
# para imprimir los resultados de la orden de laboratorio
# Ademas valida si la orden esta firmada, pagada, si usuario es medico y la op es del medico
# si la op es de empresa y es mi empresa 
@app.post('/resultado/find/{codage}/{numorden}')
def conexion_postgres(body:dict, codage:str,numorden:str):
#data: dict,
    incluir =  body['incluirexamenes']   # las secuencias q se deben incluir
    usuario = body['usuario'] #usuario que solicita imprimir
    # armaremos una cadena para la condicion de las secuencias a incluir
    # {
    #"usuario":"",
    #"incluirexamenes":{"0":"S","1":"S"}
    #}
    va_medfirmad = ''
    va_horfirmad = ''
    va_medfirmad2 = ''
    va_horfirmad2 =''

    print('incluir ++++++++++++++++')
    print(len(incluir))
    print(incluir)
    if (incluir and len(incluir) > 0):
        cad_incluir = ','.join(key for key, value in incluir.items() if value == 'S')

    if len(cad_incluir)>0:
        cad_incluir = " and d.seq in (" + cad_incluir + " )"
    else:
        cad_incluir=''    

    print('=====> ' + cad_incluir)

    #cad_incluye = '';
    #for x in range(0,len(incluir)-1):
    #    if (incluir[x] == 'S'):
    #          cad_incluye = cad_incluye + ',' + x

   #Direccion y telefonos sede ppal
    qry = "select texto,orden from textos where cod='PPAL' order by orden "
    response_querysp = sdk.executeQueryPostgresSelect(qry, str(stage))

    # Bolos del tope y piede la pagina
    respuesta=[]
    va_bolo_examen = ''
    va_respie = ''
    va_restop = ''
    va_codmedico = '' # medico de la orden
    va_codempresa = '' # empresa de la orden
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
    qry = qry + " o.codemp,e.nombre as nomemp,p.sexo,o.edadf ,p.tel, a.nomage , m.nommedico, to_char(o.fecorden,'ddmmyyyy') as fecorden,medfirma,horfirma, totpac-abopac as saldo, o.codmedico "  
    qry = qry + "        from laborden o,paciente p, labempresa e, agencias a , medicos m " 
    qry = qry + "        where o.codage='"+codage+"' and o.numorden= " + numorden
    qry = qry + "        and o.tipide=p.tipide "
    qry = qry + "        and o.codpac=p.codpac "
    qry = qry + "        and o.codemp=e.codemp "
    qry = qry + "        and o.codage = a.codage and o.codmedico = m.codmedico"
    response_query0 = sdk.executeQueryPostgresSelect(qry, str(stage))
    datapac={}
    va_saldo = 0
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
        va_codmedico = obj['codmedico']
        va_fec = obj['fecorden']
        va_nomemp = obj['nomemp']
        va_fecorden = obj['fecorden']
        va_medfirma = obj['medfirma'] #medico que firma
        va_horfirma = obj['horfirma']
        va_codempresa = obj['codemp']
        va_saldo = obj['saldo'] # saldo pendiente de la orden

        datapac = {"ordenl":va_ordenl,"codpac":va_codpac,"nombre":va_nombre,"sexo":va_sexo,"edad":va_edad,"tel":va_tel,"age":va_agencia,"medico":va_med,"empresa":va_nomemp,"fecorden":va_fecorden,"medfirma":va_medfirma,"horfirma":va_horfirma}

    va_memb = 'membrete.png'
    qry = "select imagen from labempresaplus where codemp = '"+va_codempresa+"'"
    response_memb = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obj in response_memb:
        va_memb = obj['imagen']

    va_pagado = 'S'
    if (va_saldo <= 0):
        va_pagado ='S'
    else:
        va_pagado = 'N'    

    # ---------- ESTABLECEMOS QUE TIPO DE USUARIO ESTA SOLICITANDO IMPRIMIR -----------
    va_tipousuario = ''
    va_medic_request = '' # medico que esta solicitando el resultado
    va_empresa_reques = '' # empresa del usuario q solicita el resultado
    va_totusu = 0
    if (usuario==""):
        va_tipousuario = 'X'
    else:      
        qry = "select count(*) as usu,max(codmedico) as medi from medicos where usuario='"+usuario+"'"
        response_query_m = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_query_m:
            va_totusu = obj['usu']
            va_medic_request = obj['medi']
        if va_totusu > 0:
            va_tipousuario = 'M' # ES medico
        else:
            qry = "select tipo,codemp from usuarios where usuario='"+usuario+"'"
            response_query_u = sdk.executeQueryPostgresSelect(qry, str(stage))
            for obj in response_query_u:
               va_tipousuario = obj['tipo']
               va_empresa_request = obj['codemp']
    if (va_tipousuario == ''):
        va_tipousuario = 'X'
            
    #va_tipousuario = X,I,E,M
    # ------------------------------ DETALLE DE EXAMENES ---------------------------
    # los distintos examenes de la orden de laboratorio
    qry = "select distinct r.seq,r.cdgexamen,e.nombre as nomexamen,r.usuario,medfirmad,horfirmad,medfirmad2,horfirmad2  "
    qry = qry + "from resultado r,examen e, labordendet d "
    qry = qry + "where r.cdgexamen=e.cdgexamen  " 
    qry = qry + "and r.codage='"+codage+"' and r.numorden="+numorden+" "
    qry = qry +" and r.ordenl = d.ordenl and r.seq= d.seq and r.resultado is not null " + cad_incluir    
    response_query = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    for obj in response_query:
        va_examen = obj['cdgexamen']
        va_nomexamen = obj['nomexamen']
        va_usuario = obj['usuario']
        va_seq = obj['seq']
        va_medfirmad = obj['medfirmad']
        va_horfirmad = obj['horfirmad']
        va_medfirmad2 = obj['medfirmad2']
        va_horfirmad2 = obj['horfirmad2']

        va_bolo_examen = ''
        qry = "select texto from textos where aplica like '%"+va_examen+"%'"
        response_query_textos = sdk.executeQueryPostgresSelect(qry, str(stage))
        for obj in response_query_textos:
            va_bolo_examen = obj['texto']
        
        # -------------- DETALLE DE ANALISIS ----------------------------
        # los distintos analisis del examen (seq) de la orden de laboratorio            
        qry = "select r.cdganalisis, a.nombre as nomanalisis, "
        qry = qry + "r.resultado,r.fecha,r.tipores,r.resnum,r.unicodi,r.usuario  "
        qry = qry + " ,getvalnormals('"+va_fec+"','"+va_tip+"','"+va_codpac+"',r.cdgexamen,r.cdganalisis,'"+codage+"','"+numorden+"') as valnormal  "
        qry = qry + " ,resultadoant('"+va_fec+"',r.cdgexamen,r.cdganalisis,'"+va_tip+"','"+va_codpac+"') as resant  "
        qry = qry + " from resultado r,examen e,analisis a "
        qry = qry + " where r.cdgexamen=e.cdgexamen and e.cdgexamen=a.cdgexamen and r.cdganalisis=a.cdganalisis " 
        qry = qry + " and r.codage='"+codage+"' and r.numorden="+numorden+" and r.seq='" + str(va_seq) + "' " 
        qry = qry + " and r.resultado is not null "

        response_query_ex = sdk.executeQueryPostgresSelect(qry, str(stage))
        dataexamen = {"examen":va_examen,"nomexamen":va_nomexamen,"usuario":va_usuario,"detalle":list(response_query_ex),"bolo":va_bolo_examen,"medfirmad":va_medfirmad,"horfirmad":va_horfirmad,"medfirmad2":va_medfirmad2,"horfirmad2":va_horfirmad2}
        respuesta.append(dataexamen)
    # calcular los valores de referencia
    # calcular el resultado anterior

    va_firmada = orden_firmada(codage,numorden)
    if (va_firmada):
        va_firmado='S'
    else:
        va_firmado='N'

    
    va_imprimir='S'
    va_causal =''
    if (va_tipousuario=='M' and va_codmedico!= va_medic_request):
        va_causal = 'Medico de la orden no coincida con usuario solicitante'
        va_imprimir='N'
    else:
        if (va_tipousuario=='E' and va_codempresa!= va_empresa_request):
            va_causal = 'Usuario solicitante no concuerda con empresa de la orden'
            va_imprimir='N'
        else:
            qry="select imprimir,causal from reglasimp where tipodoc='RES' and tipocli='"+va_tipousuario+"' and pagado='"+ va_pagado+"' and firmado='"+va_firmado+"'"    
            print(qry) 
            response_query_reg = sdk.executeQueryPostgresSelect(qry, str(stage))

            for obj in response_query_reg:
                va_imprimir = obj['imprimir']
                va_causal = obj['causal']
            if (va_imprimir=='SP'):
                va_memb = 'vistaprevia.png'

    return {"statusCode": 200,"resultado": "success","paciente":datapac,"grupo": list(respuesta),"respie":va_respie,"sedeppal":list(response_querysp),"membrete": va_memb,"imprimir":va_imprimir,"causal":va_causal,"firmado":va_firmado,"pagado":va_pagado,"tipousuario":va_tipousuario}


####################### ecabezado del resultado, la forma ##################################

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

    va_empresaorden = ''
    datapac = {}
    for obj in response_querysp:
        va_empresaorden = obj['codemp'] 
        va_fecorden = obj['fecorden']
        va_nompac = obj['nombre']
        va_edadf = obj['edadf']
        va_sexo = obj['sexo']
        va_medfirma = obj['medfirma']
        va_horfirma = obj['horfirma']
        datapac = {'fecorden':va_fecorden,'nompac':va_nompac,'edadf':va_edadf,'sexo':va_sexo,'medfirma':va_medfirma,'horfirma':va_horfirma}
    
    qry = "select d.cdgexamen,e.nombre,d.seq,d.medfirmad, d.horfirmad,d.medfirmad2,d.horfirmad2,e.numfirmas from labordendet d,examen e "
    qry = qry + " where d.codage='"+codage+"' and d.numorden=to_number('"+numorden+"','9999999999999') and d.cdgexamen=e.cdgexamen "
    response_exam = sdk.executeQueryPostgresSelect(qry, str(stage))
    
    va_membrete = 'membrete.png'
    #qry="select imagen from labempresaplus where codemp='"+ va_empresaorden + "'"
    #response_querym = sdk.executeQueryPostgresSelect(qry, str(stage))

    #for obj in response_querym:
    #    va_membrete = obj['imagen'] 

    return {"statusCode": 200,"resultado": "success","paciente":datapac,"examenes": list(response_exam),"membrete":va_membrete }

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

        datares = []
        regres = {}

        # los analisis del examen en esa orden
        qry = "select a.id as idanalisis, d.cdgexamen,d.seq,a.cdganalisis,a.nombre as nomanalisis, "
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
            va_idanalisis = '0_' + str( obj['idanalisis'] ) #id temporal cuando no hay

            regres = {'id':va_idanalisis ,'cdgexamen':va_examen,'cdganalisis':va_anali,'nomanalisis':va_nomanali,'orden':va_orden,
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
            va_id = va_idanalisis #, antes '0' , no existe el resultado aun 
            for res in response_query_an:
                va_id = res['id']  # si el resultado esta seteado, toma un id
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
#@app.get('/ipsconsec/next/{dep}/{doc}')
def ipsconsec(dep:str,doc:str):
    data = {}
    qry = "select  COALESCE( num+1 ,1) as proximo from ipsconsec where docu='"+doc+"' and codage='" + dep +"'" 
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
#@app.get('/precio/find/{codemp}/{dep}/{examen}')
def precioitem(codemp:str,examen:str,dep:str):

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
    if va_abo == None:
        va_abo = 0
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
        qry = "SELECT DISTINCT o.opcion,o.ruta, o.nombre "
        qry = qry+" from opciones o,usuariorole ur, usuarios u, roleopcion r "
        qry = qry+" where u.usuario='"+ usuario +"' "
        qry = qry+" and u.usuario=ur.usuario "
        qry = qry+" and ur.role = r.role  "
        qry = qry+" and r.opcion = o.opcion "
        qry = qry+" and o.carpeta ='"+va_carpeta+"' and o.mostrar='S'" 
        qry = qry+" order by 1 "    
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
	vacios = '' 
	
	if data['nomundnegocio'] =='':data['nomundnegocio'] = None 
	if data['nomundnegocio'] == None:vacios = vacios +' '+ 'nomundnegocio' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update undnegocio set nomundnegocio=%s  where codundnegocio='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/undnegocio/select') 
def conexion_postgres(): 
	query = 'SELECT codundnegocio,nomundnegocio from undnegocio order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/undnegocio/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codundnegocio'] =='':data['codundnegocio'] = None 
	if data['codundnegocio'] == None:vacios = vacios +' '+ 'codundnegocio' 
	if data['nomundnegocio'] =='':data['nomundnegocio'] = None 
	if data['nomundnegocio'] == None:vacios = vacios +' '+ 'nomundnegocio' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into undnegocio(codundnegocio,nomundnegocio) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/undnegocio/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from undnegocio where codundnegocio='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: vinculacion---------- 
# Endpoint Update 
@app.put('/vinculacion/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nomvic'] =='':data['nomvic'] = None 
	if data['nomvic'] == None:vacios = vacios +' '+ 'nomvic' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update vinculacion set nomvic=%s  where vincpac='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/vinculacion/select') 
def conexion_postgres(): 
	query = 'SELECT vincpac,nomvic from vinculacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/vinculacion/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['vincpac'] =='':data['vincpac'] = None 
	if data['vincpac'] == None:vacios = vacios +' '+ 'vincpac' 
	if data['nomvic'] =='':data['nomvic'] = None 
	if data['nomvic'] == None:vacios = vacios +' '+ 'nomvic' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into vinculacion(vincpac,nomvic) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/vinculacion/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from vinculacion where vincpac='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e))         


 # ---------------- tabla: tipomuestra---------- 
# Endpoint Update 
@app.put('/tipomuestra/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update tipomuestra set nombre=%s  where tipmues='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/tipomuestra/select') 
def conexion_postgres(): 
	query = 'SELECT tipmues,nombre from tipomuestra order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/tipomuestra/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['tipmues'] =='':data['tipmues'] = None 
	if data['tipmues'] == None:vacios = vacios +' '+ 'tipmues' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into tipomuestra(tipmues,nombre) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/tipomuestra/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from tipomuestra where tipmues='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: ocupacion---------- 
# Endpoint Update 
@app.put('/ocupacion/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['nomocu'] =='':data['nomocu'] = None 
	if data['nomocu'] == None:vacios = vacios +' '+ 'nomocu' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update ocupacion set nomocu=%s  where codocu='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/ocupacion/select') 
def conexion_postgres(): 
	query = 'SELECT codocu,nomocu from ocupacion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/ocupacion/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codocu'] =='':data['codocu'] = None 
	if data['codocu'] == None:vacios = vacios +' '+ 'codocu' 
	if data['nomocu'] =='':data['nomocu'] = None 
	if data['nomocu'] == None:vacios = vacios +' '+ 'nomocu' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into ocupacion(codocu,nomocu) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/ocupacion/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from ocupacion where codocu='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 





 # ---------------- tabla: labseccion---------- 
# Endpoint Update 
@app.put('/labseccion/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labseccion set nombre=%s,gruposeccion=%s,peso=%s  where codseccion='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labseccion/select') 
def conexion_postgres(): 
	query = 'SELECT codseccion,nombre,gruposeccion,peso from labseccion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labseccion/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codseccion'] =='':data['codseccion'] = None 
	if data['codseccion'] == None:vacios = vacios +' '+ 'codseccion' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labseccion(codseccion,nombre,gruposeccion,peso) values (%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labseccion/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labseccion where codseccion='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


# ---------------- tabla: agencias---------- 
# Endpoint Update 
@app.put('/agencias/update/{id}') 
def update_data(data: dict,id:str):
    vacios = '' 
    if data['nomage'] =='':data['nomage'] = None 
    if data['nomage'] == None:vacios = vacios +' '+ 'nomage'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')   
    try:
        query="update agencias set nomage=%s,ciuage=%s,depage=%s,dirage=%s,telage=%s,tipocons=%s,docpac=%s,resdian=%s,reqfd=%s,sinlogo=%s,predian=%s,maxfecres=%s,maxconsres=%s,tipofirma=%s,architect_prefijo=%s,proc=%s,codager=%s,domi=%s  where codage='"+id+"'"  
        sdk.updatePostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint Select 
@app.get('/agencias/select') 
def conexion_postgres(): 
	query = 'SELECT codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi from agencias order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/agencias/insert') 
def insert_data(data: dict): 
    vacios=''
    if data['nomage'] =='':data['nomage'] = None 
    if data['nomage'] == None:vacios = vacios +' '+ 'nomage'  
    if data['codage'] =='':data['codage'] = None 
    if data['codage'] == None:vacios = vacios +' '+ 'codage'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')   

    try:
        query='insert into agencias(codage,nomage,ciuage,depage,dirage,telage,tipocons,docpac,resdian,reqfd,sinlogo,predian,maxfecres,maxconsres,tipofirma,architect_prefijo,proc,codager,domi) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
        sdk.insertPostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint delete 
@app.delete('/agencias/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from agencias where codage='"+id+"'"  
        response_query = sdk.deletePostgres(query, str(stage))
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: examen---------- 
# Endpoint Update 
@app.put('/examen/update/{id}') 
def update_data(data: dict,id:str):  
    vacios=''
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +' '+ 'nombre'  
    if data['codseccion'] =='':data['codseccion'] = None 
    if data['codseccion'] == None:vacios = vacios +' '+ 'codseccion'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')   
    try:
        query="update examen set nombre=%s,codseccion=%s,cut=%s,soat=%s,nivexa=%s,nomcorto=%s,duracion=%s,tecnicas=%s,condiciones=%s,tipmues=%s,duraciont=%s,tiposerv=%s,inactiva=%s,entlun=%s,entmar=%s,entmie=%s,entjue=%s,entvie=%s,entsab=%s,entdom=%s,noproclun=%s,noprocmar=%s,noprocmie=%s,noprocjue=%s,noprocvie=%s,noprocsab=%s,noprocdom=%s,numfirmas=%s  where cdgexamen='"+id+"'"  
        sdk.updatePostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint Select 
@app.get('/examen/select') 
def conexion_postgres(): 
	query = 'SELECT cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom,numfirmas from examen order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/examen/insert') 
def insert_data(data: dict): 
    vacios=''
    if data['cdgexamen'] =='':data['cdgexamen'] = None 
    if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen'  
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +' '+ 'nombre'  
    if data['codseccion'] =='':data['codseccion'] = None 
    if data['codseccion'] == None:vacios = vacios +' '+ 'codseccion'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')   
    try:
        query='insert into examen(cdgexamen,nombre,codseccion,cut,soat,nivexa,nomcorto,duracion,tecnicas,condiciones,tipmues,duraciont,tiposerv,inactiva,entlun,entmar,entmie,entjue,entvie,entsab,entdom,noproclun,noprocmar,noprocmie,noprocjue,noprocvie,noprocsab,noprocdom,numfirmas) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
        sdk.insertPostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint delete 
@app.delete('/examen/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from examen where cdgexamen='"+id+"'"  
        response_query = sdk.deletePostgres(query, str(stage))
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: mae_unid---------- 
# Endpoint Update 
@app.put('/mae_unid/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['uni_desc'] =='':data['uni_desc'] = None 
	if data['uni_desc'] == None:vacios = vacios +' '+ 'uni_desc' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update mae_unid set uni_desc=%s  where uni_codi='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/mae_unid/select') 
def conexion_postgres(): 
	query = 'SELECT uni_codi,uni_desc from mae_unid order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mae_unid/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['uni_codi'] =='':data['uni_codi'] = None 
	if data['uni_codi'] == None:vacios = vacios +' '+ 'uni_codi' 
	if data['uni_desc'] =='':data['uni_desc'] = None 
	if data['uni_desc'] == None:vacios = vacios +' '+ 'uni_desc' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into mae_unid(uni_codi,uni_desc) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/mae_unid/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from mae_unid where uni_codi='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# ---------------- tabla: analisis---------- 
# Endpoint Update 
@app.put('/analisis/update/{id}') 
def update_data(data: dict,id:str):  
    vacios = '' 
    if data['tipores'] =='':data['tipores'] = None 
    if data['tipores'] == None:vacios = vacios +' '+ 'tipores'  
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +' '+ 'nombre'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:
        query="update analisis set cdgexamen=%s,cdganalisis=%s,nombre=%s,unicodi=%s,tipores=%s,cdganalisisa=%s,tiponorm=%s,aplica=%s,redondear=%s,redondeo=%s,tecnica=%s,grupo=%s,orden=%s  where id='"+id+"'"  
        sdk.updatePostgres(query, data,'prd')
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

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
    vacios = '' 
    if data['tipores'] =='':data['tipores'] = None 
    if data['tipores'] == None:vacios = vacios +' '+ 'tipores'  
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +' '+ 'nombre'  
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 

    try:
        query="insert into analisis(cdgexamen,cdganalisis,nombre,unicodi,tipores,cdganalisisa,tiponorm,aplica,redondear,redondeo,tecnica,grupo,orden) "
        query = query + " values ('"+va_examen+"','"+va_anali+"','"+va_nombre+"','"+va_uni+"','"+va_tipores+"','"+va_cdganalisisa+"','"+va_tiponorm+"','"+va_aplica+"','"+va_redondear+"','"+va_redondeo+"','"+va_tec+"','"+va_grup+"','"+va_orden+"')" 
        sdk.insertPostgres(query, data,'prd')
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 



# Endpoint delete 
@app.delete('/analisis/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from analisis where id='"+id+"'"  
        response_query = sdk.deletePostgres(query, str(stage))     
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: labvalores---------- 
# Endpoint Update 
@app.put('/labvalores/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['cdganalisis'] =='':data['cdganalisis'] = None 
	if data['cdganalisis'] == None:vacios = vacios +' '+ 'cdganalisis' 
	if data['tecla'] =='':data['tecla'] = None 
	if data['tecla'] == None:vacios = vacios +' '+ 'tecla' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labvalores set cdgexamen=%s,cdganalisis=%s,tecla=%s,resultado=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labvalores/select') 
def conexion_postgres(): 
	query = 'SELECT id,cdgexamen,cdganalisis,tecla,resultado from labvalores order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labvalores/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['cdganalisis'] =='':data['cdganalisis'] = None 
	if data['cdganalisis'] == None:vacios = vacios +' '+ 'cdganalisis' 
	if data['tecla'] =='':data['tecla'] = None 
	if data['tecla'] == None:vacios = vacios +' '+ 'tecla' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labvalores(cdgexamen,cdganalisis,tecla,resultado) values (%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labvalores/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labvalores where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
        

 # ---------------- tabla: feriados---------- 
# Endpoint Update 
@app.put('/feriados/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['per'] =='':data['per'] = None 
	if data['per'] == None:vacios = vacios +' '+ 'per' 
	if data['fecha'] =='':data['fecha'] = None 
	if data['fecha'] == None:vacios = vacios +' '+ 'fecha' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update feriados set per=%s,fecha=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/feriados/select') 
def conexion_postgres(): 
	query = 'SELECT id,per,fecha from feriados order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/feriados/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['per'] =='':data['per'] = None 
	if data['per'] == None:vacios = vacios +' '+ 'per' 
	if data['fecha'] =='':data['fecha'] = None 
	if data['fecha'] == None:vacios = vacios +' '+ 'fecha' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into feriados(per,fecha) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/feriados/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from feriados where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: labcombo---------- 
# Endpoint Update 
@app.put('/labcombo/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labcombo set nombre=%s,cdgexamen=%s  where codcombo='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labcombo/select') 
def conexion_postgres(): 
	query = 'SELECT codcombo,nombre,cdgexamen from labcombo order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombo/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codcombo'] =='':data['codcombo'] = None 
	if data['codcombo'] == None:vacios = vacios +' '+ 'codcombo' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labcombo(codcombo,nombre,cdgexamen) values (%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labcombo/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labcombo where codcombo='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
	
 # ---------------- tabla: labcombodet---------- 
# Endpoint Update 
@app.put('/labcombodet/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codcombo'] =='':data['codcombo'] = None 
	if data['codcombo'] == None:vacios = vacios +' '+ 'codcombo' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['valor'] =='':data['valor'] = None 
	if data['valor'] == None:vacios = vacios +' '+ 'valor' 

	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labcombodet set codcombo=%s,cdgexamen=%s,valor=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labcombodet/select') 
def conexion_postgres(): 
	query = 'SELECT x.id,x.codcombo,x.cdgexamen,x.valor, e.nombre from labcombodet x, examen e where x.cdgexamen=e.cdgexamen order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labcombodet/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codcombo'] =='':data['codcombo'] = None 
	if data['codcombo'] == None:vacios = vacios +' '+ 'codcombo' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['valor'] =='':data['valor'] = None 
	if data['valor'] == None:vacios = vacios +' '+ 'valor' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labcombodet(codcombo,cdgexamen,valor) values (%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labcombodet/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labcombodet where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: examenemp---------- 
# Endpoint Update 
@app.put('/examenemp/update/{id}') 
def update_data(data: dict,id:str):
    vacios=''
    if data['codemp'] =='':data['codemp'] = None 
    if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
    if data['cdgexamen'] =='':data['cdgexamen'] = None 
    if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:      
        query="update examenemp set codemp=%s,cdgexamen=%s,descc=%s,nivel=%s  where id='"+id+"'"  
        sdk.updatePostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint Select 
@app.get('/examenemp/select') 
def conexion_postgres(): 
	query = 'SELECT id,codemp,cdgexamen,descc,nivel from examenemp order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/examenemp/insert') 
def insert_data(data: dict): 
    vacios=''
    if data['codemp'] =='':data['codemp'] = None 
    if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
    if data['cdgexamen'] =='':data['cdgexamen'] = None 
    if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 

    try:
        query='insert into examenemp(id,codemp,cdgexamen,descc,nivel) values (%s,%s,%s,%s,%s)' 
        sdk.insertPostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint delete 
@app.delete('/examenemp/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from examenemp where id='"+id+"'"  
        response_query = sdk.deletePostgres(query, str(stage))    
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
	
 # ---------------- tabla: labdepend---------- 
# Endpoint Update 
@app.put('/labdepend/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if data['coddep'] =='':data['coddep'] = None 
	if data['coddep'] == None:vacios = vacios +' '+ 'coddep' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labdepend set codemp=%s,coddep=%s,nombre=%s,desc0=%s,pyp=%s,nofac=%s,domi=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labdepend/select') 
def conexion_postgres(): 
	query = 'SELECT id,codemp,coddep,nombre,desc0,pyp,nofac,domi from labdepend order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labdepend/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if data['coddep'] =='':data['coddep'] = None 
	if data['coddep'] == None:vacios = vacios +' '+ 'coddep' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labdepend(codemp,coddep,nombre,desc0,pyp,nofac,domi) values (%s,%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labdepend/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labdepend where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint lov 
@app.get('/labdepend/selectone/{emp}') 
def conexion_postgres(emp: str): 
	query = "SELECT coddep as id,coddep ||'-'|| nombre as name from labdepend where codemp='"+ emp +"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  

# Endpoint dependence oneonly 
#@app.get('/labdepend/selectoneonly/{emp}/{dep}') 
#def conexion_postgres(emp: str): 
#	query = "SELECT coddep as id,nombre as name from labdepend where codemp='"+ emp +"' and coddep='"+ dep +"' order by 1" 
#	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
#	return {'data': list(response_query)}  


 # ---------------- tabla: labempresa---------- 
# Endpoint Update 
@app.put('/labempresa/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labempresa set nombre=%s,n_ide=%s,dir=%s,tel=%s,ciudad=%s,codcla=%s,codlista=%s,desce=%s,codadm=%s,itemsfac=%s,codcob=%s,contacto=%s,fax=%s,coddep=%s,ciclofac=%s,repbono=%s,repcumo=%s,repcopa=%s,repdesc=%s,repmode=%s,inactiva=%s,informacion=%s,nithelisa=%s,codlista2=%s,requisitos=%s,ccosto=%s,codempt=%s,prefijorip=%s,digitosfac=%s,tipcon=%s  where codemp='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labempresa/select') 
def conexion_postgres(): 
	query = 'SELECT codemp,nombre,n_ide,dir,tel,ciudad,codcla,codlista,desce,codadm,itemsfac,codcob,contacto,fax,coddep,ciclofac,repbono,repcumo,repcopa,repdesc,repmode,inactiva,informacion,nithelisa,codlista2,requisitos,ccosto,codempt,prefijorip,digitosfac,tipcon from labempresa order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labempresa/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labempresa(codemp,nombre,n_ide,dir,tel,ciudad,codcla,codlista,desce,codadm,itemsfac,codcob,contacto,fax,coddep,ciclofac,repbono,repcumo,repcopa,repdesc,repmode,inactiva,informacion,nithelisa,codlista2,requisitos,ccosto,codempt,prefijorip,digitosfac,tipcon) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labempresa/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labempresa where codemp='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
        
 # ---------------- tabla: medicos---------- 
# Endpoint Update 
@app.put('/medicos/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codmedico'] =='':data['codmedico'] = None 
	if data['codmedico'] == None:vacios = vacios +' '+ 'codmedico' 
	if data['nommedico'] =='':data['nommedico'] = None 
	if data['nommedico'] == None:vacios = vacios +' '+ 'nommedico' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update medicos set nommedico=%s,ccmedico=%s,espmedico=%s,perfil=%s,celular=%s,tel=%s,ciudad=%s,codundnegocio=%s,usuario=%s,firma=%s,presentacion=%s  where codmedico='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/medicos/select') 
def conexion_postgres(): 
	query = 'SELECT codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion from medicos order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/medicos/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codmedico'] =='':data['codmedico'] = None 
	if data['codmedico'] == None:vacios = vacios +' '+ 'codmedico' 
	if data['nommedico'] =='':data['nommedico'] = None 
	if data['nommedico'] == None:vacios = vacios +' '+ 'nommedico' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into medicos(codmedico,nommedico,ccmedico,espmedico,perfil,celular,tel,ciudad,codundnegocio,usuario,firma,presentacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/medicos/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from medicos where codmedico='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: usuarios---------- 
# Endpoint Update 
@app.put('/usuarios/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if data['tipo'] =='':data['tipo'] = None 
	if data['tipo'] == None:vacios = vacios +' '+ 'tipo' 
	if data['estado'] =='':data['estado'] = None 
	if data['estado'] == None:vacios = vacios +' '+ 'estado' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update usuarios set nombre=%s,tipo=%s,codemp=%s,estado=%s  where usuario='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/usuarios/select') 
def conexion_postgres(): 
	query = 'SELECT usuario,nombre,tipo,codemp,estado from usuarios order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/usuarios/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['usuario'] =='':data['usuario'] = None 
	if data['usuario'] == None:vacios = vacios +' '+ 'usuario' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if data['tipo'] =='':data['tipo'] = None 
	if data['tipo'] == None:vacios = vacios +' '+ 'tipo' 
	if data['estado'] =='':data['estado'] = None 
	if data['estado'] == None:vacios = vacios +' '+ 'estado' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into usuarios(usuario,nombre,tipo,codemp,estado) values (%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/usuarios/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from usuarios where usuario='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: ipsconsec---------- 
# Endpoint Update 
@app.put('/ipsconsec/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['docu'] =='':data['docu'] = None 
	if data['docu'] == None:vacios = vacios +' '+ 'docu' 
	if data['codage'] =='':data['codage'] = None 
	if data['codage'] == None:vacios = vacios +' '+ 'codage' 
	if data['num'] =='':data['num'] = None 
	if data['num'] == None:vacios = vacios +' '+ 'num' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update ipsconsec set docu=%s,codage=%s,num=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/ipsconsec/select') 
def conexion_postgres(): 
	query = 'SELECT id,docu,codage,num from ipsconsec order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/ipsconsec/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['docu'] =='':data['docu'] = None 
	if data['docu'] == None:vacios = vacios +' '+ 'docu' 
	if data['codage'] =='':data['codage'] = None 
	if data['codage'] == None:vacios = vacios +' '+ 'codage' 
	if data['num'] =='':data['num'] = None 
	if data['num'] == None:vacios = vacios +' '+ 'num' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into ipsconsec(docu,codage,num) values (%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/ipsconsec/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from ipsconsec where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
	
 # ---------------- tabla: mediospago---------- 
# Endpoint Update 
@app.put('/mediospago/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 

	if data['desmed'] =='':data['desmed'] = None 
	if data['desmed'] == None:vacios = vacios +' '+ 'desmed' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update mediospago set desmed=%s  where codmed='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/mediospago/select') 
def conexion_postgres(): 
	query = 'SELECT codmed,desmed from mediospago order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/mediospago/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codmed'] =='':data['codmed'] = None 
	if data['codmed'] == None:vacios = vacios +' '+ 'codmed' 
	if data['desmed'] =='':data['desmed'] = None 
	if data['desmed'] == None:vacios = vacios +' '+ 'desmed' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into mediospago(codmed,desmed) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/mediospago/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from mediospago where codmed='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: labordenpago---------- 

def actualiza_pago(id:str):
    data = {}
    qry = "select codage,numorden from laborden where id="+str(id)+""
    response_query = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_age = ''
    va_ord = ''

    print("1")
    for obj in response_query:
        va_age = obj['codage']
        va_ord = obj['numorden']

    print("2")
    va_abo = 0
    #--------- los pagos de la orden ----------------------------------
    #to_number('"+va_ord+"','9999999999999999')
    qry = "select sum(valor) as abonos "
    qry = qry + " from labordenpago d where d.codage='"+va_age+"' and d.numorden= "+ str(va_ord)
    response_queryab = sdk.executeQueryPostgresSelect(qry, str(stage))
    print("3")
    for obja in response_queryab:
        va_abo = obja['abonos']  
    qry = "update laborden set abopac="+str(va_abo)+" where id='"+str(id)+"'"
    sdk.updatePostgres(qry, data,'prd')
    print("4")
    return ("ok")

# Endpoint Update 
@app.put('/labordenpago/update/{id}') 
def update_data(data: dict,id:str):  
    vacios = '' 
    if data['codage'] =='':data['codage'] = None 
    if data['codage'] == None:vacios = vacios +' '+ 'codage' 
    if data['numorden'] =='':data['numorden'] = None 
    if data['numorden'] == None:vacios = vacios +' '+ 'numorden' 
    if data['codmed'] =='':data['codmed'] = None 
    if data['codmed'] == None:vacios = vacios +' '+ 'codmed' 
    if data['valor'] =='':data['valor'] = None 
    if data['valor'] == None:vacios = vacios +' '+ 'valor' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:
        query="update labordenpago set fecha=CURRENT_TIMESTAMP,codage=%s,numorden=%s,codmed=%s,valor=%s,pend=%s  where id="+str(id)+""  
        sdk.updatePostgres(query, data,'prd')
        x = actualiza_pago(id) 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labordenpago/select/{miage}/{miord}') 
def conexion_postgres(miage:str,miord=str): 
	query = "SELECT x.id,x.codage,x.numorden,x.codmed,x.valor,x.pend,x.fecha,x.usucre from labordenpago x where  x.codage='"+miage+"' and x.numorden='"+ miord+ "' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labordenpago/insert') 
def insert_data(data: dict): 
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +' '+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +' '+ 'numorden' 
    if data['datos']['codmed'] =='':data['datos']['codmed'] = None 
    if data['datos']['codmed'] == None:vacios = vacios +' '+ 'codmed' 
    if data['datos']['valor'] =='':data['datos']['valor'] = None 
    if data['datos']['valor'] == None:vacios = vacios +' '+ 'valor' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    user = data['control']['usuario']

    qry = "select id from laborden where codage='" + data['datos']['codage'] + "' and numorden=" + str(data['datos']['numorden']);
    response_queryab = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_queryab:
        va_id = obja['id'] 


    try:
        query="insert into labordenpago(codage,numorden,codmed,valor,pend,fecha,usucre) values ('"+ data['datos']['codage'] + "'," + str(data['datos']['numorden']) +",'"+ data['datos']['codmed'] + "'," + str(data['datos']['valor']) + ",'" + data['datos']['pend'] + "',CURRENT_TIMESTAMP,'" + user + "')" 
        #query = query.replace("''", "null")
        #query = query.replace(",,", "null")
        sdk.insertPostgres(query, data['datos'],'prd')
        x = actualiza_pago(va_id) 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e))



# Endpoint delete 
@app.delete('/labordenpago/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from labordenpago where id="+id+"" 
        print(query) 
        response_query = sdk.deletePostgres(query, str(stage))
        x = actualiza_pago(id)         
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


        
 # ---------------- tabla: opciones---------- 
# Endpoint Update 
@app.put('/opciones/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if data['ruta'] =='':data['ruta'] = None 
	if data['ruta'] == None:vacios = vacios +' '+ 'ruta' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update opciones set nombre=%s,ruta=%s,mostrar=%s,orden=%s,carpeta=%s  where opcion='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/opciones/select') 
def conexion_postgres(): 
	query = 'SELECT opcion,nombre,ruta,mostrar,orden,carpeta from opciones order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/opciones/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['opcion'] =='':data['opcion'] = None 
	if data['opcion'] == None:vacios = vacios +' '+ 'opcion' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if data['ruta'] =='':data['ruta'] = None 
	if data['ruta'] == None:vacios = vacios +' '+ 'ruta' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into opciones(opcion,nombre,ruta,mostrar,orden,carpeta) values (%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/opciones/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from opciones where opcion='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: roles---------- 
# Endpoint Update 
@app.put('/roles/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update roles set nombre=%s  where role='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/roles/select') 
def conexion_postgres(): 
	query = 'SELECT role,nombre from roles order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/roles/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['role'] =='':data['role'] = None 
	if data['role'] == None:vacios = vacios +' '+ 'role' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into roles(role,nombre) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/roles/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from roles where role='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: roleopcion---------- 
# Endpoint Update 
@app.put('/roleopcion/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['role'] =='':data['role'] = None 
	if data['role'] == None:vacios = vacios +' '+ 'role' 
	if data['opcion'] =='':data['opcion'] = None 
	if data['opcion'] == None:vacios = vacios +' '+ 'opcion' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update roleopcion set role=%s,opcion=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/roleopcion/select') 
def conexion_postgres(): 
	query = 'SELECT id,role,opcion from roleopcion order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/roleopcion/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['role'] =='':data['role'] = None 
	if data['role'] == None:vacios = vacios +' '+ 'role' 
	if data['opcion'] =='':data['opcion'] = None 
	if data['opcion'] == None:vacios = vacios +' '+ 'opcion' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into roleopcion(role,opcion) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/roleopcion/delete/{id}') 
def delete_data(id: str): 
    try:
        query="delete from roleopcion where id='"+id+"'"  
        print( query)
        response_query = sdk.deletePostgres(query, str(stage)) 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: usuariorole---------- 
# Endpoint Update 
@app.put('/usuariorole/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['usuario'] =='':data['usuario'] = None 
	if data['usuario'] == None:vacios = vacios +' '+ 'usuario' 
	if data['role'] =='':data['role'] = None 
	if data['role'] == None:vacios = vacios +' '+ 'role' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update usuariorole set usuario=%s,role=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/usuariorole/select') 
def conexion_postgres(): 
	query = 'SELECT id,usuario,role from usuariorole order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/usuariorole/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['usuario'] =='':data['usuario'] = None 
	if data['usuario'] == None:vacios = vacios +' '+ 'usuario' 
	if data['role'] =='':data['role'] = None 
	if data['role'] == None:vacios = vacios +' '+ 'role' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into usuariorole(usuario,role) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/usuariorole/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from usuariorole where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
 # ---------------- tabla: labempresaplus---------- 
# Endpoint Update 
@app.put('/labempresaplus/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if data['imagen'] =='':data['imagen'] = None 
	if data['imagen'] == None:vacios = vacios +' '+ 'imagen' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labempresaplus set codemp=%s,imagen=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labempresaplus/select') 
def conexion_postgres(): 
	query = 'SELECT id,codemp,imagen from labempresaplus order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labempresaplus/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if data['imagen'] =='':data['imagen'] = None 
	if data['imagen'] == None:vacios = vacios +' '+ 'imagen' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labempresaplus(codemp,imagen) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labempresaplus/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labempresaplus where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

 # ---------------- tabla: labtarifas---------- 
# Endpoint Update 
@app.put('/labtarifas/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codlista'] =='':data['codlista'] = None 
	if data['codlista'] == None:vacios = vacios +' '+ 'codlista' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['valor'] =='':data['valor'] = None 
	if data['valor'] == None:vacios = vacios +' '+ 'valor' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labtarifas set codlista=%s,cdgexamen=%s,cup=%s,valor=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint insert 
@app.post('/labtarifas/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codlista'] =='':data['codlista'] = None 
	if data['codlista'] == None:vacios = vacios +' '+ 'codlista' 
	if data['cdgexamen'] =='':data['cdgexamen'] = None 
	if data['cdgexamen'] == None:vacios = vacios +' '+ 'cdgexamen' 
	if data['valor'] =='':data['valor'] = None 
	if data['valor'] == None:vacios = vacios +' '+ 'valor' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labtarifas(codlista,cdgexamen,cup,valor) values (%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labtarifas/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labtarifas where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
        
# Endpoint Select 
@app.get('/labtarifas/select') 
def conexion_postgres(): 
	query = 'SELECT x.id,x.codlista,x.cdgexamen,e.nombre,x.cup,x.valor from labtarifas x,examen e where x.cdgexamen=e.cdgexamen order by e.nombre' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint delete all prices in a price list
@app.delete('/labtarifas/deleteall/{id}')   # id es la lista
def delete_data(id: str): 
	query="delete from labtarifas where codlista='"+id+"'"  
	response_query = sdk.deletePostgres(query, str(stage))
# Endpoint Update multiply list by a factor
@app.put('/labtarifas/updateall/{id}')     #id es la lista 
def update_data(data: dict,id:str):
    factor = str(data['factor'])  
    listabase = data['listabase']
    query="insert into labtarifas (codlista,cdgexamen,cup,valor) select "+id+",cdgexamen,cup,valor*"+ factor +" from labtarifas where  codlista='"+ listabase +"'"  
    sdk.insertPostgres(query, data,'prd') 

@app.put('/labtarifas/simulateall')     #id es la lista 
def update_data(data: dict):
    factor = str(data['factor'])  
    listabase = data['listabase']
    query = "SELECT x.id,x.codlista,x.cdgexamen,e.nombre,x.cup,x.valor*"+ factor +" as valor from labtarifas x,examen e where x.cdgexamen=e.cdgexamen and x.codlista = '"+ listabase +"' order by e.nombre" 
    response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
    return {'data': list(response_query)}  



 # ---------------- tabla: laborden---------- 
# Endpoint Update 
@app.put('/laborden/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['codage'] =='':data['codage'] = None 
	if data['codage'] == None:vacios = vacios +','+ 'codage' 
	if data['numorden'] =='':data['numorden'] = None 
	if data['numorden'] == None:vacios = vacios +','+ 'numorden' 
	if data['codpac'] =='':data['codpac'] = None 
	if data['codpac'] == None:vacios = vacios +','+ 'codpac' 
	if data['tipide'] =='':data['tipide'] = None 
	if data['tipide'] == None:vacios = vacios +','+ 'tipide' 
	if data['totemp'] =='':data['totemp'] = None 
	if data['totemp'] == None:vacios = vacios +','+ 'totemp' 
	if data['totpac'] =='':data['totpac'] = None 
	if data['totpac'] == None:vacios = vacios +','+ 'totpac' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update laborden set fecorden=%s,estado=%s,codage=%s,numorden=%s,agefaccli=%s,numfaccli=%s,tipide=%s,codpac=%s,codemp=%s,contpac=%s,interlab=%s,prio=%s,codmedico=%s,nivpac=%s,copago=%s,cuotam=%s,bono=%s,descpac=%s,abopac=%s,coddiagnostico=%s,totemp=%s,totpac=%s,usuario=%s,dur=%s,descpacp=%s,factura=%s,edadf=%s,facturar=%s,pendaprob=%s,embar=%s,fechasol=%s,usuvbo=%s,horvbo=%s,idbono=%s,mipres=%s,poliza=%s,contrato=%s,fecent=%s,horent=%s,web=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/laborden/selectoneonly/{age}/{ord}') 
def conexion_postgres(age: str,ord:str): 
	query = "SELECT id,fecorden,estado,codage,numorden,agefaccli,numfaccli,tipide,codpac,codemp,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,totemp,totpac,usuario,dur,descpacp,factura,edadf,facturar,pendaprob,embar,fechasol,usuvbo,horvbo,idbono,mipres,poliza,contrato,fecent,horent,web from laborden where codage='"+ age +"' and numorden='"+ str(ord) +"'  order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  

# Endpoint Select 
@app.get('/laborden/selectoneonlyl/{miordenlarga}') 
def conexion_postgres(miordenlarga:str): 
	query = "SELECT id,fecorden,estado,codage,numorden,agefaccli,numfaccli,tipide,codpac,codemp,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,totemp,totpac,usuario,dur,descpacp,factura,edadf,facturar,pendaprob,embar,fechasol,usuvbo,horvbo,idbono,mipres,poliza,contrato,fecent,horent,web from laborden where ordenl='"+ miordenlarga +"'" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  



# Endpoint insert 
@app.post('/laborden/insert') 
def insert_data(data: dict): 
    vacios = '' 
    if data['codage'] =='':data['codage'] = None 
    if data['codage'] == None:vacios = vacios +','+ 'codage' 
   
    #if data['numorden'] == None:vacios = vacios +','+ 'numorden' 
    if data['codpac'] =='':data['codpac'] = None 
    if data['codpac'] == None:vacios = vacios +','+ 'codpac' 
    if data['tipide'] =='':data['tipide'] = None 
    if data['tipide'] == None:vacios = vacios +','+ 'tipide' 
    if data['totemp'] =='':data['totemp'] = None 
    if data['totemp'] == None:vacios = vacios +','+ 'totemp' 
    if data['totpac'] =='':data['totpac'] = None 
    if data['totpac'] == None:vacios = vacios +','+ 'totpac' 
    if data['codemp'] =='':data['codemp'] = None 
    if data['codemp'] == None:vacios = vacios +','+ 'codemp' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    resp = ipsconsec(data['codage'] ,'ORDEN' )  #obtenemos el siguiente consecutivo 
    data['numorden'] = resp['consecutivo'] 

    query = "select to_char(fecnac,'ddmmyyyy') as fecnac from paciente where tipide='"+ data['tipide'] +"' and codpac='"+ data['codpac'] +"'" 
    response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
    for reg in response_query:
        fechanaci = reg['fecnac']

    try:
        query="insert into laborden(fecorden,estado,codage,numorden,agefaccli,numfaccli,tipide,codpac,codemp,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,totemp,totpac,usuario,dur,descpacp,factura,facturar,pendaprob,embar,fechasol,usuvbo,horvbo,idbono,mipres,poliza,contrato,fecent,horent,web,edadf) values (CURRENT_TIMESTAMP,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,edadf('"+ fechanaci +"') )" 
        sdk.insertPostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success', 'consecutivo' :resp['consecutivo'] } 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 



# Endpoint delete 
@app.delete('/laborden/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from laborden where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


# Endpoint Select 
@app.get('/laborden/selectone/{ide}/{pac}') 
def conexion_postgres(ide:str,pac:str): 
	query = "SELECT id,fecorden,estado,codage,numorden,agefaccli,numfaccli,tipide,codpac,codemp,contpac,interlab,prio,codmedico,nivpac,copago,cuotam,bono,descpac,abopac,coddiagnostico,totemp,totpac,usuario,dur,descpacp,factura,edadf,facturar,pendaprob,embar,fechasol,usuvbo,horvbo,idbono,mipres,poliza,contrato,fecent,horent,web from laborden where tipide='"+ ide +"' and codpac='"+ pac +"' order by id desc" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  


 # ---------------- tabla: labordendet---------- 
# Endpoint Update 
@app.put('/labordendet/update/{id}') 
def update_data(data: dict,id:str):  
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    if data['datos']['cdgexamen'] =='':data['datos']['cdgexamen'] = None 
    if data['datos']['cdgexamen'] == None:vacios = vacios +','+ 'cdgexamen' 
    if data['datos']['valor'] =='':data['datos']['valor'] = None 
    if data['datos']['valor'] == None:vacios = vacios +','+ 'valor'
    if data['datos']['fechapend'] ==None:data['datos']['fechapend'] = '' # para solucionar lo de fecha
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    # revisar totales ******************************************************
    #obj = precioitem(data['control']['empresa'], data['datos']['cdgexamen'], data['datos']['coddep'])
    print('1')
    valor_real=0
    descu_real=0
    descu_2 =0
    recargo =0
    valor_real = float(data['datos']['valor'])
    descu_real = float(data['datos']['desc1'])
    descu_2 = float(data['datos']['desc2'])
    recargo = float(data['datos']['desc3'])
    valor_neto = valor_real * (1-descu_real/100) * (1-descu_2/100) * (1 + recargo/100)
    valor_real = valor_neto

    print('valor neto ')
    print(str(valor_neto))

    subtemp = '0'
    subtpac = '0'
    print('2')
    if (data['control']['empresa'] =='00'): # si empresa es 00 entonces examen es particular
        data['datos']['partic'] ='S'      
    if (data['datos']['partic'] == 'N'):
        subtemp = valor_real
        subtpac = 0
    else:
        subtpac = valor_real
        subtemp = 0
    if (data['datos']['corte'] == 'S'):
        subtpac = 0
        subtemp = 0  
    print(' va a ejecutar update , subtpac ' + str(subtpac) + ' subtemp ' + str(subtemp)   )
    print( data['datos']['fechapend'] )
    try:
        query="update Labordendet set cdgexamen='"+ data['datos']['cdgexamen'] +"',valor="+str(data['datos']['valor'])+",desc1="+str(data['datos']['desc1'])+",desc2="+str(data['datos']['desc2'])+",desc3="+str(data['datos']['desc3'])+",partic='"+data['datos']['partic']+"',corte='"+data['datos']['corte']+"',pend='"+data['datos']['pend']+"',codcombo='"+data['datos']['codcombo']+"',subtemp="+str(subtemp)+",subtpac="+str(subtpac)+",cuotam="+str(data['datos']['cuotam'])+",remi='"+ data['datos']['remi'] +"',ordenam='"+data['datos']['ordenam']+"',coddep='"+data['datos']['coddep']+"',fechapend='"+ data['datos']['fechapend']+"' where id='"+str(id)+"'"  
        query = query.replace("''", "null")
        query = query.replace(",,", "null")
        print(' query para el update labordendet ')
        sdk.updatePostgres(query, data['datos'],'prd') 
        ordenlarga = data['datos']['codage']+'-'+str(data['datos']['numorden'])
        print(' ordenlarga ' + ordenlarga)
        resp = recalcula(ordenlarga) 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labordendet/selectone/{age}/{orden}') 
def conexion_postgres(age:str, orden:str): 
    query = "SELECT x.id,x.codage,x.numorden,x.cdgexamen,y.nombre,x.valor,x.desc1,x.desc2,x.desc3,x.partic,x.corte,x.pend,x.codcombo,x.subtemp,x.subtpac,x.seq,x.cuotam,x.fechapend,x.remi,x.ordenam,x.coddep,y.condiciones,y.duracion,y.cut from labordendet x,examen y where x.cdgexamen=y.cdgexamen and x.codage='"+ age +"' and x.numorden="+ orden +" order by seq desc" 
    print(query)
    response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
    return {'data': list(response_query)}  

# Endpoint insert 
@app.post('/labordendet/insert') 
def insert_data(data: dict): 
    empresa = data['control']['empresa']
    usuario = data['control']['usuario']
    #data = datos[0]
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    va_age = data['datos']['codage']
    va_ord = data['datos']['numorden']   
    if data['datos']['cdgexamen'] =='':data['datos']['cdgexamen'] = None 
    if data['datos']['cdgexamen'] == None:vacios = vacios +','+ 'cdgexamen' 
    #if data['datos']['valor'] =='':data['datos']['valor'] = None 
    #if data['datos']['valor'] == None:vacios = vacios +','+ 'valor' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')
    ordenlarga = data['datos']['codage']+'-'+ str(data['datos']['numorden'])
    # busco el valor del examen y su descuento --------------------------------------------------------
    print('0')
    obj = precioitem(empresa, data['datos']['cdgexamen'], '00')
    #print('1')
    valor_real = obj['valor']
    descu_real = obj['descuento']
    subtemp = '0'
    subtpac = '0'
    #print('2')
    if (empresa =='00'): # si empresa es 00 entonces examen es particular
        data['datos']['partic'] = 'S'      
    if (data['datos']['partic'] == 'N'):
        subtemp = valor_real * (1-obj['descuento']/100)
        subtpac = 0
    else:
        subtpac = valor_real * (1-obj['descuento']/100)
        subtemp = 0
        if (data['datos']['corte'] == 'S'):
            subtpac = 0
            subtemp = 0
    #print('3')
    # ----------------------------------------------------------------------------------------------------        
    qry = "select  COALESCE(max(seq),0)+1 as maxseq from labordendet where codage='"+ va_age +"' and numorden="+ str(va_ord)  
    response_queryseq = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_proximo = 0 # para calcular la proxima secuencia
    #print('4')
    for objt in response_queryseq:
        if (objt['maxseq']==''):
            va_proximo = '0'
        else:
            va_proximo = str(objt['maxseq'])
    data['datos']['seq'] = va_proximo
    #print('5')
    print(data['datos'])
    if data['datos']['cuotam'] == None:data['datos']['cuotam']=0
    if data['datos']['desc1'] == None:data['datos']['desc1']=0
    if data['datos']['desc2'] == None:data['datos']['desc2']=0
    if data['datos']['desc3'] == None:data['datos']['desc3']=0
      
    try:
        query="insert into labordendet(codage,numorden,cdgexamen,valor,desc1,desc2,desc3,partic,corte,pend,codcombo,subtemp,subtpac,seq,cuotam,fechapend,remi,ordenam,coddep) values ('"+data['datos']['codage']+"',"+str(data['datos']['numorden'])+",'"+data['datos']['cdgexamen']+"',"+ str(valor_real) + ","+ str(descu_real) + ","+str(data['datos']['desc2'])+","+str(data['datos']['desc3'])+",'"+data['datos']['partic']+"','"+data['datos']['corte']+"','"+data['datos']['pend']+"','"+data['datos']['codcombo']+"',"+str(subtemp)+","+str(subtpac)+","+ str(va_proximo) + ","+ str(   data['datos']['cuotam']  ) + ",null,'"+data['datos']['remi'] + "','" + data['datos']['ordenam'] + "','00')" 
        query = query.replace("''", "null")
        print(query)
        #query="insert into labordendet(codage,numorden,cdgexamen,valor,desc1,desc2,desc3,partic,corte,pend,codcombo,subtemp,subtpac,seq,cuotam,fechapend,remi,ordenam,coddep) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','00')".format(data['codage'],data['numorden'],data['cdgexamen'],data['valor'],data['desc1'],data['desc2'],data['desc3'],data['partic'],data['corte'],data['pend'],data['codcombo'],data['subtemp'],data['subtpac'],data['seq'],data['cuotam'],data['fechapend'],data['remi'],data['ordenam)']
        # "'{0}' is longer than '{1}'".format(name1, name2)
        sdk.insertPostgres(query, data['datos'],'prd') 
        print(' orden larga ' + ordenlarga)
        resp = recalcula(ordenlarga) 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


# Endpoint insert combo
@app.post('/labordendet/insertcombo') 
def insert_data(data: dict): 
    print('entra al servicio de insertar combo')
    #empresa = data['control']['empresa']
    usuario = data['control']['usuario']
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    va_age = data['datos']['codage']
    va_ord = data['datos']['numorden']   
    if data['datos']['codcombo'] =='':data['datos']['cdgexamen'] = None 
    if data['datos']['codcombo'] == None:vacios = vacios +','+ 'codcombo' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')
    ordenlarga = data['datos']['codage']+'-'+ str(data['datos']['numorden'])

    print(' agencia ' + data['datos']['codage'])
    print(' agencia ' + str(data['datos']['numorden']))
    print(' codcombo ' + data['datos']['codcombo'])
    print(' usuario ' + data['control']['usuario'])
    
    # busco el valor del examen y su descuento --------------------------------------------------------
    print('0')
    print('1')
    qry = "select cdgexamen,valor from labcombodet where codcombo='"+ data['datos']['codcombo'] +"'"  
    response_querycomb = sdk.executeQueryPostgresSelect(qry, str(stage))
    va_proximo = 0 # para calcular la proxima secuencia
    #print('4')
    for objc in response_querycomb:
        valor_real = objc['valor']
        examen = objc['cdgexamen']
        print('2')
        subtpac = valor_real 
        subtemp = 0
        # ----------------------------------------------------------------------------------------------------        
        qry = "select COALESCE(max(seq)+1,1) as maxseq from labordendet where codage='"+ va_age +"' and numorden="+ str(va_ord)  
        response_queryseq = sdk.executeQueryPostgresSelect(qry, str(stage))
        va_proximo = 0 # para calcular la proxima secuencia
        print('4')
        for objt in response_queryseq:
            if (objt['maxseq']==''):
                va_proximo = '0'
            else:
                va_proximo = str(objt['maxseq'])
        print(data['datos'])
        try:
            print('4.5')
            query="insert into labordendet(codage,numorden,cdgexamen,valor,desc1,desc2,desc3,partic,corte,pend,codcombo,subtemp,subtpac,seq,cuotam,fechapend,remi,ordenam,coddep) "
            query = query +" values ('"+data['datos']['codage']+"',"+str(data['datos']['numorden'])+",'"+ examen +"',"+ str(valor_real) + ",0,0,0,'S','N','N','"+data['datos']['codcombo']+"',"+str(subtemp)+","+str(subtpac)+","+ str(va_proximo) + ",0,null,'N',NULL,'00')" 
            query = query.replace("''", "null")
            query = query.replace(",,", ",null,")
            print('5')
            print(query)
            sdk.insertPostgres(query, data['datos'],'prd') 
            print(' orden larga ' + ordenlarga)
        except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
    
    resp = recalcula(ordenlarga) 
    return {'statusCode': 200,'resultado': 'success'} 

# Endpoint remover combo
@app.post('/labordendet/quitarcombo') 
def insert_data(data: dict): 
    #empresa = data['control']['empresa']
    usuario = data['control']['usuario']
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    va_age = data['datos']['codage']
    va_ord = data['datos']['numorden']   
    if data['datos']['codcombo'] =='':data['datos']['cdgexamen'] = None 
    if data['datos']['codcombo'] == None:vacios = vacios +','+ 'codcombo' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')
    ordenlarga = data['datos']['codage']+'-'+ str(data['datos']['numorden'])

    print(' agencia ' + data['datos']['codage'])
    print(' agencia ' + str(data['datos']['numorden']))
    print(' codcombo ' + data['datos']['codcombo'])
    print(' usuario ' + data['control']['usuario'])
    
    try:
        qry = "delete from labordendet where  codage='"+ data['datos']['codage'] +"' and numorden="+ str(data['datos']['numorden']) +" and codcombo='"+ data['datos']['codcombo'] +"'"  
        response_query = sdk.deletePostgres(qry, str(stage)) 

    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
    resp = recalcula(ordenlarga) 
    return {'statusCode': 200,'resultado': 'success'} 



# Endpoint modificar dependencia a toda la orden
@app.post('/labordendet/cambiardepend') 
def cambiardep(data: dict): 
    print('entra al servicio de cambiar la dep')
    #empresa = data['control']['empresa']
    usuario = data['control']['usuario']
    vacios = '' 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    va_age = data['datos']['codage']
    va_ord = data['datos']['numorden']   
    if data['datos']['coddep'] =='':data['datos']['coddep'] = None 
    if data['datos']['coddep'] == None:vacios = vacios +','+ 'coddep' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')
    
    ordenlarga = data['datos']['codage']+'-'+ str(data['datos']['numorden'])

    print(' agencia ' + data['datos']['codage'])
    print(' agencia ' + str(data['datos']['numorden']))
    print(' coddep ' + data['datos']['coddep'])
    print(' usuario ' + data['control']['usuario'])
    
    # busco el valor del examen y su descuento --------------------------------------------------------
    print('0')
    try:
        qry = "update labordendet set coddep='" + data['datos']['coddep'] + "'  where ordenl='"+ ordenlarga +"'"  
        sdk.updatePostgres(qry, {},'prd') 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
    
    #resp1 = liquida
    resp = recalcula(ordenlarga) 
    return {'statusCode': 200,'resultado': 'success'} 



# Endpoint delete 
@app.delete('/labordendet/delete/{id}') 
def delete_data(data:dict, id: str):
    ordenlarga = data['datos']['age'] + '-' + str(data['datos']['ord']) 
    combo = data['datos']['codcombo']
    usuario = data['control']['usuario']
    print('**********')
    print(combo)

    try:
        if (combo != None and combo != ''):
            query="delete from labordendet where ordenl='"+ ordenlarga + "' and codcombo='" + combo + "'" ; 
            response_query = sdk.deletePostgres(query, str(stage)); 
        else:
            query="delete from labordendet where id='"+id+"'"  
            response_query = sdk.deletePostgres(query, str(stage));    
        
        
        resp = recalcula(ordenlarga)     
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


# Endpoint insert 
@app.post('/laborden/liquida') # este endpoint reliquida toda la orden cuando se modifica empresa o dependencia 
def liquida_data(data: dict): 
    print('0')
    usuario = data['control']['usuario']
    #data = datos[0]
    vacios = ''
    print('1') 
    if data['datos']['codage'] =='':data['datos']['codage'] = None 
    if data['datos']['codage'] == None:vacios = vacios +','+ 'codage' 
    if data['datos']['numorden'] =='':data['datos']['numorden'] = None 
    if data['datos']['numorden'] == None:vacios = vacios +','+ 'numorden' 
    va_age = data['datos']['codage']
    va_ord = data['datos']['numorden']   
    print('2')
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado')
    ordenlarga = data['datos']['codage']+'-'+ str(data['datos']['numorden'])
    # busco el valor del examen y su descuento --------------------------------------------------------
    valor=0
    print('3')
    qry = "select codemp from laborden where ordenl='"+ ordenlarga +"'"
    response_querydenc = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obje in response_querydenc:
        empresa = obje['codemp']
    print('4')
    qry = "select id,seq,cdgexamen,valor,desc1,desc2,desc3,cuotam,coddep,corte,partic from labordendet where codage='"+ va_age +"' and numorden="+ str(va_ord)
    response_querydet = sdk.executeQueryPostgresSelect(qry, str(stage))
    for objd in response_querydet:
        print('5')
        examen = objd['cdgexamen']
        idd = objd['id']
        d1d = objd['desc1']
        d2d = objd['desc2']
        d3d = objd['desc3']
        cuotamd = objd['cuotam']
        depd = objd['coddep']
        obj = precioitem(empresa, examen , depd )
        valor_real = obj['valor']
        descu_real = obj['descuento']
        corted = objd['corte']
        particd = objd['partic']
        subtemp = 0
        subtpac = 0
        #print('2')
        print('6')
        if (empresa =='00'): # si empresa es 00 entonces examen es particular
            particd = 'S'     
        else:
            particd = 'N'           
        if (particd == 'N'):
            subtemp = valor_real * (1-obj['descuento']/100) * (1-d2d/100) * (1 + d3d/100) 
            subtpac = 0
        else:
            print('7')
            subtpac = valor_real * (1-obj['descuento']/100) * (1-d2d/100) * (1 + d3d/100)
            subtemp = 0
        if (corted == 'S'):
            subtpac = 0
            subtemp = 0
        try:
            print('8')
            query="update Labordendet set valor="+str(valor_real)+",subtemp=" +str(subtemp)+",subtpac="+str(subtpac) +" where id='" +str(idd)+ "'"  
            query = query.replace("''", "null")
            query = query.replace(",,", ",null,")
            print(' query para el update labordendet ')
            sdk.updatePostgres(query, {},'prd') 
            print(' ordenlarga ' + ordenlarga)
        except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
    print('9')
    resp = recalcula(ordenlarga) 
    return {'statusCode': 200,'resultado': 'success'} 


# Funcion para recalcular el detalle de la OP a nivel de valores
def recalcula(ordenlarga: str): 
    qry = "select sum(subtemp) as subtemp,sum(subtpac) as subtpac,sum(cuotam) as cuotam from labordendet where ordenl='"+ ordenlarga +"'"  
    response_emp = sdk.executeQueryPostgresSelect(qry, str(stage))
    for objt in response_emp:
        totemp = objt['subtemp']
        totpac = objt['subtpac']
        cmo = objt['cuotam']
    qry = "select copago,bono,cuotam from laborden where ordenl='"+ ordenlarga +"'"  
    response_ord = sdk.executeQueryPostgresSelect(qry, str(stage))
    for obja in response_ord:
        cop = obja['copago']
        bon = obja['bono']
        #cmo = obja['cuotam']
        totpac = float(totpac) - float(cop) + float(bon) + float(cmo)
    qry = "update laborden set totpac=" + str(totpac) + ",totemp=" + str(totemp) + ",cuotam="+ str(cmo) +" where ordenl='"+ ordenlarga +"'"
    sdk.updatePostgres(qry, {},'prd') 

    return {'statusCode': 200,'resultado': 'success'} 
    

 # ---------------- tabla: paciente---------- 
# Endpoint Update 
@app.put('/paciente/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['tipide'] =='':data['tipide'] = None 
	if data['tipide'] == None:vacios = vacios +' '+ 'tipide' 
	if data['codpac'] =='':data['codpac'] = None 
	if data['codpac'] == None:vacios = vacios +' '+ 'codpac' 
	if data['nompac'] =='':data['nompac'] = None 
	if data['nompac'] == None:vacios = vacios +' '+ 'nompac' 
	if data['apepac'] =='':data['apepac'] = None 
	if data['apepac'] == None:vacios = vacios +' '+ 'apepac' 
	if data['sexo'] =='':data['sexo'] = None 
	if data['sexo'] == None:vacios = vacios +' '+ 'sexo' 
	if data['codemp'] =='':data['codemp'] = None 
	if data['codemp'] == None:vacios = vacios +' '+ 'codemp' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update paciente set tipide=%s,codpac=%s,nompac=%s,nompac2=%s,apepac=%s,apepac2=%s,sexo=%s,vincpac=%s,fecnac=%s,fecing=%s,codocu=%s,deppac=%s,ciupac=%s,gruposang=%s,codemp=%s,coddiagnostico=%s,contpac=%s,planben=%s,codundnegocio=%s,nivpac=%s,obs=%s,dir=%s,tel=%s,remite=%s,cedaco=%s,nomaco=%s,apeaco=%s,telaco=%s,diraco=%s,celular=%s,acofam=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/paciente/select') 
def conexion_postgres(): 
	query = 'SELECT id,tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,celular,acofam from paciente order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/paciente/insert') 
def insert_data(data: dict): 
    vacios = '' 
    if data['datos']['tipide'] =='':data['datos']['tipide'] = None 
    if data['datos']['tipide'] == None:vacios = vacios +','+ 'tipide' 
    if data['datos']['codpac'] =='':data['datos']['codpac'] = None 
    if data['datos']['codpac'] == None:vacios = vacios +','+ 'codpac' 
    if data['datos']['nompac'] =='':data['datos']['nompac'] = None 
    if data['datos']['nompac'] == None:vacios = vacios +','+ 'nompac' 
    if data['datos']['apepac'] =='':data['datos']['apepac'] = None 
    if data['datos']['apepac'] == None:vacios = vacios +','+ 'apepac' 
    if data['datos']['fecnac'] =='':data['datos']['fecnac'] = None 
    if data['datos']['fecnac'] == None:vacios = vacios +','+ 'fecnac' 
    if data['datos']['codemp'] =='':data['datos']['codemp'] = None 
    if data['datos']['codemp'] == None:vacios = vacios +','+ 'codemp' 
    if data['datos']['codocu'] == '':data['datos']['codocu'] = 0
    if data['datos']['nivpac'] == '':data['datos']['nivpac'] = 1
    if data['datos']['deppac'] =='':data['datos']['deppac'] = None 
    if data['datos']['deppac'] == None:vacios = vacios +','+ 'deppac' 
    if data['datos']['ciupac'] =='':data['datos']['ciupac'] = None 
    if data['datos']['ciupac'] == None:vacios = vacios +','+ 'ciupac' 
    if data['datos']['dir'] =='':data['datos']['dir'] = None 
    if data['datos']['dir'] == None:vacios = vacios +','+ 'dir' 


    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:
        query="insert into paciente(tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,celular,acofam) values ('"+data['datos']['tipide']+"','"+data['datos']['codpac']+"','"+data['datos']['nompac']+"','"+data['datos']['nompac2']+"','"+data['datos']['apepac']+"','"+data['datos']['apepac2']+"','"+data['datos']['sexo']+"','"+data['datos']['vincpac']+"','"+data['datos']['fecnac']+"',current_timestamp,"+str(data['datos']['codocu'])+",'"+data['datos']['deppac']+"','"+data['datos']['ciupac']+"','"+data['datos']['gruposang']+"','"+data['datos']['codemp']+"','"+data['datos']['coddiagnostico']+"','"+data['datos']['contpac']+"','"+data['datos']['planben']+"','"+data['datos']['codundnegocio']+"',"+str(data['datos']['nivpac'])+",'"+data['datos']['obs']+"','"+data['datos']['dir']+"','"+data['datos']['tel']+"','"+data['datos']['remite']+"','"+data['datos']['cedaco']+"','"+data['datos']['nomaco']+"','"+data['datos']['apeaco']+"','"+data['datos']['telaco']+"','"+data['datos']['diraco']+"','"+data['datos']['celular']+"','"+data['datos']['acofam']+"')" 
        query = query.replace("''", "null")   
        sdk.insertPostgres(query, data['datos'],'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint delete 
@app.delete('/paciente/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from paciente where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# Endpoint Select one
@app.get('/paciente/selectone/{codpac}') 
def conexion_postgres(codpac:str): 
	query = "SELECT id,tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,celular,acofam from paciente where codpac='"+codpac+"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint Select one only
@app.get('/paciente/selectoneonly/{ide}/{codp}') 
def conexion_postgres(ide: str,codp:str): 
	query = "SELECT id,tipide,codpac,nompac,nompac2,apepac,apepac2,sexo,vincpac,fecnac,fecing,codocu,deppac,ciupac,gruposang,codemp,coddiagnostico,contpac,planben,codundnegocio,nivpac,obs,dir,tel,remite,cedaco,nomaco,apeaco,telaco,diraco,celular,acofam from paciente where tipide = '"+ ide +"' and codpac='"+ codp +"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  


 # ---------------- tabla: lablistas---------- 
# Endpoint Update 
@app.put('/lablistas/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update lablistas set nombre=%s  where codlista='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/lablistas/select') 
def conexion_postgres(): 
	query = 'SELECT codlista,nombre from lablistas order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/lablistas/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['codlista'] =='':data['codlista'] = None 
	if data['codlista'] == None:vacios = vacios +' '+ 'codlista' 
	if data['nombre'] =='':data['nombre'] = None 
	if data['nombre'] == None:vacios = vacios +' '+ 'nombre' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into lablistas(codlista,nombre) values (%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/lablistas/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from lablistas where codlista='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: labnormal---------- 
# Endpoint Update 
@app.put('/labnormal/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['resultado'] =='':data['resultado'] = None 
	if data['resultado'] == None:vacios = vacios +','+ 'resultado' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update labnormal set cons=%s,cdgexamen=%s,cdganalisis=%s,edadmin=%s,edadmax=%s,sexo=%s,tecnica=%s,resultado=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/labnormal/select/{exa}/{ana}') 
def conexion_postgres(exa: str,ana:str): 
	query = "SELECT id,cons,cdgexamen,cdganalisis,edadmin,edadmax,sexo,tecnica,resultado from labnormal where cdgexamen='"+ exa +"' and cdganalisis='"+ ana +"' order by 1" 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/labnormal/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['resultado'] =='':data['resultado'] = None 
	if data['resultado'] == None:vacios = vacios +','+ 'resultado' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into labnormal(cons,cdgexamen,cdganalisis,edadmin,edadmax,sexo,tecnica,resultado) values (%s,%s,%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/labnormal/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from labnormal where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 

# ---------------- tabla: zreportes---------- 
# Endpoint Update 
@app.put('/zreportes/update/{id}') 
def update_data(data: dict,id:str):  
    vacios = '' 
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +','+ 'nombre' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:
        query="update zreportes set carpeta=%s,nombre=%s,usuario=%s,consulta=%s,filtros=%s,columnas=%s,medidas=%s  where cod='"+id+"'"  
        sdk.updatePostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/zreportes/select') 
def conexion_postgres(): 
	query = 'SELECT cod,carpeta,nombre,usuario,consulta,filtros,columnas,medidas from zreportes order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/zreportes/insert') 
def insert_data(data: dict): 
    vacios = '' 
    if data['nombre'] =='':data['nombre'] = None 
    if data['nombre'] == None:vacios = vacios +','+ 'nombre' 
    if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
    try:
        query='insert into zreportes(carpeta,nombre,usuario,consulta,filtros,columnas,medidas) values (%s,%s,%s,%s,%s,%s,%s)' 
        sdk.insertPostgres(query, data,'prd') 
        return {'statusCode': 200,'resultado': 'success'} 
    except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/zreportes/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from zreportes where cod='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 


 # ---------------- tabla: reglasimp---------- 
# Endpoint Update 
@app.put('/reglasimp/update/{id}') 
def update_data(data: dict,id:str):  
	vacios = '' 
	if data['tipodoc'] =='':data['tipodoc'] = None 
	if data['tipodoc'] == None:vacios = vacios +','+ 'tipodoc' 
	if data['tipocli'] =='':data['tipocli'] = None 
	if data['tipocli'] == None:vacios = vacios +','+ 'tipocli' 
	if data['imprimir'] =='':data['imprimir'] = None 
	if data['imprimir'] == None:vacios = vacios +','+ 'imprimir' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query="update reglasimp set tipodoc=%s,tipocli=%s,pagado=%s,firmado=%s,imprimir=%s,causal=%s  where id='"+id+"'"  
		sdk.updatePostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint Select 
@app.get('/reglasimp/select') 
def conexion_postgres(): 
	query = 'SELECT id,tipodoc,tipocli,pagado,firmado,imprimir,causal from reglasimp order by 1' 
	response_query = sdk.executeQueryPostgresSelect(query, str(stage)) 
	return {'data': list(response_query)}  
# Endpoint insert 
@app.post('/reglasimp/insert') 
def insert_data(data: dict): 
	vacios = '' 
	if data['tipodoc'] =='':data['tipodoc'] = None 
	if data['tipodoc'] == None:vacios = vacios +','+ 'tipodoc' 
	if data['tipocli'] =='':data['tipocli'] = None 
	if data['tipocli'] == None:vacios = vacios +','+ 'tipocli' 
	if data['imprimir'] =='':data['imprimir'] = None 
	if data['imprimir'] == None:vacios = vacios +','+ 'imprimir' 
	if (vacios!=''):raise HTTPException(status_code=400, detail= vacios + ' debe ser diligenciado') 
	try:
		query='insert into reglasimp(tipodoc,tipocli,pagado,firmado,imprimir,causal) values (%s,%s,%s,%s,%s,%s)' 
		sdk.insertPostgres(query, data,'prd') 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 
# Endpoint delete 
@app.delete('/reglasimp/delete/{id}') 
def delete_data(id: str): 
	try:
		query="delete from reglasimp where id='"+id+"'"  
		response_query = sdk.deletePostgres(query, str(stage)) 
		return {'statusCode': 200,'resultado': 'success'} 
	except Exception as e:raise HTTPException(status_code=400, detail=str(e)) 



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

