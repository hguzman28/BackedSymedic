# https://oracle.github.io/python-cx_Oracle/samples/tutorial/Python-and-Oracle-Database-Scripting-for-the-Future.html#connecting
import psycopg2
from botocore.exceptions import ClientError
import base64
import boto3
import cx_Oracle
import json
import os
import sys


#cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_19_9")

def get_secret(secret):
    secret_name = secret
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
        else:
            secret = json.loads(base64.b64decode(
                get_secret_value_response['SecretBinary']))

    # Your code goes here.
    return secret



def getConnectionPostgres(environment):

    # credential = {}
    # if environment == 'dev':
    #     credential = get_secret("JAMAR_DB_MEC_EXTENDED_DATABASE_DEV")
    # elif environment == 'prd':
    #     credential = get_secret("JAMAR_DB_MEC_EXTENDED_DATABASE_PRD")
    try:

        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="Abcd.1234")
        return conn

    except Exception as e:
        raise Exception(e)



def executeQueryPostgresSelect(query, environment):
    connection = getConnectionPostgres(environment)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        response = cursor.fetchall()
        # print(response)
        cursor.close()
        return map(lambda x: dict(zip(column_names, x)), response)
    except (Exception, psycopg2.DatabaseError) as e:
        raise Exception(e)
    finally:
        if cursor is not None:
            cursor.close()



def insertPostgres(query, data,environment):
    connection = getConnectionPostgres(environment)
    try:
        cursor = connection.cursor()
        data: dict = dict(data)
        print(len(data))
        print(list(data.values()))
        cursor.execute(query, (list(data.values())))
        connection.commit()
        #id = cursor.fetchone()[0]
        #return id
    except Exception as e:
        raise Exception(e)
        # print(sys.exc_info())
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def updatePostgres(query, data,environment):
    connection = getConnectionPostgres(environment)
    try:
        cursor = connection.cursor()
        cursor.execute(query, (list(data.values())))
        connection.commit()
    except Exception as e:
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def deletePostgres(query,environment):
    connection = getConnectionPostgres(environment)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()            






# def call_procedure_oracle_pro_aplica_pago(name_procedure, client_id, security_code, amount, payment_date):
#     connection = getConnection()
#     try:
#         print(type(amount))
#         print(type(payment_date))

#         cursor = connection.cursor()
#         ps_vcAgencia = cursor.var(str)
#         ps_vcPeriodo = cursor.var(str)
#         ps_vcRecibo = cursor.var(str)
#         ps_nuError = cursor.var(int)
#         ps_vcError = cursor.var(str)
#         cursor.callproc('PkDaoEstadoCta.proAplicaPago', [client_id, security_code, amount, payment_date, ps_vcAgencia, ps_vcPeriodo, ps_vcRecibo, ps_nuError, ps_vcError])

#         object_response = {

#             'ps_vcAgencia': ps_vcAgencia.getvalue(),
#             'ps_vcPeriodo': ps_vcPeriodo.getvalue(),
#             'ps_vcRecibo': ps_vcRecibo.getvalue(),
#             'ps_nuError': ps_nuError.getvalue(),
#             'ps_vcError': ps_vcError.getvalue(),
#         }

#         print(object_response)
#         return object_response
#     except Exception as e:
#         return {"messaje": str(e)}
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()



