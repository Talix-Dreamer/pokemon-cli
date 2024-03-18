# Importation des mudules nécéssaire pour le bien du projet
import requests
import argparse


# Trouver le pokémon
def search_pokemon(name):
    URL = "https://pokeapi.co/api/v2/pokemon/" + name + "/"
    RESPONSE = requests.get(URL)
    if RESPONSE.status_code == 200:
        POK_DATA = RESPONSE.json()
        return {
            "Nom": POK_DATA["name"].capitalize(),
            "Taille": POK_DATA["height"],
            "Poid": POK_DATA["weight"],
            "Abilités": [
                ability["ability"]["name"] for ability in POK_DATA["abilities"]
            ],
        }
    else:
        raise ValueError("There is no pokemon.")


# Code des actions dans le terminal et assemblage des functions
def main():
    PARSER = argparse.ArgumentParser(
        description="Search for pokemon information in progress."
    )
    PARSER.add_argument("action", choices=["search"], help="action to perform")
    PARSER.add_argument("--name", help="name of pokemon to look for.")
    ARGS = PARSER.parse_args()
    if ARGS.action == "search" and ARGS.name:
        try:
            POKEMON_INFO = search_pokemon(ARGS.name)
            print(POKEMON_INFO)
        except ValueError as e:
            print(e)


# condition finale
if __name__ == "__main__":
    main()
