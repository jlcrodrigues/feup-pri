import type { CourseUnit, Degree, Professor } from "@/model/types";
import { defineStore } from "pinia";
import { ref, toRaw } from "vue";
import e from "@/assets/entities.json";

const entities = ref({} as any);

const loadEntities = async () => {
  entities.value = e;
};

const useEntityStore = defineStore("entity", () => {
  const apiUrl = import.meta.env.VITE_BACKEND_URI;
  loadEntities();

  const getEntity = (id: string) => {
    return entities.value[id];
  };

  const getEntities = () => {
    return entities;
  };

  const replaceDegreeEntities = async (degree: Degree) => {
    const response = await fetch(`${apiUrl}/degree/entities/${degree.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const documentEntities = (await response.json())[0];
    degree.description = replaceEntities(degree.description, documentEntities);
    degree.outings= replaceEntities(degree.outings, documentEntities);
    return degree;
  };

  const replaceCourseEntities = async (course: CourseUnit) => {
    const response = await fetch(`${apiUrl}/course/entities/${course.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const documentEntities = (await response.json())[0];
    course.objectives = replaceEntities(course.objectives, documentEntities);
    course.results = replaceEntities(course.results, documentEntities);
    course.workingMethod = replaceEntities(course.workingMethod, documentEntities);
    course.preRequirements = replaceEntities(course.preRequirements, documentEntities);
    course.program = replaceEntities(course.program, documentEntities);
    return course;
  };

  const replaceProfessorEntities = async (professor: Professor) => {
    const response = await fetch(`${apiUrl}/professor/entities/${professor.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const documentEntities = (await response.json())[0];
    professor.personalPresentation = replaceEntities(professor.personalPresentation, documentEntities);
    professor.fieldsOfInterest = replaceEntities(professor.fieldsOfInterest, documentEntities);
    return professor;
  };

  const replaceEntities = (text: string, entityList: Array<string>) => {
    if (text == null) return text;
    let replacedText = text;
    for (const entity of entityList) {
      replacedText = replacedText.replace(
        entity,
        `<a class="tw-underline" href="${entities.value[entity]}">${entity}</a>`
      );
    }
    return replacedText;
  };

  return {
    getEntity,
    getEntities,
    replaceDegreeEntities,
    replaceCourseEntities,
    replaceProfessorEntities,
  };
});

export default useEntityStore;
