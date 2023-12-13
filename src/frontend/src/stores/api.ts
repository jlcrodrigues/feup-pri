import { defineStore } from "pinia";
import { ref } from "vue";

const useApiStore = defineStore("search", () => {
  const apiUrl = import.meta.env.VITE_BACKEND_URI;
  console.log(apiUrl);

  const searchDegrees = async (params: any) => {
    let queryParams = "&"
    if (params.text == null) params.text = ""
    if (params.typeOfCourse) {
      for (const type of params.typeOfCourse) {
        queryParams += `&typeOfCourse=${type}`
      }
    }

  const response = await fetch(`${apiUrl}/search/degrees?text=${params.text}${(queryParams != '?' ? queryParams : '')}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchCourses = async (text: String) => {
    if (text.length === 0) {
      return [];
    }
    const response = await fetch(`${apiUrl}/search/courses?text=${text}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchProfessors = async (text: String) => {
    if (text.length === 0) {
      return [];
    }
    const response = await fetch(`${apiUrl}/search/professors?text=${text}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const getDegree = async (id: String) => {
    const response = await fetch(`${apiUrl}/degree/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return await response.json();
  };

  const getCourse = async (id: String) => {
    const response = await fetch(`${apiUrl}/course/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return await response.json();
  };

  const getProfessor = async (id: String) => {
    const response = await fetch(`${apiUrl}/professor/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return await response.json();
  };

  return {
    searchDegrees,
    searchCourses,
    searchProfessors,
    getDegree,
    getCourse,
    getProfessor,
  };
});

export default useApiStore;
