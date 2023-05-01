"""Sort the glossary terms in alphabetical order reading from a YAML file."""
import yaml


def sort_dicts_by_key(dicts: list[dict], key: str, reverse: bool=False):
    """
    Sort a list of dictionaries by a key
    :param dicts: list of dictionaries
    :param key: key to sort by
    :param reverse: whether to sort in reverse order
    :return: sorted list of dictionaries
    """
    return sorted(dicts, key=lambda x: x[key], reverse=reverse)


def read_glossary(glossary_file: str ='Glossary.yaml'):
    """
    Read the glossary from a YAML file
    :param glossary_file: YAML file containing the glossary
    :return: glossary
    """
    with open(glossary_file, 'r', encoding='utf-8') as file:
        glossary = yaml.load(file, Loader=yaml.FullLoader)
    return glossary


def write_glossary(glossary: list[dict], glossary_file: str):
    """
    Write the glossary to a YAML file
    :param glossary: glossary
    :param glossary_file: YAML file to write the glossary to
    :return: None
    """
    with open(glossary_file, 'w', encoding='utf-8') as file:
        yaml.dump(glossary, file, allow_unicode=True)


def sort_glossary(language: str='en'):
    """
    Sort the glossary terms in alphabetical order reading from a YAML file
    and write the sorted glossary to a new YAML file
    :param language: language of the glossary
    :return: None
    """
    # read the glossary from a YAML file
    glossary = read_glossary('Glossary.yaml')

    # sort the glossary terms in alphabetical order based on the language
    if language == 'en':
        sorted_glossary = sort_dicts_by_key(glossary, 'english')
    elif language == 'fa':
        sorted_glossary = sort_dicts_by_key(glossary, 'persian')
    else:
        raise ValueError('language should be either "en" or "fa"')

    # write the sorted glossary to a new YAML file
    output_filename = f"Glossary_sorted_{language}.yaml"
    write_glossary(sorted_glossary, output_filename)


if __name__ == '__main__':
    sort_glossary(language='en')
    sort_glossary(language='fa')
