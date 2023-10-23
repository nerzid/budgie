import yaml
class ActionParser:
    @staticmethod
    def parse(file_path: str):
        with open(file_path, 'r') as file:
            parsed_file = yaml.safe_load(file)

