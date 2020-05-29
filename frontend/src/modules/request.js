import axios from "axios";
import eventBus from "@/modules/event-bus";

let host =
  process.env.VUE_APP_API_HOST !== undefined
    ? process.env.VUE_APP_API_HOST
    : "";
let service = axios.create({
  baseURL: host + "/api",
  timeout: 5000,
});

service.interceptors.response.use(
  (response) => {
    if (response.data.status - 0 !== 200) {
      eventBus.$emit("global-snackbar-message", {
        message: response.data.message,
      });
      throw response.data.message;
    }
    return response.data;
  },
  (error) => {
    eventBus.$emit("global-snackbar-message", {
      message: "Network Error",
    });
    throw error;
  }
);

export default service;
