import { defineStore } from "pinia";
import { ref, toRaw } from "vue";

const useApiStore = defineStore("search", () => {
  const apiUrl = import.meta.env.VITE_BACKEND_URI;

  const searchDegrees = async (params: any) => {
    let queryParams = ""
    if (params.text == null) params.text = ""
    if (params.typeOfCourse) {
      for (const type of params.typeOfCourse) {
        queryParams += `&typeOfCourse=${type}`
      }
    }
    if (params.sortKey) {
      queryParams += `&sortKey=${params.sortKey}`
    }
    if (params.sortOrder) {
      queryParams += `&sortOrder=${params.sortOrder}`
    }

  const response = await fetch(`${apiUrl}/search/degrees?text=${params.text}${(queryParams != '' ? queryParams : '')}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchCourses = async (params: any) => {
    let queryParams = ""
    if (params.text == null) params.text = ""
    if (params.language) {
      for (const type of params.language) {
        queryParams += `&language=${type}`
      }
    }
    if (params.sortKey) {
      queryParams += `&sortKey=${params.sortKey}`
    }
    if (params.sortOrder) {
      queryParams += `&sortOrder=${params.sortOrder}`
    }

    const response = await fetch(`${apiUrl}/search/courses?text=${params.text}${(queryParams != '' ? queryParams : '')}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    const responseJson = await response.json();
    return responseJson.results;
  };

  const searchProfessors = async (params: any) => {
    let queryParams = ""
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
    if (params.sortKey) {
      queryParams += `&sortKey=${params.sortKey}`
    }
    if (params.sortOrder) {
      queryParams += `&sortOrder=${params.sortOrder}`
    }

    const response = await fetch(`${apiUrl}/search/professors?text=${params.text}${(queryParams != '' ? queryParams : '')}`, {
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

  const getRelatedDegrees = async (id: String) => {
    const response = await fetch(`${apiUrl}/degree/related/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return toRaw(await response.json()).results;
  }

  const getRelatedCourses = async (id: String) => {
    const response = await fetch(`${apiUrl}/course/related/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return toRaw(await response.json()).results;
  }

  const getRelatedProfessors = async (id: String) => {
    const response = await fetch(`${apiUrl}/professor/related/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/text",
      },
    });
    return toRaw(await response.json()).results;
  }

  return {
    searchDegrees,
    searchCourses,
    searchProfessors,
    getDegree,
    getCourse,
    getProfessor,
    getRelatedDegrees,
    getRelatedCourses,
    getRelatedProfessors,
  };
});

export default useApiStore;
