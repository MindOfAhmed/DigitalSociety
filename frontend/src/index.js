import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
// add the Axios interceptors
import "./refreshToken.js";
// add the font awesome icons
import "./fontAwesome.js";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
