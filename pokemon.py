#!/usr/bin/env python3
import requests
import random
import json

# Path to the JSON file
filename = '/home/ec2-user/Pokemon_API/data.json'


def get_pokemon_count_and_results():
    # URL to the Pokémon API
    url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"

    # GET request.
    response = requests.get(url)
    data = response.json()

    # Extract count and results from the response.
    count_of_pokemons = data['count']
    results = data['results']

    return response.status_code, count_of_pokemons, results


def get_pokemon_from_api(pokemon_name):
    # URL to the Pokémon API (Get Pokémon by id)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    # GET request.
    response = requests.get(url)
    pokemon = response.json()
    return response.status_code, pokemon


def extract_pokemon_details(pokemon_name):
    response_status_code, pokemon = get_pokemon_from_api(pokemon_name)
    filtered_pokemon = {
        "id": pokemon["id"],
        "name": pokemon["name"],
        "weight": pokemon["weight"],
        "image": pokemon["sprites"]["front_default"]
    }
    if response_status_code != 200:
        print("Failed to retrieve data. Status code:", response_status_code)
        return
    else:
        return filtered_pokemon


def read_data_from_json_file():
    try:
        # Open the file and read the JSON data
        with open('data.json', 'r') as file:
            data = json.load(file)
            return data  # Move the return statement inside the try block
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return {}  # Return an empty dictionary or appropriate structure when the file is not found
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
        return {}  # Return an empty dictionary or appropriate structure in case of JSON errors


def write_pokemon_from_api_to_json_file(pokemon_name):
    data = read_data_from_json_file()
    pokemon_filtered_details = extract_pokemon_details(pokemon_name)

    # Append the new Pokémon to the list of Pokémon
    data['pokemons'].append(pokemon_filtered_details)

    # Save Pokémon to DB
    # Write the updated data back to the file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def check_if_pokemon_exist_in_db(pokemon_name):
    data = read_data_from_json_file()
    if len(data['pokemons']) > 0:
        for pokemon in data['pokemons']:
            if pokemon['name'] == pokemon_name:
                print(f"Pokemon Details: ")
                print(f"Pokemon ID: {pokemon['id']}")
                print(f"Pokemon Name: {pokemon['name']}")
                print(f"Pokemon Weight: {pokemon['weight']}")
                print(f"Pokemon Image: {pokemon['image']}")
                return True
    return False


def download_pokemon_list():
    response_status_code, pokemons_count, pokemon_results = get_pokemon_count_and_results()
    # Check if the request was successful.
    if response_status_code != 200:
        print("Failed to retrieve data. Status code:", response_status_code)
        return
    else:
        # List of random Pokémon (indexes)
        random_api_pokemons_indexes = [random.randint(0, int(pokemons_count)) for _ in range(4)]
        # Choose random Pokémon (index)
        random_pokemon_index = random.choice(random_api_pokemons_indexes)
        # Get chosen pokemon name
        pokemon_name = pokemon_results[random_pokemon_index]["name"]

        # Check by name if the chosen Pokémon exist in db
        # If chosen Pokémon exist in db then print its details.
        # If chosen Pokémon doesn't exist in db then get its detail's from the api and write to the db.
        if not check_if_pokemon_exist_in_db(pokemon_name):
            write_pokemon_from_api_to_json_file(pokemon_name)


while True:
    choice = input("Would like to draw a Pokémon? (Y/N) ")
    choice = choice.lower()

    if choice == "y":
        print("Start downloading pokemon list...")
        download_pokemon_list()
    elif choice == "n":
        print("See you around!")
        break
    else:
        print("Invalid choice option. Please try again.")
