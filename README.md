# Documentación 

1.  Estructura de nombre de appventass y servicios:
2.  Definición del Flujo
3.  Definición de ramas
4.  Buenas practicas
5.  Definición de numeración versiones
6.  Requisitos para pruebas locales

## Estructura de nombre de appventass y servicios:

**Repositorios:** {NombreDelProyecto}-{NombreDelServicio}

### Endpoint de servicios:

**Ambiente Dev:** \
🔄Se actualiza cada vez que se hace un merge request a la rama dev🔄
https://dev.symedic.com.co/{NombreDelProyecto}-{NombreDelServicio}/{path}

**Ambiente qa:** \
 🔄Se actualiza cada vez que se hace un merge request a la rama qa🔄
https://qa.symedic.com.co/{NombreDelProyecto}-{NombreDelServicio}/{path}

**Ambiente prd:**\
🔄Se actualiza cada vez que se hace un merge request a la rama main🔄
https://prd.symedic.com.co/{NombreDelProyecto}-{NombreDelServicio}/{path}

## Definición del Flujo

![image](https://user-images.githubusercontent.com/80862575/205971980-af6f840b-60c7-4ffe-a1a5-65adc769e40d.png)

1.  Al iniciar un Sprint se debe sacar una rama desde
develop y nombrarla sprint/XXX (ejm sprint/22), se recomienda ya no
trabajar más en las anteriores ramas de Sprint y todo trabajarlo en la
última creada. 
2.  Para desarrollar una funcionalidad se debe sacar de la
rama sprint/XX una rama con nombre feature/XXXX y se realiza el
desarrollo (recomendable que la rama lleve el nombre de la historia de
usuario a implementar) 
3.  Al terminar el desarrollo se debe realizar
merge a la rama del sprint, dando una descripción breve de la
funcionalidad. 
4.  Después de terminado el sprint se debe generar un merge
request desde la rama del sprint a develop 
5.  Después de terminado el sprint y tener el código terminado en develop, se debe generar un merge request desde la rama de develop a qa, para proceder con las pruebas de certificación. 
6. Después de terminadas las pruebas de certificación de
una versión y dar la aprobación para pasar a producción, se debe generar
un merge request desde la rama de qa(certificación) a main (producción),
para proceder con la salida a producción.

## Definición de ramas

**Rama de Producción (main)** Esta rama debe ser "protegida", es decir, sólo
los roles Team Leardes y Owner pueden hacer modificaciones sobre ella.
Esta rama solo tendrá versiones en producción y que fueron certificadas
por pruebas.

**Rama de certificación (QA)** Esta rama debe ser "protegida", es decir,
sólo los roles Team Leardes y Owner pueden hacer modificaciones sobre
ella. Esta rama solo tendrá versiones en certificación y próximas a ser
publicadas en producción.

**Rama de desarrollo (develop o dev)** Al iniciar el desarrollo, se debe
crear una rama protegida sobre la cual se van a realizar los merges de
las diferentes "features" que se van agregando. De esta rama se pueden
desprender sub-ramas, para cada "sprint", la adición de "features" o la
corrección de bugs.

**Rama del sprint (sprint/XXX)** Al iniciar cada Sprint se debe crear una
rama a la cual se asocian todos las features correspondientes a ese
Sprint. Se debe hacer merge con la rama develop para mantener
actualizado el appventas.

**Rama de funcionalidad (feature/XXX)** Con la adición de una nueva
característica al producto se debe crear una rama (local o remota) no
protegida, a partir de la rama de desarrollo.

Para appventass ágiles, debería haber una rama por historia de usuario y
no deberían durar más de un ciclo de desarrollo.

El formato para la creación de ramas de funcionalidad es:

**feature/\[nombre funcionalidad\]**

**Por ejemplo:**

**feature/hu20**

Después de terminada la funcionalidad se debe hacer un merge request a
la rama del sprint al que corresponde la funcionalidad y una persona
diferente a quien desarrollo, debe aceptarlo

Rama de correcciones (hotfix /XXX) En ocasiones particulares se requiere
corregir un error de una versión entregada al cliente (producción o
pruebas del cliente). El formato para la creación de ramas de corrección
es:

**hotfix/\[nombre corrección\]**

**Por ejemplo: hotfix/ticket001**

Tags (vX.Y.Z) Aunque internamente, una rama y un tag son manejados de la
misma forma, conceptualmente son diferentes. El tag es una "foto" del
estado del producto en un momento específico, por lo cual, deben ser
sólo de lectura. Cuando se genera una versión estable en producción o
para pruebas de certificación se debe crear un tag que la identifique.

El formato para la creación de tags es el siguiente, bajo la Definición
de numeración de versiones:

v\[X.Y.Z\]

**Por ejemplo: v1.0.3**

## Buenas practicas 🚀
1.  NUNCA modificar directamente la línea base (rama
main) y certificación (rama qa). Las modificaciones se deben realizar
sobre ramas de desarrollo/release/fix. Las únicas modificaciones sobre
la línea base deben ser hechas mediante "merge" de ramas, el merge se
realizará solicitando un merge request. 
2.  Se debe sincronizar frecuentemente el código en el ambiente local, como mínimo, al iniciar labores y antes de hacer cada commit.\
3.  Cada desarrollador debe garantizar que el código que se suba al
repositorio, esté estable (compila correctamente).
4.  Deben realizarse commits granulares, es decir, no mezclar diferentes
issues/temas/historias de usuario dentro de un mismo commit. Esto es,
con la finalización de una tarea específica, una porción de código con
una funcionalidad puntual o la creación/modificación de
módulos/componentes.
5.  Cada commit debe tener esta estructura 
```
<tipo-de-commit>:<descripcion> \
 tipos <tipo-de-commit> (Add, Change, Fix, Remove) \
 Ejemplos: \
 add a new search feature \
 fix a problem with the topbar \
 change the default system color \
 remove a random notification
 ```
6.  No hacer modificaciones (commit) sobre TAGs, estos deben ser sólo de lectura. 
7.  Los nombres de los artefactos deben tener sólo caracteres alphanuméricos \[0-9A-Za-z-\] y no deben contener tildes, espacios ni caracteres especiales diferentes a . --


## Definición de numeración versiones

Se debe definir para cada appventas, cuál será la estructura de
numeración de las versiones. La propuesta estándar es:

![image](https://user-images.githubusercontent.com/80862575/205971832-f8e8ee8c-71ed-4db2-b21a-e1e63529ac9c.png)

## Requisitos para pruebas locales
- Python 3.8 o 3.9
- Cliente Oracle, descargar [aquí](https://drive.google.com/file/d/1musU0zbSWz6AB9YBGr7eUgt8NVrsNbEc/view?usp=sharing)

## Instalar dependencias
En el archivo de requerimientos.txt están todas las dependencias, usa el siguiente comando para instalarlas.

``` basch
pip install -r ./requirements.txt
```

TIP: Antes de instalar las dependencias, no olvidar crear un ambiente virtual.

## Correr localmente
- Descargar el cliente Oracle y ubicarlo en el lugar de su preferencia.
En el archivo sdk.py, ubicar la linea *cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_9")*, descomentar y actualizar la ruta del cliente Oracle.

Para correr el appventas localmente, usar los siguientes comandos:

``` python
uvicorn main:app --reload 
```

Podrías probarlo 
```
curl http://localhost:8000/{NombreDelProyecto}-{NombreDelServicio}/{path}
```
