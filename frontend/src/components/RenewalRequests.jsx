import axios from "axios";
import { useEffect, useState } from "react";
import { RenewalRequest } from "./RenewalRequest";
import { Passport } from "./Passport";
import { DrivingLicense } from "./DrivingLicense";

export const RenewalRequests = () => {
  // define state variables to store the requests
  const [requests, setRequests] = useState([]);
  // define state variables to control the rejection reason form
  const [rejectionReason, setRejectionReason] = useState(""); // this state variable has been lifted up from the RenewalRequest component

  // on mount, fetch the requests
  useEffect(() => {
    (async () => {
      // this function will be exceuted immediately
      try {
        const response = await axios.get(
          "http://127.0.0.1:8080/api/renewal_requests/"
        );
        // set the requests in the state
        setRequests(response.data);
        console.log("response.data:", response.data);
      } catch (error) {
        console.error("Failed to fetch renewal requests:", error);
      }
    })();
  }, []);

  // define the function to handle the accept button
  const handleAccept = async (requestID) => {
    // send an API request to accept the renewal request
    try {
      const response = await axios.post(
        `http://127.0.0.1:8080/api/accept_renewal_request/${requestID}/`
      );
      // check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // filter out the accepted request from the requests array
      setRequests(requests.filter((request) => request.id !== requestID));
    } catch (error) {
      console.error("Failed to accept renewal request:", error);
    }
  };
  // define the function to handle the reject button
  const handleReject = async (requestID) => {
    // send an API request to reject the renewal request
    try {
      // send the rejection reason along with the request
      const response = await axios.post(
        `http://127.0.0.1:8080/api/reject_renewal_request/${requestID}/`,
        { rejectionReason }
      );
      // check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // filter out the rejected request from the requests array
      setRequests(requests.filter((request) => request.id !== requestID));
    } catch (error) {
      console.error("Failed to reject renewal request:", error);
    }
  };

  // this function will extend the expiry date of the documents by years
  const extendExpiryDate = (date, years) => {
    const result = new Date(date);
    result.setFullYear(result.getFullYear() + years);
    return result.toISOString().split("T")[0]; // Format YYYY-MM-DD
  };
  // copilot ^_^ helped me to write this code, i added years as arg

  return (
    // map over the requests and render them
    requests.map((request) =>
      request.request_type === "Passport" ? (
        <RenewalRequest
          key={request.id}
          request={request}
          oldDoc={
            request.passport_info && request.passport_info[0] ? (
              <Passport
                citizen={request.citizen_info}
                info={request.passport_info[0]}
                picture={request.passport_info[0].picture}
              />
            ) : null
          }
          newDoc={
            request.passport_info && request.passport_info[0] ? (
              <Passport
                citizen={request.citizen_info}
                info={{
                  ...request.passport_info[0],
                  issue_date: new Date().toISOString().split("T")[0],
                  expiry_date: extendExpiryDate(new Date(), 5),
                }}
                picture={request.picture}
              />
            ) : null
          }
          onAccept={handleAccept}
          onRejectionReason={rejectionReason}
          onsetRejectionReason={setRejectionReason}
          onReject={handleReject}
        />
      ) : (
        <RenewalRequest
          key={request.id}
          request={request}
          oldDoc={
            request.license_info && request.license_info[0] ? (
              <DrivingLicense
                picture={request.license_info[0].picture}
                info={request.license_info[0]}
                citizen={request.citizen_info}
              />
            ) : null
          }
          newDoc={
            request.license_info && request.license_info[0] ? (
              <DrivingLicense
                picture={request.picture}
                info={{
                  ...request.license_info[0],
                  issue_date: new Date().toISOString().split("T")[0],
                  expiry_date: extendExpiryDate(new Date(), 10),
                }}
                citizen={request.citizen_info}
              />
            ) : null
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
