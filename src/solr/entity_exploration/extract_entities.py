import spacy
import json
import functools
import wikipediaapi


# jq '[.[] | .entities] | reduce .[] as $elem ([];  $elem+.) | unique'


def clean_text(text):
    replacements = {
        "\n": " ",
        "\t": " ",
        "\r": " ",
        ".": " . ",
        ",": " , ",
        ";": " ; ",
        ":": " : ",
        "!": " ! ",
        "?": " ? ",
        "(": " ( ",
        ")": " ) ",
        "[": " [ ",
        "]": " ] ",
        "{": " { ",
        "}": " } ",
        "/": " / ",
        ">": " > ",
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    return text


def extract_entities(text, nlp, entities_dict):
    doc = nlp(text)
    entities = set()
    wiki = wikipediaapi.Wikipedia("Daniel Rodrigues", "pt")
    for ent in doc.ents:
        if ent.label_ == "MISC" or len(ent.text) <= 2:
            continue

        if ent.text in entities_dict:
            entities.add(ent.text)
            continue

        try:
            wiki_page = wiki.page(ent.text)
            if wiki_page.exists():
                entities_dict[ent.text] = wiki_page.fullurl
                entities.add(ent.text)
                continue
        except:
            pass

    return entities


def extract_entities_from_file(file_path, nlp, fields, entities_dict):
    with open(file_path, "r") as f:
        data = json.load(f)

    for entry in data:
        text = functools.reduce(
            lambda x, y: x if x else "" + " . " + y if y else "",
            [entry[field] for field in fields],
        )
        if text == "":
            continue

        text = clean_text(text)

        entities = extract_entities(text, nlp, entities_dict)
        entry["entities"] = list(entities)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def main():
    nlp = spacy.load("pt_core_news_md")
    entities_dict = dict()
    extract_entities_from_file(
        "../data/course_units_embeddings.json",
        nlp,
        ["objectives", "results", "program"],
        entities_dict,
    )
    extract_entities_from_file(
        "../data/degrees_embeddings.json",
        nlp,
        ["description", "outings"],
        entities_dict,
    )
    extract_entities_from_file(
        "../data/professors_embeddings.json",
        nlp,
        ["personalPresentation", "fieldsOfInterest"],
        entities_dict,
    )
    with open("entities.json", "w") as f:
        json.dump(entities_dict, f, indent=4)

    print("Entity extraction done.")


if __name__ == "__main__":
    main()
