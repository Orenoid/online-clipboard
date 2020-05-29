import axios from "axios";
import eventBus from "@/modules/event-bus";

let service = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
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
