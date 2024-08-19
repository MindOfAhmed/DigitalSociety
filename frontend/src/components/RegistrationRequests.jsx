import axios from "axios";
import { useEffect, useState } from "react";
import { RegistrationRequest } from "./RegistrationRequest";
import { Property } from "./Property";
import { Vehicle } from "./Vehicle";
import { Address } from "./Address";

export const RegistrationRequests = () => {
  // define state variables to store the requests
  const [requests, setRequests] = useState([]);
  // define state variables to control the rejection reason form
  const [rejectionReason, setRejectionReason] = useState("");

  // on mount, fetch the requests
  useEffect(() => {
    (async () => {
      // this function will be exceuted immediately
      try {
        const response = await axios.get(
          "http://127.0.0.1:8080/api/registration_requests/"
        );
        // set the requests in the state
        setRequests(response.data);
      } catch (error) {
        console.error("Failed to fetch renewal requests:", error);
      }
    })();
  }, []);

  // define the function to handle the accept button
  const handleAccept = async (requestID) => {
    // send an API request to accept the registration request
    try {
      const response = await axios.post(
        `http://127.0.0.1:8080/api/accept_registration_request/${requestID}/`
      );
      // check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // filter out the accepted request from the requests array
      setRequests(requests.filter((request) => request.id !== requestID));
    } catch (error) {
      console.error("Failed to accept registration request:", error);
    }
  };
  // define the function to handle the reject button
  const handleReject = async (requestID) => {
    // send an API request to reject the registration request
    try {
      // send the rejection reason along with the request
      const response = await axios.post(
        `http://127.0.0.1:8080/api/reject_registration_request/${requestID}/`,
        { rejectionReason }
      );
      // check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // filter out the rejected request from the requests array
      setRequests(requests.filter((request) => request.id !== requestID));
    } catch (error) {
      console.error("Failed to reject registration request:", error);
    }
  };

  return (
    // map over the requests and render each request
    requests.map((request) =>
      request.request_type === "Property Registration" ? (
        <RegistrationRequest
          key={request.id}
          request={request}
          doc={
            <Property
              info={request.property_info}
              citizen={request.citizen_info}
            />
          }
          onAccept={handleAccept}
          onRejectionReason={rejectionReason}
          onsetRejectionReason={setRejectionReason}
          onReject={handleReject}
        />
      ) : request.request_type === "Vehicle Registration" ? (
        <RegistrationRequest
          key={request.id}
          request={request}
          doc={
            <Vehicle
              info={request.vehicle_info}
              citizen={request.citizen_info}
            />
          }
          onAccept={handleAccept}
          onRejectionReason={rejectionReason}
          onsetRejectionReason={setRejectionReason}
          onReject={handleReject}
        />
      ) : (
        <RegistrationRequest
          key={request.id}
          request={request}
          doc={
            <Address
              info={request.address_info}
              citizen={request.citizen_info}
            />
          }
          onAccept={handleAccept}
          onRejectionReason={rejectionReason}
          onsetRejectionReason={setRejectionReason}
          onReject={handleReject}
        />
      )
    )
  );
};
