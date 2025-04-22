from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50, null=True)
    unit = models.CharField(max_length=50, null=True)
    max_players = models.IntegerField(default=0, null=True)
    min_players = models.IntegerField(default=0, null=True)
    logo = models.CharField(max_length=255, null=True)
    sponsor1 = models.CharField(max_length=255, null=True)
    sponsor2 = models.CharField(max_length=255, null=True)
    background = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=5000, null=True)


class Categories(models.Model):
    name = models.CharField(max_length=50)
    base_price = models.IntegerField()
    player = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    @property
    def project_name(self):
        return self.project.name


class Teams(models.Model):
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=255, null=True)
    purse_allocated = models.IntegerField()
    available_purse = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=20, null=True)
    user_id=models.IntegerField(null=True)

    @property
    def project_name(self):
        return self.project.name


class Players(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.CharField(max_length=500, null=True)
    batting_style = models.CharField(max_length=250, null=True)
    bowling_hand = models.CharField(max_length=250, null=True)
    bowling_style = models.CharField(max_length=250, null=True)
    fielding_position = models.CharField(max_length=250, null=True)
    division = models.CharField(max_length=250, null=True)
    previous_team = models.CharField(max_length=250, null=True)
    availability = models.CharField(max_length=250, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True)
    turn = models.CharField(default="False", null=True, max_length=22)
    is_active = models.BooleanField(null=True,default=True)
    sold_price = models.FloatField(null=True)
    video = models.CharField(max_length=500, null=True)

    @property
    def category_name(self):
        return self.category.name

    @property
    def project_name(self):
        return self.project.name

    @property
    def team_name(self):
        return self.team.name



