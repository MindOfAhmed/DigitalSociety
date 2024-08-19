import { useNavigate } from "react-router-dom";

export const ProtectedRoute = ({ children }) => {
  // check if the user is authenticated
  const isAutheticated = !!localStorage.getItem("access_token");
  const navigate = useNavigate(); // useNavigate is a hook that allows us to navigate to different pages
  // redirect the user to the login page if they are not authenticated
  if (!isAutheticated) {
    return navigate("/login/");
  }
  // render the component if the user is authenticated
  return children;
};
