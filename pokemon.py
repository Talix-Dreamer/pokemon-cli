import requests
import click

class PokeAPI:
    def __init__(self, name):
        self.name = name
        self.url = f"https://pokeapi.co/api/v2/pokemon/{self.name}/"
    
    def get_api(self, url_api, information=None):
        try:
            response = requests.get(url_api)
            response.raise_for_status()  # Vérifie si la requête a réussi
            data = response.json()
            if information is None:
                return data
            else:
                return data.get(information)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    def get_species(self, species_url):
        data_species = self.get_api(species_url)
        if data_species is not None:
            return data_species.get("evolves_from_species", {}).get("name", "Not specified")
        else:
            return "Not specified"
   
        
    def has_next_evolution(self):
        species_url_info = self.get_api(self.url, "species")
        if species_url_info:
            species_url = species_url_info.get('url')
            data_species = self.get_api(species_url)
            if data_species:
                evolution_chain_url = data_species.get("evolution_chain", {}).get("url")
                if evolution_chain_url:
                    evolution_chain = self.get_api(evolution_chain_url)
                    if evolution_chain and evolution_chain.get("chain"):
                        chain = evolution_chain.get("chain", {})
                        while chain:
                            if chain.get("species", {}).get("name") == self.name:
                                return bool(chain.get("evolves_to"))
                            chain = chain.get("evolves_to", [])[0] if chain.get("evolves_to") else None
        return False
                  
     
    def get_attribute(self, attribute, attribute_api, text):
        att = self.get_api(self.url)
        if att is not None:
            value = att.get(attribute_api)
            if value is not None:
                click.echo(f"{text}: {value}")
            else:
                click.echo(f"Failed to retrieve {attribute} for Pokemon {self.name}")
        else:
            click.echo(f"Failed to retrieve data for Pokemon {self.name}")
            
    def get_info(self):
        attributes_to_retrieve = [
            ("ID", "id", "ID"),
            ("Name", "name", "Name"),
            ("Height", "height", "Height"),
            ("Weight", "weight", "Weight")
        ]
    
        for attribute in attributes_to_retrieve:
            self.get_attribute(*attribute)

        info = self.get_api(self.url)
        if info is not None:
            species_url_info = self.get_api(self.url, "species")
            if species_url_info:
                species_url = species_url_info.get('url')
                before_evolve = self.get_species(species_url)
                click.echo("Before evolution: " + before_evolve)
                abilities = info.get("abilities")
                if abilities:
                    click.echo("Abilities:")
                    for ability in abilities:
                        ability_name = ability.get("ability", {}).get("name")
                        if ability_name:
                            click.echo(ability_name)
                        else:
                            click.echo("Failed to retrieve ability name")
                else:
                    click.echo(f"Failed to retrieve abilities for Pokemon {self.name}")
            else:
                click.echo(f"Failed to retrieve species information for Pokemon {self.name}")
        else:
            click.echo(f"Failed to retrieve data for Pokemon {self.name}")
            
        if self.has_next_evolution():
            click.echo("This Pokémon has an evolution.")
        else:
            click.echo("This Pokémon does not have an evolution.")

@click.command()
@click.argument("name")
def search_pokemon(name): 
    pokemon = PokeAPI(name)
    print(pokemon)
    pokemon.get_info()

if __name__ == "__main__":
    search_pokemon()
