from urllib.parse import urlparse
import uuid
from django.conf import settings
from pathlib import Path
import shutil
import os

local_upload_path = Path(settings.BASE_DIR) / 'static' 

BASE_URL = 'http://localhost:8000' + settings.STATIC_URL

def upload_player_to_local_server(image_path, project_id, is_path=False):

    try:
        if is_path:
            file_extension = image_path.split('.')[-1]
            id = str(uuid.uuid4()) + "." + file_extension
            local_path = local_upload_path / f'projects/{project_id}/players/{id}'
            os.makedirs(local_path.parent, exist_ok=True)
            shutil.copy(image_path, local_path)
        else:
            id = str(uuid.uuid4()) + "." + image_path.name.split('.')[-1]
            local_path = local_upload_path / f'projects/{project_id}/players/{id}'
            os.makedirs(local_path.parent, exist_ok=True)
            with open(local_path, 'wb') as local_file:
                local_file.write(image_path.read())

        relative_path = str(local_path.relative_to(settings.BASE_DIR))
        if relative_path.startswith('static\\'):   
            relative_path = relative_path[len('static/'):]

        local_image_url = BASE_URL + relative_path.replace('\\', '/')

        return local_image_url
        
    except Exception as e:
        print(e)
        return None


def upload_team_to_local_server(image_file, project_id, team_id):

    try:
        file_extension = image_file.name.split('.')[-1]
        id = str(uuid.uuid4()) + "." + file_extension
        local_path = local_upload_path / f'projects/{project_id}/teams/{team_id}/{id}'
        os.makedirs(local_path.parent, exist_ok=True)
        with open(local_path, 'wb') as local_file:
            local_file.write(image_file.read())

        relative_path = str(local_path.relative_to(settings.BASE_DIR))
        if relative_path.startswith('static\\'):   
            relative_path = relative_path[len('static/'):]

        local_image_url = BASE_URL + relative_path.replace('\\', '/')

        return local_image_url

    except Exception as e:
        print(e)
        return None


def upload_settings_to_local_server(image_file, project_id):

    try:
        file_extension = image_file.name.split('.')[-1]
        id = str(uuid.uuid4()) + "." + file_extension
        local_path = local_upload_path / f'projects/{project_id}/settings/{id}'
        os.makedirs(local_path.parent, exist_ok=True)
        with open(local_path, 'wb') as local_file:
            local_file.write(image_file.read())

        relative_path = str(local_path.relative_to(settings.BASE_DIR))
        if relative_path.startswith('static\\'):   
            relative_path = relative_path[len('static/'):]

        local_image_url = BASE_URL + relative_path.replace('\\', '/')

        return local_image_url

    except Exception as e:
        print(e)
        return None


def delete_project_image_from_local_server(project_id,s3_path):

    try:
        if s3_path.startswith('http://localhost:8000/'):
            s3_path = s3_path[len('http://localhost:8000/'):]
        
        local_path =  Path(settings.BASE_DIR) / f'{s3_path}'
        os.remove(local_path)
        return True
    
    except Exception as e:
        print(e)
        return False


def delete_team_from_local_server(project_id,team_id,s3_path):

    try:
        if s3_path.startswith('http://localhost:8000/'):
            s3_path = s3_path[len('http://localhost:8000/'):]
        
        local_path =  Path(settings.BASE_DIR) / f'{s3_path}'
        os.remove(local_path)
        return True
    
    except Exception as e:
        print(e)
        return False
    

def delete_player_from_local_server(project_id, filename):
    try:
        if filename.startswith('http://localhost:8000/'):
            filename = filename[len('http://localhost:8000/'):]
        local_path = Path(settings.BASE_DIR) / filename
      

        if local_path.exists():
            os.remove(local_path)
            return True
        else:
            print(f"File not found: {local_path}")
            return False
    except Exception as e:
        print(e)
        return False
    

def delete_project_from_local_server(project_id):

    try:
        path='static/projects/'+str(project_id)
        shutil.rmtree(path)
        return True
    
    except Exception as e:
        print(e)
        return False