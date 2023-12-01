import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import SearchView from "@/views/SearchView.vue";
import SearchCoursesView from "@/views/SearchCoursesView.vue";
import SearchDegreesView from "@/views/SearchDegreesView.vue";
import SearchProfessorsView from "@/views/SearchProfessorsView.vue";
import DegreeView from "@/views/DegreeView.vue";
import CourseView from "@/views/CourseView.vue";
import ProfessorView from "@/views/ProfessorView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/search",
      name: "search",
      component: SearchView,
    },
    {
      path: "/search/degrees",
      name: "degrees",
      component: SearchDegreesView,
    },
    {
      path: "/search/courses",
      name: "courses",
      component: SearchCoursesView,
    },
    {
      path: "/search/professors",
      name: "professors",
      component: SearchProfessorsView,
    },
    {
      path: "/degree/:id",
      name: "degree",
      component: DegreeView,
    },
    {
      path: "/course/:id",
      name: "course",
      component: CourseView,
    },
    {
      path: "/professor/:id",
      name: "professor",
      component: ProfessorView,
    },
  ],
});

export default router;
