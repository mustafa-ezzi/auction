import csv
import io
from django.db.models import Q
import uuid
import random
from urllib.parse import urlparse
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bidding.fixed_response import FixedResponseMixin
from bidding.serializer import (
    PlayersPatchSerializer,
    PlayersSerializer,
    ProjectSerializer,
    CategoriesSerializer,
    TeamsSerializer,
)
from bidding.upload import (
    delete_player,
    delete_player_image,
    delete_project_image,
    delete_team,
    delete_project,
    delete_team_image,
    upload_player,
    upload_team,
    upload_settings,
)
from bidding.utils import process_team_object
from user.serializers import UserRegistrationSerializer
from .models import Project, Categories, Players, Teams
from django.db import IntegrityError

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class ProjectApiView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serialized = ProjectSerializer(project)
            return self.get_fixed_response(
                message=None, data=serialized.data, status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return self.get_fixed_response(
                message=str(e), data=None, status_code=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request, pk):

        project_data = request.data

        project_logo = request.FILES.get("logo", None)
        sponsor1 = request.FILES.get("sponsor1", None)
        sponsor2 = request.FILES.get("sponsor2", None)
        background = request.FILES.get("background", None)

        # Remove the file fields from project_data as they're handled separately
        for field in ["logo", "sponsor1", "sponsor2", "background"]:
            if field in project_data:
                del project_data[field]

        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project, data=project_data, partial=True)

        if serializer.is_valid():
            if project_logo:
                serializer.instance.logo = upload_settings(project_logo, pk)

            if sponsor1:
                serializer.instance.sponsor1 = upload_settings(sponsor1, pk)

            if sponsor2:
                serializer.instance.sponsor2 = upload_settings(sponsor2, pk)

            if background:
                serializer.instance.background = upload_settings(background, pk)

            serializer.save()

            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_200_OK
            )
        else:
            return self.get_fixed_response(
                message="Serializer Issue",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

    def delete(self, request, pk, *args, **kwargs):
        project = Project.objects.get(pk=pk)
        # delete project media from S3/Local
        delete_project(pk)
        project.delete()

        return self.get_fixed_response(
            message="Project deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )


class ProjectPostApiVeiw(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        project_data = request.data

        serializer = ProjectSerializer(data=project_data)

        if serializer.is_valid():
            serializer.save()
            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_201_CREATED
            )

        return self.get_fixed_response(
            message="Serializer Issue",
            data=None,
            status_code=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
        )

    def get(self, request):
        projects = Project.objects.all().order_by("name")
        serializer = ProjectSerializer(projects, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class CategoriesPostApiView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        categories_data = request.data
        serializer = CategoriesSerializer(data=categories_data)

        if serializer.is_valid():
            serializer.save()
            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_201_CREATED
            )
        else:
            return self.get_fixed_response(
                message="Serializer Issue",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

    def get(self, request):
        categories = Categories.objects.select_related("project").all()
        serializer = CategoriesSerializer(categories, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class CategoriesApiView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = Categories.objects.select_related("project").get(pk=pk)
        serializer = CategoriesSerializer(category)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )

    def patch(self, request, pk, *args, **kwargs):
        category = Categories.objects.select_related("project").get(pk=pk)
        serializer = CategoriesSerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_200_OK
            )
        else:
            return self.get_fixed_response(
                message="Serializer Issue",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

    def delete(self, request, pk, *args, **kwargs):
        Categories.objects.get(pk=pk).delete()
        return self.get_fixed_response(
            message="Category deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )


class PlayersPostApiView(FixedResponseMixin, APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):

        player_data = request.data

        project_id = player_data.get("project")

        uploaded_image = request.FILES.get("profile_pic", None)

        if "profile_pic" in player_data:
            del player_data["profile_pic"]

        serializer = PlayersSerializer(data=player_data)

        if serializer.is_valid():
            serializer.save()

            if uploaded_image:
                s3_image_path = upload_player(uploaded_image, project_id, False)

                if s3_image_path:
                    serializer.instance.profile_pic = s3_image_path
                    serializer.instance.save()

            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_201_CREATED
            )
        return self.get_fixed_response(
            message="Serializer Issue",
            data=None,
            status_code=status.HTTP_400_BAD_REQUEST,
            error=serializer.errors,
        )

    def get(self, request):
        players = Players.objects.select_related("category", "project", "team").all()
        serializer = PlayersSerializer(players, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class PlayersApiView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        player = Players.objects.select_related("category", "project", "team").get(
            pk=pk
        )
        serializer = PlayersSerializer(player)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )

    def patch(self, request, pk, *args, **kwargs):

        player_data = request.data.copy()

        uploaded_image = request.FILES.get("profile_pic", None)

        if "profile_pic" in player_data:
            del player_data["profile_pic"]

        player = Players.objects.get(pk=pk)
        serializer = PlayersPatchSerializer(player, data=player_data, partial=True)

        if serializer.is_valid():
            if uploaded_image:
                s3_image_path = upload_player(uploaded_image, player.project_id, False)
                serializer.instance.profile_pic = s3_image_path

            serializer.save()

            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_200_OK
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        player = Players.objects.get(pk=pk)
        # TODO: no need for try catch here, always should be link
        try:
            parsed_url = urlparse(player.profile_pic)
            filename = parsed_url.path.split("/")[-1]
            delete_player(player.project.id, filename)
        except Exception as e:
            pass
        player.delete()
        return Response(
            {"message": "Player deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TeamsPostApiView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        data = request.data

        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )
        team_name_cleaned = data["name"].lower().replace(" ", "_")
        random_string_cleaned = random_string.lower()
        username = f"{team_name_cleaned}_{random_string_cleaned}"

        data["username"] = username
        data["password"] = str(uuid.uuid4())[:8]

        user_data = {"username": username, "role": "team", "password": data["password"]}
        serializer = UserRegistrationSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()

        data["user_id"] = serializer.instance.id

        logo_image = request.FILES.get("logo", None)

        data.pop("logo")

        serializer = TeamsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if logo_image:
                s3_image_path = upload_team(
                    logo_image, data["project"], serializer.data["id"]
                )
                if s3_image_path:
                    serializer.instance.logo = s3_image_path
                    serializer.instance.save()

            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_201_CREATED
            )
        else:
            return self.get_fixed_response(
                message="Serializer Issue",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

    def get(self, request):
        teams = Teams.objects.select_related("project").all()
        serializer = TeamsSerializer(teams, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class TeamsApiView(FixedResponseMixin, APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        teams = Teams.objects.get(pk=pk)
        serializer = TeamsSerializer(teams)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )

    def patch(self, request, pk, *args, **kwargs):

        data = request.data.copy()
        logo_image = request.FILES.get("logo", None)

        if "logo" in data:
            del data["logo"]

        team = Teams.objects.select_related("project").get(pk=pk)
        serializer = TeamsSerializer(team, data=data, partial=True)

        if serializer.is_valid():

            if logo_image:
                s3_image_path = upload_team(logo_image, team.project.id, team.id)
                serializer.instance.logo = s3_image_path

            serializer.save()

            return self.get_fixed_response(
                message=None, data=serializer.data, status_code=status.HTTP_200_OK
            )

        else:
            return self.get_fixed_response(
                message="Serializer Issue",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

    def delete(self, request, pk):
        team = Teams.objects.get(pk=pk)
        delete_team(team.project.id, pk, team.logo)
        team.delete()
        return self.get_fixed_response(
            message="Team deleted successfully",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT,
        )


class CategoryDropdownApiView(FixedResponseMixin, APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        categories = (
            Categories.objects.filter(project=project_id)
            .select_related("project")
            .order_by("name")
        )
        serializer = CategoriesSerializer(categories, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class GetAllTeamsByProject(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        team = (
            Teams.objects.filter(project=project_id)
            .select_related("project")
            .order_by("name")
        )
        teamserializer = TeamsSerializer(team, many=True)
        return self.get_fixed_response(
            message=None, data=teamserializer.data, status_code=status.HTTP_200_OK
        )


class GetAllPlayersByProject(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        players = (
            Players.objects.filter(project=project_id)
            .select_related("project", "category", "team")
            .order_by("id")
        )
        serializer = PlayersSerializer(players, many=True)
        return self.get_fixed_response(
            message=None, data=serializer.data, status_code=status.HTTP_200_OK
        )


class PlayerSold(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        team_id = data["team_id"]
        sold_price = data["sold_price"]
        player_id = data["player_id"]

        team = Teams.objects.get(pk=team_id)
        team.available_purse = team.available_purse - sold_price
        team.save()

        player = Players.objects.get(pk=player_id)

        player.team = team

        player.sold_price = sold_price

        player.save()

        return self.get_fixed_response(
            message=f"Player {player.name} sold out to {team.name} at Price {sold_price}",
            data=None,
            status_code=status.HTTP_200_OK,
        )


class PlayerReverse(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        player = Players.objects.get(pk=pk)

        team = Teams.objects.get(pk=player.team.id)
        team.available_purse = team.available_purse + player.sold_price
        team.save()

        player.turn = "False"
        player.team = None
        player.sold_price = 0
        player.save()

        return self.get_fixed_response(
            message=f"Player {player.name} available for auction",
            data=None,
            status_code=status.HTTP_200_OK,
        )


class BulkPlayer(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data["project"]
        uploaded_file = request.FILES.get("file")

        try:
            # Fetch the Project instance using project_id
            project = get_object_or_404(Project, id=project_id)

            # Cache all categories in a dictionary for quick lookup
            categories = {
                category.id: category for category in Categories.objects.all()
            }

            file_wrapper = io.TextIOWrapper(uploaded_file.file, encoding="utf-8")
            csv_reader = csv.reader(file_wrapper)

            # Skip the header row if the CSV has one
            headers = next(csv_reader, None)
            players_to_create = []
            errors = []

            # Iterate over each row in the CSV file
            for row in csv_reader:
                try:
                    # Get the Category instance from the cached dictionary
                    category_id = int(row[10])
                    category = categories.get(category_id)

                    if not category:
                        errors.append(
                            {
                                "row": row,
                                "error": f"Category with ID {category_id} not found.",
                            }
                        )
                        continue

                    # Create a Player instance for each row
                    player = Players(
                        name=f"{row[1]} {row[2]}".strip(),
                        batting_style=row[3],
                        bowling_hand=row[4],
                        bowling_style=row[5],
                        fielding_position=row[6],
                        availability=row[7],
                        division=row[8],
                        previous_team=row[9],
                        category=category,
                        profile_pic=row[11],
                        project=project,
                    )
                    players_to_create.append(player)
                except ValueError as ve:
                    # Handle data conversion errors (e.g., invalid integer fields)
                    errors.append({"row": row, "error": str(ve)})
                except IndexError as ie:
                    # Handle missing columns in a row
                    errors.append({"row": row, "error": str(ie)})

            # Use Django's bulk_create for better performance
            if players_to_create:
                try:
                    Players.objects.bulk_create(players_to_create)
                except IntegrityError as ie:
                    # Handle any database integrity errors during bulk create
                    return self.get_fixed_response(
                        message="Database integrity error during bulk creation",
                        data=None,
                        status_code=status.HTTP_400_BAD_REQUEST,
                        error=str(ie),
                    )

            # If there are any errors, return them
            if errors:
                return self.get_fixed_response(
                    message="Some records failed",
                    data={"errors": errors},
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error=None,
                )

            return self.get_fixed_response(
                message="Bulk Upload Completed",
                data=None,
                status_code=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return self.get_fixed_response(
                message="An error occurred during file processing",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
                error=str(e),
            )


class TeamPlayer(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id):

        players = (
            Players.objects.filter(team=team_id)
            .select_related("category", "project", "team")
            .order_by("name")
        )
        playerserializer = PlayersSerializer(players, many=True)
        return self.get_fixed_response(
            message=None, data=playerserializer.data, status_code=status.HTTP_200_OK
        )


class TeamLogin(FixedResponseMixin, APIView):
    def post(self, request):
        data = request.data

        username = data["username"]
        password = data["password"]

        try:
            teams = Teams.objects.select_related("project").get(
                username=username, password=password
            )
        except Teams.DoesNotExist:
            return self.get_fixed_response(
                message="Invalid credentials",
                data=None,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TeamsSerializer(teams)
        return self.get_fixed_response(
            message="Successfully Logged In",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class ResetUnsoldPlayers(FixedResponseMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):

        players_without_team_and_turn = Players.objects.filter(
            project=pk, team__isnull=True, turn="True"
        )

        players_without_team_and_turn.update(turn="False")

        return self.get_fixed_response(
            message=str(len(players_without_team_and_turn)) + " Players Turn Updated",
            data=[],
            status_code=status.HTTP_200_OK,
        )


class GenerateCSV(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        sold_players = (
            Players.objects.filter(project=project_id, sold_price__isnull=False)
            .select_related("team", "project")
            .order_by("team__name")
        )

        serializers = PlayersSerializer(sold_players, many=True)

        return self.get_fixed_response(
            message=None,
            data=serializers.data,
            status_code=status.HTTP_200_OK,
        )


class UnsoldPlayers(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, category_id):

        players_without_team_and_turn = (
            Players.objects.filter(
                project=pk, turn="True", category=category_id, sold_price=None
            )
            .select_related("project", "category")
            .order_by("name")
        )

        serializer = PlayersSerializer(players_without_team_and_turn, many=True)

        return self.get_fixed_response(
            message=None,
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class RandomPlayers(FixedResponseMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        category_id = data.get("category_id")
        project_id = data["project_id"]
        player_id = data.get("player_id", None)
        # Filter by player_id if provided, otherwise by category
        query = Q(turn="False", project=project_id, is_active=True)
        if player_id:
            query &= Q(id=player_id)
        elif category_id:
            query &= Q(category=category_id)

        # Use order_by('?') to randomly select one player and select_related() for optimization
        selected_player = (
            Players.objects.filter(query)
            .select_related("project", "category")
            .order_by("?")
            .first()
        )

        if selected_player:
            selected_player.turn = "True"
            selected_player.save()

            serializer = PlayersSerializer(selected_player)
            selected_player = serializer.data

        return self.get_fixed_response(
            message=None, data=selected_player, status_code=status.HTTP_200_OK
        )


class TeamBid(FixedResponseMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        project_id = data["project_id"]
        category_id = data["category_id"]

        # Fetch all necessary data at the beginning
        teams = Teams.objects.filter(project=project_id)
        categories = Categories.objects.filter(project=project_id)
        players = Players.objects.filter(project=project_id).select_related(
            "category", "team"
        )

        # Create a dictionary for fast lookup of players per team and category
        players_by_team_and_category = {}
        for player in players:
            if player.team_id not in players_by_team_and_category:
                players_by_team_and_category[player.team_id] = {}
            if player.category_id not in players_by_team_and_category[player.team_id]:
                players_by_team_and_category[player.team_id][player.category_id] = []
            players_by_team_and_category[player.team_id][player.category_id].append(
                player
            )

        project_teams = []

        # Loop over each team and process each team's data
        for team in teams:
            # Pass only categories to the utility function
            result = process_team_object(team, category_id, categories)

            # Prepare category data for each team
            categories_data = []
            for category in categories:
                purchased_category = players_by_team_and_category.get(team.id, {}).get(
                    category.id, []
                )
                purchased_count = len(purchased_category)
                remaining_count = category.player - purchased_count

                category_data = {
                    "id": category.id,
                    "name": category.name,
                    "purchased": purchased_count,
                    "remaining": remaining_count,
                }
                categories_data.append(category_data)

            # Prepare team data
            team_data = {
                "team_id": team.id,
                "team_name": team.name,
                "team_logo": team.logo,
                "max_bid": result,
                "categories": categories_data,
            }

            project_teams.append(team_data)

        sorted_teams = sorted(project_teams, key=lambda x: x["team_name"].lower())

        return self.get_fixed_response(
            message=None, data=sorted_teams, status_code=status.HTTP_200_OK
        )


class DeleteAPIView(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        type = request.data.get("type")
        sub_type = request.data.get("sub_type")
        id = request.data.get("id")

        if type == "settings":
            project = get_object_or_404(Project, pk=id)
            if sub_type == "logo":
                delete_project_image(id, project.logo)
                project.logo = None
            elif sub_type == "sponsor1":
                delete_project_image(id, project.sponsor1)
                project.sponsor1 = None
            elif sub_type == "sponsor2":
                delete_project_image(id, project.sponsor2)
                project.sponsor2 = None
            elif sub_type == "background":
                delete_project_image(id, project.background)
                project.background = None

            project.save()

        if type == "team":
            team = get_object_or_404(Teams, pk=id)
            delete_team_image(team.project.id, team.id, team.logo)
            team.logo = None
            team.save()

        if type == "player":
            player = get_object_or_404(Players, pk=id)
            delete_player_image(player.project.id, id, player.profile_pic)
            player.profile_pic = None
            player.save()

        return self.get_fixed_response(
            message=f"Image deleted for {type}",
            data=None,
            status_code=status.HTTP_200_OK,
        )


class UpdateSoldPrice(FixedResponseMixin, APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        player_query = Players.objects.get(pk=pk)
        team_query = Teams.objects.get(pk=player_query.team.id)
        new_price = request.data["sold_price"]

        if team_query.purse_allocated < new_price:
            return self.get_fixed_response(
                message=f"Sold price cannot be greater than {team_query.purse_allocated}",
                data=None,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        current_price = player_query.sold_price

        player_query.sold_price = new_price
        player_query.save()

        reverse_purse = team_query.available_purse + current_price - new_price
        team_query.available_purse = reverse_purse
        team_query.save()

        return self.get_fixed_response(
            message=f"Sold price updated Successfully, the new price is {new_price} and the purse availible is {team_query.available_purse}",
            data=None,
            status_code=status.HTTP_200_OK,
        )
