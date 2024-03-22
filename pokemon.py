import logging  # Pour permettre la journalisation des messages, notamment pour enregistrer les erreurs et les informations importantes lors de l'exécution du programme.
import sys  # Pour obtenir des informations sur le système, telles que la gestion des flux de sortie standard et d'autres paramètres système.
import click  # Pour créer une interface de ligne de commande conviviale, facilitant l'interaction avec votre programme via le terminal.
import requests  # Pour envoyer des requêtes HTTP vers des serveurs distants et récupérer les réponses, utilisé ici pour interroger l'API Pokémon.
from dataclasses import (
    dataclass,
)  # Pour simplifier la création de classes de données en Python avec la syntaxe des décorateurs, ce qui rend le code plus concis et lisible.
from typing import (
    Optional,
    Dict,
    Any,
)  # Pour annoter les types dans mon code, améliorant ainsi la lisibilité et permettant une meilleure compréhension du fonctionnement des fonctions et des méthodes.
from requests.exceptions import (
    RequestException,
)  # Pour capturer spécifiquement les exceptions liées aux requêtes HTTP, telles que les erreurs de connexion ou de délai d'attente.


@dataclass
class Pokemon:
    id: int
    name: str
    height: str
    weight: str
    evolves_from: Optional[str]
    evolves_to: Optional[str]

    def __init__(self, data: Dict[str, Any]):
        self.id = data["id"]
        self.name = data["name"]
        self.height = data["height"]
        self.weight = data["weight"]
        species_info = self._get_species_info(data["species"]["url"])
        if species_info is not None:
            evolves_from_species = species_info.get("evolves_from_species")
            if evolves_from_species is not None:
                self.evolves_from = evolves_from_species.get("name")
            else:
                self.evolves_from = "None"
            self.evolves_to = self._get_evolves_to(species_info)
        else:
            self.evolves_from = None
            self.evolves_to = None

    def _get_species_info(self, url: str) -> Optional[Dict[str, Any]]:
        response = self._make_request(url)
        if response is not None:
            species_info = response.json()
            if species_info:
                return species_info
        return None

    def _get_evolves_to(self, species_info: Dict[str, Any]) -> Optional[str]:
        evolution_chain_url = species_info.get("evolution_chain", {}).get("url")
        if evolution_chain_url:
            response = self._make_request(evolution_chain_url)
            if response:
                evolution_chain = response.json()
                chain = evolution_chain.get("chain", {})
                while chain:
                    if chain.get("species", {}).get("name") == self.name:
                        evolves_to = chain.get("evolves_to")
                        if evolves_to:
                            return evolves_to[0].get("species", {}).get("name")
                        else:
                            return None
                    chain = (
                        chain.get("evolves_to", [])[0]
                        if chain.get("evolves_to")
                        else None
                    )
        return None

    def _make_request(self, url: str) -> Optional[requests.Response]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def get_info(self):
        click.echo(f"ID: {self.id}")
        click.echo(f"Name: {self.name}")
        click.echo(f"Height: {self.height}")
        click.echo(f"Weight: {self.weight}")
        if self.evolves_from:
            click.echo(f"Evolves From: {self.evolves_from}")
        elif self.evolves_from is None:
            click.echo("No previous evolution.")
        if self.evolves_to:
            click.echo(f"Evolves To: {self.evolves_to}")
        elif self.evolves_to is None:
            click.echo("No further evolution.")


class PokeApi:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, name: str) -> Optional[Pokemon]:
        url = f"{self.base_url}pokemon/{name}/"
        response = self._make_request(url)
        if response is not None:
            pokemon_data = response.json()
            if pokemon_data:
                return Pokemon(pokemon_data)
        return None

    def _make_request(self, url: str) -> Optional[requests.Response]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None


@click.command()
@click.argument("name")
def search_pokemon(name):
    api = PokeApi()
    pokemon = api.get_pokemon(name)
    if pokemon:
        pokemon.get_info()
    else:
        click.echo("No Pokemon found with that name.")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    search_pokemon()