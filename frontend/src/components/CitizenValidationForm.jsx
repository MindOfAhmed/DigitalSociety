import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const CitizenValidationForm = ({ next }) => {
  // create state variable to control the form
  const [formData, setFormData] = useState({
    national_id: "",
    first_name: "",
    last_name: "",
    date_of_birth: "",
    sex: "",
    blood_type: "",
  });
  // create state variable to control the error message
  const [error, setError] = useState("");

  // useNavigate is a hook that allows us to navigate to different pages
  const navigate = useNavigate();

  // set the form data to the appropriate value when the input changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
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
    // ensure that the national ID is 11 characters long without any special characters other than a dash
    if (!/^(?!.*\/)[a-zA-Z0-9\s-]{1,11}$/.test(data.national_id)) {
      return "National ID must be 11 characters long without slashes or spaces";
    }
    // ensure that the first and last name contain only alphabets without special characters
    if (
      !/^[a-zA-Z\s]+$/.test(data.first_name) ||
      !/^[a-zA-Z\s]+$/.test(data.last_name)
    ) {
      return "First and Last Name must contain only alphabets";
    }
    // ensure that the date format is as expected (YYYY-MM-DD)
    if (!validateDateFormat(data.date_of_birth)) {
      return "Invalid date format. Please use the format YYYY-MM-DD";
    }

    return "";
  };
  // copilot helped with the regex

  const handleSubmit = async (e) => {
    e.preventDefault(); // this is to prevent the default form submission

    // validate the form data
    const validationError = validateFormData(formData);
    setError(validationError);
    if (validationError !== "") return;

    try {
      // make an API request to the server to validate the citizen information
      const response = await axios.post(
        "http://127.0.0.1:8080/api/citizen_info_validation/",
        formData
      );

      // Check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }

      // clear any previous errors
      setError("");

      // redirect the user to the next form upon success
      navigate(`${next}/`);
    } catch (error) {
      const errorMessage =
        error.response && error.response.data && error.response.data.message
          ? error.response.data.message
          : "An error occurred. Please try again later.";
      setError(errorMessage);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="col-md-12 d-flex justify-content-center align-items-center flex-column mt-5">
        <h1>Personal Details</h1>
        <p>please fill in the form below accurately</p>
        <div className="form-group col-md-6">
          <label htmlFor="national_id">National ID</label>
          <input
            type="text"
            id="national_id"
            name="national_id"
            className="form-control"
            value={formData.national_id}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="first_name">First Name: </label>
          <input
            type="text"
            name="first_name"
            id="first_name"
            className="form-control"
            value={formData.first_name}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="last_name">Last Name: </label>
          <input
            type="text"
            name="last_name"
            id="last_name"
            className="form-control"
            value={formData.last_name}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="date_of_birth">Date of Birth: </label>
          <input
            type="text"
            placeholder="YYYY-MM-DD"
            name="date_of_birth"
            id="date_of_birth"
            className="form-control"
            value={formData.date_of_birth}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6  d-flex flex-column justify-content-center align-items-center">
          <label className="col-md-6  d-flex justify-content-center align-items-center">
            Sex:
          </label>
          <div className="form-check col-md-6  d-flex justify-content-center align-items-center">
            <input
              type="radio"
              name="sex"
              className="form-check-input"
              id="M"
              value="M"
              required={true}
              checked={formData.sex === "M"}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="M">
              Male
            </label>
          </div>
          <div className="form-check col-md-6  d-flex justify-content-center align-items-center">
            <input
              type="radio"
              name="sex"
              className="form-check-input"
              id="F"
              value="F"
              required={true}
              checked={formData.sex === "F"}
              onChange={handleChange}
            />
            <label className="form-check-label" htmlFor="F">
              Female
            </label>
          </div>
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="blood_type">Blood Type: </label>
          <select
            className="form-control"
            name="blood_type"
            id="blood_type"
            value={formData.blood_type}
            onChange={handleChange}
            required={true}
          >
            <option value="">Select Blood Type</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
          </select>
        </div>
        {error && (
          <div className="alert alert-info mt-3" role="alert">
            {error}
          </div>
        )}
        <button type="submit" className="button mt-3">
          Next
        </button>
      </div>
    </form>
  );
};
