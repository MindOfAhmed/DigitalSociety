import axios from "axios";
/*
 *This interceptor will run before each request
 * if there's an access token in local storage it will be attached to the request headers
 */

// refresh the access token
const refreshToken = async () => {
  const refresh_token = localStorage.getItem("refresh_token");
  // check if a refresh attempt has already failed
  if (refresh_token && !localStorage.getItem("refresh_attempt_failed")) {
    // send a request to the refresh token endpoint
    try {
      const response = await axios.post(
        "http://127.0.0.1:8080/api/token/refresh/",
        {
          refresh: refresh_token,
        }
      );
      if (response && response.data) {
        // store the new access token in local storage
        localStorage.setItem("access_token", response.data.access);
        // remove the refresh attempt failed flag
        localStorage.removeItem("refresh_attempt_failed");
      } else {
        throw new Error("Invalid server response");
      }
    } catch (error) {
      // set the refresh attempt failed flag
      localStorage.setItem("refresh_attempt_failed", "true");
      console.error("Refresh token failed", error);
      // throw the error to be caught by the calling code
      throw error;
    }
  } else {
    throw new Error("Refresh token not available or refresh already attempted");
  }
};

// setupAxiosInterceptors.js
const setupAxiosInterceptors = () => {
  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      if (
        error.response.status === 401 && // check if the error status is unauthorized
        !originalRequest._retry && // check if this is not a retry request
        !originalRequest.url.includes("/api/token/refresh/") && // check if the request is not a refresh token request
        !localStorage.getItem("refresh_attempt_failed") // check if a refresh attempt has not already failed
      ) {
        // set the retry flag
        originalRequest._retry = true;
        // attempt to refresh the token
        try {
          await refreshToken();
          originalRequest.headers["Authorization"] =
            "Bearer " + localStorage.getItem("access_token");
          return axios(originalRequest);
        } catch (e) {
          // redirect the user to the login page if the refresh attempt fails
          window.location.href = `/login?sessionExpired=true`;
          console.error("Refresh token failed", e);
          return Promise.reject(e);
        }
      }
      return Promise.reject(error);
    }
  );

  // add the Authorization header to the request
  axios.interceptors.request.use(
    (config) => {
      // get the access token from local storage
      const token = localStorage.getItem("access_token");
      // check if the access token is available and add it to the request headers
      if (token) {
        config.headers["Authorization"] = "Bearer " + token;
      }
      // get the CSRF token from the meta tag in index.html
      const csrfToken = document
        .querySelector('meta[name="csrf-token"]')
        .getAttribute("content");
      // check if the CSRF token is available and add it to the request headers
      if (csrfToken) {
        config.headers["X-CSRFToken"] = csrfToken;
      }

      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

// initialize the Axios interceptors
setupAxiosInterceptors();

export default setupAxiosInterceptors;
// copilot ^_^
