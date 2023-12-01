import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import SearchView from "@/views/SearchView.vue";
import SearchCoursesView from "@/views/SearchCoursesView.vue";
import SearchDegreesView from "@/views/SearchDegreesView.vue";
import DegreeView from "@/views/DegreeView.vue";

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
      path: "/degree",
      name: "degree",
      component: DegreeView,
    },
  ],
});

export default router;
