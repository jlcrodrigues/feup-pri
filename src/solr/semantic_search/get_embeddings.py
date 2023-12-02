import sys
import json
from sentence_transformers import SentenceTransformer
import argparse

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def arg_parser():
    parser = argparse.ArgumentParser(description="Generate embeddings for course units")
    parser.add_argument(
        "--inputs",
        "-i",
        nargs="+",
        help="Input JSON file",
        default=[
            "../data/course_units.json",
            "../data/degrees.json",
            "../data/professors.json",
        ],
    )
    return parser.parse_args()


def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()


def get_embeddings_degrees(data):
    for document in data:
        name = document.get("name", "")
        description = document.get("description", "")
        outings = document.get("outings", "")
        typeOfCourse = document.get("typeOfCourse", "")
        duration = document.get("duration", "")
        combined = f"{name} {description} {outings} {typeOfCourse} {duration}"
        document["embedding"] = get_embedding(combined)


def get_embeddings_course_units(data):
    for document in data:
        name = document.get("name", "")
        language = document.get("language", "")
        ects = document.get("ects", 0)
        objectives = document.get("objectives", "")
        results = document.get("results", "")
        workingMethod = document.get("workingMethod", "")
        program = document.get("program", "")
        evaluationType = document.get("evaluationType", "")
        combined = f"{name} {language} {ects} {objectives} {results} {workingMethod} {program} {evaluationType}"
        document["embedding"] = get_embedding(combined)


def get_embeddings_professors(data):
    for document in data:
        name = document.get("name", "")
        institutionalWebsite = document.get("institutionalWebsite", "")
        rank = document.get("rank", "")
        personalPresentation = document.get("personalPresentation", "")
        fieldsOfInterest = document.get("fieldsOfInterest", "")
        combined = f"{name} {institutionalWebsite} {rank} {personalPresentation} {fieldsOfInterest}"
        document["embedding"] = get_embedding(combined)


def get_embeddings_from_file(input_file, data):
    match input_file.split("/")[-1]:
        case "course_units.json":
            get_embeddings_course_units(data)
        case "degrees.json":
            get_embeddings_degrees(data)
        case "professors.json":
            get_embeddings_professors(data)
        case _:
            raise ValueError("Invalid input file")


def main(input_files):
    for input_file in input_files:
        with open(input_file, "r") as f:
            data = json.load(f)

        get_embeddings_from_file(input_file, data)

        output_file = input_file.replace(".json", "_embeddings.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    print("Done!")


if __name__ == "__main__":
    args = arg_parser()
    main(args.inputs)
