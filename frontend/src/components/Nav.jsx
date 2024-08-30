import { Link } from "react-router-dom";
import { useState } from "react";
import { faBell } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export const Nav = ({ isLoggedIn, onLogout, notifications, userGroups }) => {
  // define state variable that will control the visibility of the notifications
  const [showNotifications, setShowNotifications] = useState(false);
  // this function will check if the user is in a specific group
  const isInGroup = (group) => userGroups.includes(group);

  return (
    <nav
      className="navbar navbar-expand-lg primary_color"
      aria-label="main app navigation"
    >
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
                <li className="nav-item mt-2 mx-1">
                  <FontAwesomeIcon
                    icon={faBell}
                    onClick={() => setShowNotifications((s) => !s)}
                    aria-label="notifications"
                  />
                  {notifications && notifications.length > 0 && (
                    <span className="badge mx-1">{notifications.length}</span>
                  )}
                  {showNotifications && (
                    <div className="dropdown-menu show">
                      {notifications && notifications.length > 0 ? (
                        notifications.map((notification, index) => (
                          <p key={index} className="dropdown-item">
                            {notification.message}
                          </p>
                        ))
                      ) : (
                        <span className="dropdown-item">No notifications</span>
                      )}
                    </div>
                  )}
                </li>
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
