from glossary import Glossary


if __name__ == '__main__':
    enfa_glossary = Glossary('Glossary.yaml')
    glossary_sorted_en = enfa_glossary.sort_glossary('en')
    glossary_sorted_fa = enfa_glossary.sort_glossary('fa')
    enfa_glossary.write_glossary(glossary_sorted_en, 'Glossary_sorted_en.yaml')
    enfa_glossary.write_glossary(glossary_sorted_fa, 'Glossary_sorted_fa.yaml')
    print(f"Number of terms in the glossary: {len(enfa_glossary)}")
