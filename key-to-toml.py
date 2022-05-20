import toml

output_file = ".streamlit/secrets.toml"

def convert_service_account_to_secret():
    print("Converting service account json file to toml file...")
    with open("./firebase/firebase_service_account.json") as json_file:
        json_text = json_file.read()

    config = {"serviceAccountKey": json_text}
    toml_config = toml.dumps(config)

    with open(output_file, "a") as target:
        target.write(toml_config)

    print("Done!")

def convert_app_config_to_secret():
    print("Converting app config json file to toml file...")

    with open("./firebase/firebase_app_config.json") as json_file:
        json_text = json_file.read()

    config = {"appConfigKey": json_text}
    toml_config = toml.dumps(config)

    with open(output_file, "a") as target:
        target.write(toml_config)
    
    print("Done!")
    
if __name__ == "__main__":
    convert_service_account_to_secret()
    convert_app_config_to_secret()
