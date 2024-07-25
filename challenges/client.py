import requests
import json
from hash_functions import sha256_hash
from encrypt_functions import rsa_encrypt

SERVER_URL = "http://34.163.219.17:3000"

def subscribe(name):
    payload = {"Name": name}
    response = requests.post(f"{SERVER_URL}/subscribe", json=payload)
    return response.json()

def get_info(address):
    response = requests.get(f"{SERVER_URL}/info/{address}")
    return response.json()

def get_hash_challenge(address):
    response = requests.get(f"{SERVER_URL}/challenge/hash/{address}")
    return response.json()
def submit_hash_challenge(address, challenge_id, hash_solution):
    payload = {
        "hash": hash_solution
    }
    response = requests.post(
        f"{SERVER_URL}/challenge/hash/{address}/{challenge_id}",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Submit Hash Challenge Response: {response.text}") 
    response.raise_for_status()
    return response.json()



def get_encrypt_challenge(address):
    response = requests.get(f"{SERVER_URL}/challenge/encrypt/{address}") # Afficher la réponse brute
    return response.json()

def submit_encrypt_challenge(address, challenge_id, encrypted_solution):
    payload = {
        "ciphertext": encrypted_solution.hex()
    }
    response = requests.post(
        f"{SERVER_URL}/challenge/encrypt/{address}/{challenge_id}",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Submit Encrypt Challenge Response: {response.text}")  
    response.raise_for_status()
    return response.json()



def main():
    try:
        # Inscription et récupération de l'adresse
        name = "Louis"
        #subscription = subscribe(name)
        #address = subscription["Address"]
        address = "0x0000000000000000000000000000000000000000"
        print(f"Subscribed with address: {address}")

        # Test de récupération des informations
        info = get_info(address)
        print(f"Info: {info}")

        # Récupération d'un défi de hachage
        hash_challenge = get_hash_challenge(address)
        print(f"Hash Challenge: {hash_challenge}")

        if "sentence" in hash_challenge and "challenge_id" in hash_challenge:
            sentence = hash_challenge["sentence"]
            challenge_id = hash_challenge["challenge_id"]
            hash_solution = sha256_hash(sentence)
            print(f"Hash Solution: {hash_solution}")

            # Soumission du défi de hachage
            result = submit_hash_challenge(address, challenge_id, hash_solution)
            print("Hash Challenge Result:", result)
        else:
            print("Invalid hash challenge format")

        # Récupération d'un défi de chiffrement
        encrypt_challenge = get_encrypt_challenge(address)
        print(f"Encrypt Challenge: {encrypt_challenge}")

        if "sentence" in encrypt_challenge and "challenge_id" in encrypt_challenge and "public_key" in encrypt_challenge:
            sentence = encrypt_challenge["sentence"]
            challenge_id = encrypt_challenge["challenge_id"]
            public_key = encrypt_challenge["public_key"]
            encrypted_solution = rsa_encrypt(public_key, sentence)
            print(f"Encrypted Solution: {encrypted_solution.hex()}")

            # Soumission du défi de chiffrement
            result = submit_encrypt_challenge(address, challenge_id, encrypted_solution)
            print("Encrypt Challenge Result:", result)
        else:
            print("Invalid encrypt challenge format")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

