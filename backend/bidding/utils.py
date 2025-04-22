from bidding.models import Players
import os


def process_team_object(team, current_category, categories):

    hash_category = {}
    minimum_amount_for_auction = 0

    for i in categories:
        hash_category[i.id] = {
            "base_price": i.base_price,
            "players": i.player,
            "purse": i.base_price * i.player,
        }

        players = Players.objects.filter(category=i, team=team.id)

        hash_category[i.id]["players"] = hash_category[i.id]["players"] - len(players)

        for j in players:
            hash_category[i.id]["purse"] = hash_category[i.id]["purse"] - j.sold_price

    for hash in hash_category:
        minimum_amount_for_auction = minimum_amount_for_auction + (
            hash_category[hash]["players"] * hash_category[hash]["base_price"]
        )

    extra_amount = team.available_purse - minimum_amount_for_auction
    extra_amount = extra_amount + hash_category[current_category]["base_price"]

    return extra_amount


def find_csv_and_media_paths(base_path):
    csv_file_path = None
    media_folder_path = None

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_file_path = os.path.join(root, file)
                break

    for root, dirs, files in os.walk(base_path):
        if "media" in dirs:
            media_folder_path = os.path.join(root, "media")
            break

    return csv_file_path, media_folder_path
