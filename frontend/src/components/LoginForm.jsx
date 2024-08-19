import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const LoginForm = ({ onLogin }) => {
  // create state variables to control the form
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // useNavigate is a hook that allows us to navigate to different pages
  const navigate = useNavigate();

  // if the session has expired, notify the user
  useEffect(() => {
    // check if the sessionExpired query parameter is present in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const sessionExpired = urlParams.get("sessionExpired");
    // if the session has expired, notify the user
    if (sessionExpired) {
      alert("Your session has expired. Please log in again.");
      // remove the sessionExpired query parameter from the URL to prevent a loop
      urlParams.delete("sessionExpired");
      window.history.replaceState(
        null,
        "",
        `${window.location.pathname}${
          urlParams.toString() ? "?" + urlParams.toString() : ""
        }`
      );
    }
  }, []);
  //copilot ^_^

  const handleSubmit = async (e) => {
    e.preventDefault(); // this is to prevent the default form submission
    try {
      // send a login request to the server and fetch the tokens
      const response = await axios.post("http://127.0.0.1:8080/api/token/", {
        username,
        password,
      });
      // check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // copilot ^_^

      // store the tokens in local storage as key-value pairs
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      // clear any previous errors
      setError("");
      // update the state
      onLogin();
      // redirect the user to the home page upon success
      navigate("/");
    } catch (error) {
      // Invalid credentials
      setError(
        error.response?.data?.detail || "Login Failed. Please try again."
      );
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="col-md-12 d-flex justify-content-center align-items-center flex-column mt-5">
        <h1>Welcome Back!</h1>
        <div className="form-group col-md-6">
          <label>Username: </label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group col-md-6">
          <label>Password: </label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <div className="alert alert-info mt-3">{error}</div>}
        <button type="submit" className="button mt-3" role="alert">
          Login
        </button>
      </div>
    </form>
  );
};
