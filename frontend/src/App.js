// css and bootstrap
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
// hooks
import { useEffect, useState } from "react";
// axios
import axios from "axios";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
// components
import { Home } from "./components/Home";
import { Profile } from "./components/Profile";
import { TownHall } from "./components/TownHall";
import { Requests } from "./components/Requests";
import { Services } from "./components/Services";
import { NotFound } from "./components/NotFound";
import { Nav } from "./components/Nav";
import { Footer } from "./components/Footer";
import { LoginForm } from "./components/LoginForm";
import { CitizenValidationForm } from "./components/CitizenValidationForm";
import { AddressValidationForm } from "./components/AddressValidationForm";
import { PassportValidationForm } from "./components/PassportValidationForm";
import { DriversLicenseValidationForm } from "./components/DriversLicenseValidationForm";
import { AddressRegistrationForm } from "./components/AddressRegistrationForm";
import { PropertyRegistrationForm } from "./components/PropertyRegistrationForm";
import { VehicleRegistrationForm } from "./components/VehicleRegistrationForm";
import { Success } from "./components/Success";
import { getUserGroups } from "./getUserGroups";
import { Forum } from "./components/Forum";
import { PostPage } from "./components/PostPage";

function App() {
  // the following states and handlers have been lifted up from the nav component
  const [isLoggedIn, setIsLoggedIn] = useState(false); // this will check if the user is logged in or not
  const [notifications, setNotifications] = useState(null); // this will store the notifications after login
  const [userGroups, setUserGroups] = useState([]); // this will store the user groups the user is in after login

  useEffect(() => {
    // check if the user is logged in
    const token = localStorage.getItem("access_token");
    if (token) {
      // set logged in state
      setIsLoggedIn(!!token);
      // make an API call to fetch the notifications
      (async () => {
        try {
          const response = await axios.get(
            "http://127.0.0.1:8080/api/get_notifications/"
          );
          // store the notifications in state
          setNotifications(response.data);
        } catch (error) {
          console.error(error);
        }
      })();
      // fetch the user's user groups from the backend
      (async () => {
        const groups = await getUserGroups();
        // store the groups in state
        setUserGroups(groups);
      })();
    }
  }, [isLoggedIn]);

  const handleLogout = () => {
    // remove the token from local storage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("refresh_attempt_failed");

    // update the logged in state
    setIsLoggedIn(false);
  };

  // this handler will be passed in as a prop for the login form
  const handleLogin = () => {
    // update the state and the user data
    setIsLoggedIn(true);
  };

  return (
    /* Router is the parent component that wraps all the routes and allows routing functionality in the app. 
    it listens to the url changes and renders the correct component  */
    <Router>
      <div className="container-fluid">
        <div className="content col-md-12">
          <Nav
            isLoggedIn={isLoggedIn}
            onLogout={handleLogout}
            notifications={notifications}
            userGroups={userGroups}
          />
          {/* Routes is used to group Route components and ensure that only one route is rendered at a time */}
          <Routes>
            {/* route is used to define the mapping between the URL path and the component that should be rendered 
            when the path matches. Note: exact is used to match the path exactly */}
            <Route path="/" element={<Home />} exact />
            <Route path="/profile" element={<Profile />} />
            <Route
              path="/townhall"
              element={<TownHall userGroups={userGroups} />}
            />
            <Route path="/townhall/forum/:forumId" element={<Forum />} />
            <Route
              path="/townhall/forum/:forumId/post/:postId"
              element={<PostPage />}
            />
            <Route path="/requests" element={<Requests />} />
            <Route path="/services" element={<Services />} />
            <Route
              path="/services/passport_citizen"
              element={
                <CitizenValidationForm next="/services/passport_address" />
              }
            />
            <Route
              path="/services/passport_address"
              element={<AddressValidationForm next="/services/passport" />}
            />
            <Route
              path="/services/passport"
              element={<PassportValidationForm />}
            />
            <Route
              path="/services/DriversLicense_citizen"
              element={
                <CitizenValidationForm next="/services/DriversLicense_address" />
              }
            />
            <Route
              path="/services/DriversLicense_address"
              element={
                <AddressValidationForm next="/services/DriversLicense" />
              }
            />
            <Route
              path="/services/DriversLicense"
              element={<DriversLicenseValidationForm />}
            />
            <Route
              path="/services/address"
              element={<AddressRegistrationForm />}
            />
            <Route
              path="/services/address_citizen"
              element={<CitizenValidationForm next="/services/address" />}
            />
            <Route
              path="/services/property_citizen"
              element={<CitizenValidationForm next="/services/property" />}
            />
            <Route
              path="/services/property"
              element={<PropertyRegistrationForm />}
            />
            <Route
              path="/services/vehicle_citizen"
              element={<CitizenValidationForm next="/services/vehicle" />}
            />
            <Route
              path="/services/vehicle"
              element={<VehicleRegistrationForm />}
            />
            <Route
              path="/login/"
              element={<LoginForm onLogin={handleLogin} />}
            />
            <Route path="/success" element={<Success />} />
            {/* this route will be rendered when no other route matches the URL path */}
            <Route path="*" element={<NotFound />} />
          </Routes>
          <Footer />
        </div>
      </div>
    </Router>
  );
}

export default App;
