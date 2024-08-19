import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { getUserGroups } from "../getUserGroups";

export const Nav = ({ isLoggedIn, onLogout, userData }) => {
  // create state variable that will store the user groups the user is in
  const [userGroups, setUserGroups] = useState([]);

  useEffect(() => {
    if (!isLoggedIn) {
      return;
    }
    // fetch the user groups from the backend
    const fetchGroups = async () => {
      const groups = await getUserGroups();
      // store the groups in state
      setUserGroups(groups);
    };
    fetchGroups();
  }, [isLoggedIn]); // copilot ^_^

  // this function will check if the user is in a specific group
  const isInGroup = (group) => userGroups.includes(group);

  return (
    <nav className="navbar navbar-expand-lg primary_color">
      <div className="container-fluid">
        <Link className="navbar-brand complimentary_color" to="/">
          Digital Society
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link className="nav-link complimentary_color" to="/townhall">
                Town Hall
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link complimentary_color" to="/services">
                Services
              </Link>
            </li>
            {/* conditionally render the login, logout, and profile links */}
            {isLoggedIn ? (
              <>
                {isInGroup("Inspectors") ? (
                  <li className="nav-item">
                    <Link
                      className="nav-link complimentary_color"
                      to="/requests"
                    >
                      Requests
                    </Link>
                  </li>
                ) : (
                  <li className="nav-item">
                    <Link
                      className="nav-link complimentary_color"
                      to="/profile"
                    >
                      Profile
                    </Link>
                  </li>
                )}
                <li className="nav-item">
                  <button
                    className="nav-link complimentary_color"
                    onClick={onLogout}
                  >
                    Logout
                  </button>
                </li>
                {/* {userData && userData.citizens && userData.citizens.picture && (
                  <li className="nav-item">
                    <img
                      src={userData.citizens.picture}
                      alt="profile"
                      className="rounded-circle mt-2"
                      height={40}
                      width={40}
                    />
                  </li>
                )} */}
              </>
            ) : (
              <li className="nav-item">
                <Link className="nav-link complimentary_color" to="/login/">
                  Login
                </Link>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};
