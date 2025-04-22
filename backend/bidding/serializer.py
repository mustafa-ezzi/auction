from rest_framework import serializers
from .models import Project,Players,Categories,Teams
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields =["id","name","unit","max_players","min_players","logo","description","sponsor1","sponsor2","background"]

class CategoriesSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField()

    class Meta:
        model= Categories
        fields = ["id","name","base_price","player","project","project_name"]

class PlayersSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()
    project_name = serializers.ReadOnlyField()
    team_name = serializers.ReadOnlyField()
    
    class Meta:
        model= Players
        fields = ["id",'name','is_active','category','team','sold_price','division','previous_team','profile_pic','batting_style','bowling_hand','bowling_style','fielding_position','availability','project','category_name','project_name','team_name', 'video']
        
class TeamsSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField()

    class Meta:
        model= Teams
        fields = ["id","name","logo","purse_allocated","available_purse","project_name","username","password","project","user_id"]

class CategoriesDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model= Categories
        fields = ["name","id"]

class PlayersPatchSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()
    project_name = serializers.ReadOnlyField()

    class Meta:
        model= Players
        fields = ["id",'name','category','profile_pic','division','previous_team','batting_style','bowling_hand','bowling_style','fielding_position','availability','project','category_name','project_name','video']

class PlayersBulkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Players
        fields = ["id",'name','division','previous_team','batting_style','bowling_hand','bowling_style','fielding_position','availability','category','project','profile_pic']