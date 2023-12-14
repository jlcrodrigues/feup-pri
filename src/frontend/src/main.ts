import "./assets/main.css";
import "@mdi/font/css/materialdesignicons.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from 'vuetify/components';
import * as directives from "vuetify/directives";

import { createI18n } from "vue-i18n";
import { en } from "@/locale/en"
import { pt } from "@/locale/pt"

import App from "./App.vue";
import router from "./router";


const customTheme = {
  disable: true,
  dark: false,
  colors: {
    primary: "#8c2d19",
    secondary: "#2a3c24",
    backgroud: "#f1e0c5",
  },
};

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "customTheme",
    themes: {
      customTheme,
    },
  },
});

const i18n = createI18n({
  legacy: false,
  locale: "pt",
  fallbackLocale: "en",
  messages: {
    en: en,
    pt: pt,
  },
});

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(vuetify);
app.use(i18n)

app.mount("#app");
