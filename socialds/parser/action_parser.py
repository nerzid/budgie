import yaml

from repositories.repository import action_repository


def parse(file_path: str):
    with open(file_path, 'r') as file:
        parsed_file = yaml.safe_load(file)
    return parsed_file


if __name__ == '__main__':
    parsed_file = parse('../actions/actions.yml')
    for action in parsed_file['actions']:
        for sense in action['senses']:
            for variation in sense['variations']:
                for operation in variation['operations']:
                    pass