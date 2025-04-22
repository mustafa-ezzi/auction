from dotenv import load_dotenv
load_dotenv()
from bidding.upload_to_s3 import *
from bidding.upload_to_local_server import *


ENVIRONMENT = os.getenv('ENVIRONMENT')

def upload_player(player_image, project_id, isPath):

    if ENVIRONMENT == 'local':
        image_string = upload_player_to_local_server(player_image, project_id, isPath)
    else:
        image_string = upload_player_to_s3(player_image, project_id, isPath)

    return image_string


def upload_team(team_logo, project_id, team_id):
        
    if ENVIRONMENT == 'local':
        image_string = upload_team_to_local_server(team_logo, project_id, team_id)
    else:
        image_string = upload_team_to_s3(team_logo, project_id, team_id)

    return image_string


def upload_settings(project_logo, project_id):  
        
    if ENVIRONMENT == 'local':
        image_string = upload_settings_to_local_server(project_logo, project_id)
    else:
        image_string = upload_settings_to_s3(project_logo, project_id)

    return image_string


def delete_project(project_id):
            
    if ENVIRONMENT == 'local':
        status = delete_project_from_local_server(project_id)
    else:
        status = delete_project_from_s3(project_id)

    return status

def delete_project_image(project_id,s3_path):
            
    if ENVIRONMENT == 'local':
        status = delete_project_image_from_local_server(project_id,s3_path)
    else:
        status = delete_key_from_s3(s3_path)

    return status

def delete_team_image(project_id, team_id, s3_path):
                
    if ENVIRONMENT == 'local':
        status = delete_team_from_local_server(project_id, team_id,s3_path)
    else:
        status = delete_key_from_s3(s3_path)

    return status


def delete_team(project_id,team_id,s3_path):

    if ENVIRONMENT == 'local':
        status = delete_team_from_local_server(project_id, team_id,s3_path)
    else:
        status = delete_team_from_s3(project_id, team_id)

    return status


def delete_player(project_id, previous_image):
                
    if ENVIRONMENT == 'local':
        status = delete_player_from_local_server(project_id, previous_image)
    else:
        status = delete_player_from_s3(project_id, previous_image)

    return status


def delete_player_image(project_id, player_id,s3_path):
                
    if ENVIRONMENT == 'local':
        status = delete_player_from_local_server(project_id, s3_path)
    else:
        status = delete_key_from_s3(s3_path)

    return status
