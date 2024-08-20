import { useState, useEffect } from "react";
import axios from "axios";
import Col from "react-bootstrap/Col";
import Nav from "react-bootstrap/Nav";
import Row from "react-bootstrap/Row";
import Tab from "react-bootstrap/Tab";
// import Tabs from "react-bootstrap/Tabs";
import { Passport } from "./Passport";
import { DrivingLicense } from "./DrivingLicense";
import { Address } from "./Address";
import { Property } from "./Property";
import { Vehicle } from "./Vehicle";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare } from "@fortawesome/free-solid-svg-icons";
import { ProfileModal } from "./ProfileModal";

export const Profile = () => {
  // define state variable that will store the user's documetns
  const [userDocuments, setUserDocuments] = useState({
    addresses: [],
    properties: [],
    vehicles: [],
    license: null,
    passport: null,
    citizen: null,
  });
  // define state variable that will keep track of the active tab key
  const [activeKey, setActiveKey] = useState("Passport");
  // define state variable that will control the visibility of the modal
  const [showModal, setShowModal] = useState(false);
  // define handlers for showing and hiding the modal
  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  // derive the state variable that will store the user's documents
  const addresses = userDocuments?.addresses;
  const properties = userDocuments?.properties;
  const vehicles = userDocuments?.vehicles;
  const license = userDocuments?.license;
  const passport = userDocuments?.passport;
  const citizen = userDocuments?.citizen;

  // define the handler for submitting the form
  const handleSubmit = async (
    username,
    profilePicture,
    currentPassword,
    newPassword
  ) => {
    // make an API call to update the user's profile
    try {
      // create a FormData object to send the form data
      const formData = new FormData();
      if (username && username !== citizen.user.username) {
        formData.append("username", username);
      }
      if (profilePicture) {
        formData.append("profile_picture", profilePicture);
      }
      if (profilePicture || (username && username !== citizen.user.username)) {
        const response = await axios.post(
          "http://127.0.0.1:8080/api/user_profile/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        if (!response || !response.data) {
          throw new Error("Invalid server response");
        }
      }
      // if the password fields are not empty, update the password
      if (currentPassword && newPassword) {
        const passwordResponse = await axios.post(
          "http://127.0.0.1:8080/api/change_password/",
          {
            current_password: currentPassword,
            new_password: newPassword,
          }
        );
        if (!passwordResponse || !passwordResponse.data) {
          throw new Error("Invalid server response");
        }
      }
      handleCloseModal();
    } catch (error) {
      if (error.response && error.response.data) {
        // handle validation errors
        const usernameErrorMsg = error.response.data.username;
        if (usernameErrorMsg) {
          alert(usernameErrorMsg); // display error to the user
        }
        const passwordErrorMsg = error.response.data.current_password;
        if (passwordErrorMsg) {
          alert(passwordErrorMsg); // display error to the user
        }
      } else {
        console.error("Failed to update user profile:", error);
      }
    }
  };
  // on mount, load the user documents
  useEffect(() => {
    (async () => {
      try {
        // make an API call to fetch the user's documents
        const response = await axios.get(
          "http://127.0.0.1:8080/api/user_documents/"
        );
        if (!response || !response.data) {
          setUserDocuments([]);
          return;
        }
        // set the user documents in the state
        setUserDocuments(response.data);
      } catch (error) {
        console.error("Failed to fetch user documents:", error);
      }
    })();
  }, []);

  return (
    // place each document in a separate tab
    // <Tabs
    //   defaultActiveKey="Passport"
    //   id="profile-tab"
    //   className="d-flex justify-content-center"
    // >
    //   <Tab eventKey="Profile" title="Profile">
    //     {/* the citizen's profile picture */}
    //     <div className="row d-flex justify-content-center">
    //       <div className="col-md-8 mt-5">
    //         {citizen && citizen.picture && (
    //           <img
    //             src={citizen.picture}
    //             alt="profile"
    //             className="rounded mx-auto d-block"
    //             style={{ width: "300px", height: "300px" }}
    //           />
    //         )}
    //         <div className="d-flex justify-content-center">
    //           <button className="button mt-3">
    //             <FontAwesomeIcon icon={faPenToSquare} /> Edit Profile
    //           </button>
    //         </div>
    //       </div>
    //     </div>
    //   </Tab>
    //   <Tab eventKey="Passport" title="Passport">
    //     <div className="row d-flex justify-content-center">
    //       <div className="col-md-8 mt-5">
    //         {passport && (
    //           <Passport
    //             citizen={citizen}
    //             info={passport}
    //             picture={passport.picture}
    //           />
    //         )}
    //       </div>
    //     </div>
    //   </Tab>
    //   <Tab eventKey="Driver's License" title="Driver's License">
    //     <div className="row d-flex justify-content-center mt-5">
    //       <div className="col-md-8">
    //         {license && (
    //           <DrivingLicense
    //             citizen={citizen}
    //             info={license}
    //             picture={license.picture}
    //           />
    //         )}
    //       </div>
    //     </div>
    //   </Tab>
    //   <Tab eventKey="Addresses" title="Address(es)">
    //     <div className="row d-flex justify-content-center mt-5">
    //       <div className="col-md-8">
    //         {addresses &&
    //           addresses.map((address, index) => (
    //             <Address key={index} citizen={citizen} info={address} />
    //           ))}
    //       </div>
    //     </div>
    //   </Tab>
    //   <Tab eventKey="Properties" title="Properties">
    //     <div className="row d-flex justify-content-center mt-5">
    //       <div className="col-md-8">
    //         {properties &&
    //           properties.map((property, index) => (
    //             <Property key={index} citizen={citizen} info={property} />
    //           ))}
    //       </div>
    //     </div>
    //   </Tab>
    //   <Tab eventKey="Vehicles" title="Vehicle(s)">
    //     <div className="row d-flex justify-content-center mt-5">
    //       <div className="col-md-8">
    //         {vehicles &&
    //           vehicles.map((vehicle, index) => (
    //             <Vehicle key={index} citizen={citizen} info={vehicle} />
    //           ))}
    //       </div>
    //     </div>
    //   </Tab>
    // </Tabs>

    <>
      {/*  place each document in a separate tab */}
      <Tab.Container
        id="profile-tab"
        defaultActiveKey="Passport"
        activeKey={activeKey}
        onSelect={(key) => setActiveKey(key)}
      >
        <Row>
          <Col sm={3}>
            {/* the citizen's profile picture */}
            <div className="row">
              <div className="com-md-4">
                {citizen && citizen.picture && (
                  <img
                    src={citizen.picture}
                    alt="profile"
                    className="profile_picture m-3"
                  />
                )}
                <div>
                  <button
                    className="button mb-3 mx-4"
                    onClick={handleShowModal}
                  >
                    <FontAwesomeIcon icon={faPenToSquare} /> Edit Profile
                  </button>
                </div>
              </div>
            </div>
            {/* the navigation links for the tabs */}
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link
                  eventKey="Passport"
                  disabled={!passport}
                  className={activeKey === "Passport" ? "active_tab" : ""}
                >
                  Passport
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="Driver's License"
                  disabled={!license}
                  className={
                    activeKey === "Driver's License" ? "active_tab" : ""
                  }
                >
                  Driver's License
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="Addresses"
                  disabled={!addresses}
                  className={activeKey === "Addresses" ? "active_tab" : ""}
                >
                  Address(es)
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="Properties"
                  disabled={!properties}
                  className={activeKey === "Properties" ? "active_tab" : ""}
                >
                  Properties
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link
                  eventKey="Vehicles"
                  disabled={!vehicles}
                  className={activeKey === "Vehicles" ? "active_tab" : ""}
                >
                  Vehicle(s)
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            {/* the corresponding content for each tab */}
            <Tab.Content className="d-flex justify-content-center">
              <Tab.Pane eventKey="Passport" className="col-md-8 mt-5">
                {passport && (
                  <Passport
                    citizen={citizen}
                    info={passport}
                    picture={passport.picture}
                  />
                )}
              </Tab.Pane>
              <Tab.Pane eventKey="Driver's License" className="col-md-8 mt-5">
                {license && (
                  <DrivingLicense
                    citizen={citizen}
                    info={license}
                    picture={license.picture}
                  />
                )}
              </Tab.Pane>
              <Tab.Pane eventKey="Addresses" className="col-md-8 mt-5">
                {addresses &&
                  addresses.map((address, index) => (
                    <Address key={index} citizen={citizen} info={address} />
                  ))}
              </Tab.Pane>
              <Tab.Pane eventKey="Properties" className="col-md-8 mt-5">
                {properties &&
                  properties.map((property, index) => (
                    <Property key={index} citizen={citizen} info={property} />
                  ))}
              </Tab.Pane>
              <Tab.Pane eventKey="Vehicles" className="col-md-8 mt-5">
                {vehicles &&
                  vehicles.map((vehicle, index) => (
                    <Vehicle key={index} citizen={citizen} info={vehicle} />
                  ))}
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
      {/* the modal for editing the profile */}
      <ProfileModal
        show={showModal}
        handleClose={handleCloseModal}
        citizen={citizen}
        onSubmit={handleSubmit}
      />
    </>
  );
};
