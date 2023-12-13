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


def extract_entities(text, nlp):
    doc = nlp(text)
    entities = []
    wiki = wikipediaapi.Wikipedia('Daniel Rodrigues', 'pt')
    for ent in doc.ents:
        wiki_page = wiki.page(ent.text)
        wiki_url = wiki_page.fullurl if wiki_page.exists() else None
        entities.append({"text": ent.text, "label": ent.label_, "wiki_url": wiki_url})
        #if ent.label_ in ["PER", "ORG", "LOC"] and len(ent.text) > 2 and wiki_page.exists():
        #    entities.append(ent.text)



    return entities


def extract_entities_from_file(file_path, nlp, fields):
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

        entities = extract_entities(text, nlp)
        #entities = list(set(entities))
        entry["entities"] = entities

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def main():
    nlp = spacy.load("pt_core_news_md")
    # extract_entities_from_file(
    #    "../data/course_units_embeddings.json",
    #    nlp,
    #    ["objectives", "results", "program"],
    # )
    extract_entities_from_file(
        "../data/degrees_embeddings.json", nlp, ["description", "outings"]
    )
    # extract_entities_from_file(
    #    "../data/professors_embeddings.json",
    #    nlp,
    #    ["personalPresentation", "fieldsOfInterest"],
    # )
    print("Entity extraction done.")


if __name__ == "__main__":
    main()
