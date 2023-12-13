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

  const response = await fetch(`${apiUrl}/search/degrees?text=${params.text}${(queryParams != '&' ? queryParams : '')}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchCourses = async (params: any) => {
    let queryParams = "&"
    if (params.text == null) params.text = ""
    if (params.language) {
      for (const type of params.language) {
        queryParams += `&language=${type}`
      }
    }

    const response = await fetch(`${apiUrl}/search/courses?text=${params.text}${(queryParams != '&' ? queryParams : '')}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchProfessors = async (params: any) => {
    let queryParams = "&"
    if (params.text == null) params.text = ""
    if (params.status) {
      for (const type of params.status) {
        queryParams += `&status=${type}`
      }
    }
    if (params.rank) {
      for (const type of params.rank) {
        queryParams += `&rank=${type}`
      }
    }

    const response = await fetch(`${apiUrl}/search/professors?text=${params.text}${(queryParams != '&' ? queryParams : '')}`, {
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
