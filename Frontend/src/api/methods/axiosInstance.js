import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL;
// const BASE_URL = "http://127.0.0.1:8000/";

export const normalInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const accessInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const getAccessToken = () => localStorage.getItem("token");
// const getRefreshToken = () => localStorage.getItem("refreshToken");

normalInstance.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

normalInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = "fffg";

        if (!refreshToken) {
          // console.warn("Refresh token missing, logging out.");
          handleLogout();
          return Promise.reject(error);
        }

        const response = await accessInstance.post("/access/user/details/", {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem("accessToken", newAccessToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return normalInstance(originalRequest);
      } catch (refreshError) {
        // console.error("Failed to refresh token:", refreshError);

        if (
          refreshError.response &&
          refreshError.response.data.code === "token_not_valid"
        ) {
          // console.warn("Refresh token is invalid or expired, logging out.");
          handleLogout();
        }

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

const handleLogout = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  window.dispatchEvent(new Event("tokenChange"));
  window.location.href = "/";
};

export const handleError = (error) => {
  const errorMessage =
    error.response?.data?.data?.detail || error.response?.data?.data?.error;

  console.error("❌ API Error ❌: ", errorMessage);

  throw error;
};
