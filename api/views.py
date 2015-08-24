from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from suds.client import Client


def get_client(url):    
    client = Client(url)
    credentials = client.factory.create('credentials')
    credentials.username = 'webmail'
    credentials.password = 'webmail'
    client.set_options(soapheaders=credentials)
    return client

def autenticar(username, password):
    response = {'esDocente': False}

    url_seguridad = 'http://academico.espoch.edu.ec/OAS_Interop/Seguridad.wsdl'
    url_carrera = 'http://academico.espoch.edu.ec/OAS_Interop/InfoCarrera.wsdl'
    client = get_client(url_seguridad)
    result = client.service.AutenticarUsuarioCarrera(username, password)

    if result is None:
        return result

    roles = result.RolCarrera
    client = get_client(url_carrera)
    
    for rol in roles:
        if rol.NombreRol == 'DOC':
            docente = client.service.GetDatosUsuarioCarrera(rol.CodigoCarrera, username)
            response['cedula'] = docente.Cedula
            response['nombres'] = docente.Nombres
            response['apellidos'] = docente.Apellidos
            response['email'] = docente.Email
            response['esDocente'] = True
            return response

    estudiante = client.service.GetDatosUsuarioCarrera(roles[0].CodigoCarrera, username)
    response['cedula'] = estudiante.Cedula
    response['nombres'] = estudiante.Nombres
    response['apellidos'] = estudiante.Apellidos
    response['email'] = estudiante.Email    
    return response

@api_view(['POST',])
def login(request):    
    if request.method == 'POST':        
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = autenticar(username, password)
        if response is None:
            return Response('Not found',status=status.HTTP_404_NOT_FOUND)            

        return Response(response, status=status.HTTP_200_OK)