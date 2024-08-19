import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const DriversLicenseValidationForm = () => {
  // create state variable to control the form
  const [formData, setFormData] = useState({
    license_number: "",
    issue_date: "",
    expiry_date: "",
    nationality: "",
    license_class: "",
    emergency_contact: "",
    picture: "",
    reason: "",
    proof_document: "",
  });
  // create state variable to control the error message
  const [error, setError] = useState("");

  // useNavigate is a hook that allows us to navigate to different pages
  const navigate = useNavigate();

  // set the form data to the appropriate value when the input changes
  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === "file") {
      setFormData({
        ...formData,
        [name]: files[0],
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };
  // ensure that the dates entered are mumbers in the format YYYY-MM-DD
  const validateDateFormat = (dateString) => {
    const regex = /^\d{4}-\d{2}-\d{2}$/; // foramt YYYY-MM-DD
    if (!dateString.match(regex)) return false;

    const date = new Date(dateString);
    const timestamp = date.getTime();

    // check if the date is a number
    if (typeof timestamp !== "number" || Number.isNaN(timestamp)) return false;

    return dateString === date.toISOString().split("T")[0];
  };

  // ensure the field types are correct
  const validateFormData = (data) => {
    // ensure that the license number is 13 characters long without any special characters other than a dash
    if (!/^(?!.*\/)[a-zA-Z0-9\s-]{1,13}$/.test(data.license_number)) {
      return "License number must be 13 characters long without slashes or spaces";
    }
    // ensure that the date format is as expected
    if (
      !validateDateFormat(data.issue_date) ||
      !validateDateFormat(data.expiry_date)
    ) {
      return "Invalid date format. Please use the format YYYY-MM-DD";
    }
    // esnure that the nationality is only alphabets
    if (!/^[a-zA-Z]+$/.test(data.nationality)) {
      return "Nationality must contain only alphabets";
    }
    // ensure that the emergency contact is a valid phone number
    if (!/^\+\d{2,3}\d{9,10}$/.test(data.emergency_contact)) {
      return "Emergency contact must be a valid phone number";
    }
    // esnure the reason field can be empty and it doesn't contain any special characters
    if (data.reason && !/^[a-zA-Z0-9\s]+$/.test(data.reason)) {
      return "Reason for early renewal must contain only alphabets and numbers";
    }

    return "";
  };
  const handleSubmit = async (e) => {
    e.preventDefault(); // this is to prevent the default form submission

    // validate the form data
    const validationError = validateFormData(formData);
    setError(validationError);
    if (validationError !== "") return;

    try {
      // form data object is not directly accepted by the server
      const formDataToSend = new FormData(); // FormData is a web API that provides a way to construct a set of key/value pairs representing form fields and their values
      // convert the form data object to a FormData object that can handle files
      Object.keys(formData).forEach((key) => {
        formDataToSend.append(key, formData[key]);
      });

      // make an API request to the server to validate the citizen's license
      const response = await axios.post(
        "http://127.0.0.1:8080/api/license_info_validation/",
        formDataToSend,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // clear any previous errors
      setError("");
      // redirect the user to the next form upon success
      navigate("/success");
    } catch (error) {
      // check if the error response exists and has a data property with a message
      const errorMessage =
        error.response && error.response.data && error.response.data.message
          ? error.response.data.message
          : "An error occurred. Please try again later.";
      setError(errorMessage);
    }
  };
  // create a state variable to control the visibility of the additional fields
  const [isVisible, setIsVisible] = useState(false);
  useEffect(() => {
    // create a date object for three years ago
    const today = new Date();
    const fiveYearsAgo = new Date(today.setFullYear(today.getFullYear() - 5))
      .toISOString()
      .slice(0, 10);
    // don't do anything if the issue date isn't complete
    if (formData.issue_date.length < 10) {
      return;
    }
    // if the issue date is within five years ago, show the additional fields
    if (formData.issue_date > fiveYearsAgo) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  }, [formData.issue_date]); // dependency array, this effect runs only when formData.issue_date changes

  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <div className="col-md-12 d-flex justify-content-center align-items-center flex-column mt-5">
        <h1>Driver's License Information</h1>
        <p className="col-md-6">
          please confirm you current License information and upload a new
          picture and the latest emergency contact
        </p>
        <div className="form-group col-md-6">
          <label htmlFor="license_number">License Number: </label>
          <input
            type="text"
            name="license_number"
            id="license_number"
            className="form-control"
            value={formData.license_number}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="license_class">License Class: </label>
          <select
            className="form-control"
            name="license_class"
            id="license_class"
            value={formData.license_class}
            onChange={handleChange}
            required={true}
          >
            <option value="">Select A Class</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
          </select>
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="nationality">Nationality: </label>
          <input
            type="text"
            name="nationality"
            id="nationality"
            className="form-control"
            value={formData.nationality}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="issue-date">Issue Date: </label>
          <input
            type="text"
            name="issue_date"
            placeholder="YYYY-MM-DD"
            id="issue-date"
            className="form-control"
            value={formData.issue_date}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="expiry-date">Expiry Date: </label>
          <input
            type="text"
            placeholder="YYYY-MM-DD"
            name="expiry_date"
            className="form-control"
            id="expiry-date"
            value={formData.expiry_date}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="emergency_contact">
            Upade Your Emergency Contact:
          </label>
          <input
            type="text"
            name="emergency_contact"
            id="emergency_contact"
            className="form-control"
            placeholder="e.g. +XX12345678"
            value={formData.emergency_contact}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="file">Upload New Picture: </label>
          <input
            type="file"
            name="picture"
            className="form-control"
            required={true}
            onChange={handleChange}
          />
        </div>
        {isVisible === true ? (
          <>
            <p className="col-md-6 mt-3 fw-bold">
              you already renewed your license in the last 5 years. Please
              provide an early renewal reason and upload a proof document (eg.
              police report)
            </p>
            <div className="form-group col-md-6">
              <label htmlFor="reason">Reason For Early Renewal: </label>
              <textarea
                className="form-control"
                name="reason"
                id="reason"
                value={formData.reason}
                onChange={handleChange}
              />
            </div>
            <div className="form-group col-md-6">
              <label htmlFor="file">Upload a Proof Document: </label>
              <input
                type="file"
                name="proof_document"
                className="form-control"
                onChange={handleChange}
              />
            </div>
          </>
        ) : null}
        {error && (
          <div className="alert alert-info mt-3" role="alert">
            {error}
          </div>
        )}
        <button type="submit" className="button mt-3">
          Submit Request
        </button>
      </div>
    </form>
  );
};
