import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const AddressRegistrationForm = () => {
  // create state variable to control the form
  const [formData, setFormData] = useState({
    country: "",
    city: "",
    street: "",
    building_number: "",
    floor_number: "",
    apartment_number: "",
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

  // ensure the field types are correct
  const validateFormData = (data) => {
    // ensure that the street can have both alphabets and numbers without special characters
    if (!/^[a-zA-Z0-9\s]+$/.test(data.street)) {
      return "Street can only be number or alphabets";
    }
    // ensure that the country and city contain only alphabets without special characters
    if (!/^[a-zA-Z]+$/.test(data.country) || !/^[a-zA-Z]+$/.test(data.city)) {
      return "Country and City must contain only alphabets";
    }

    return "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // this is to prevent the default form submission

    // validate the form data
    const validationError = validateFormData(formData);
    setError(validationError);
    if (validationError !== "") return;

    // form data object is not directly accepted by the server
    const formDataToSend = new FormData(); // FormData is a web API that provides a way to construct a set of key/value pairs representing form fields and their values
    // convert the form data object to a FormData object that can handle files
    Object.keys(formData).forEach((key) => {
      formDataToSend.append(key, formData[key]);
    });

    try {
      // make an API request to the server to register the citizen's alleged address
      const response = await axios.post(
        "http://127.0.0.1:8080/api/register_address/",
        formDataToSend,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      // Check if response and response.data are defined
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }

      // clear any previous errors
      setError("");

      // redirect the user to the success page
      navigate("/success");
    } catch (error) {
      const errorMessage =
        error.response && error.response.data && error.response.data.message
          ? error.response.data.message
          : "An error occurred. Please try again later."; // this is in case the error message is not available
      setError(errorMessage);
    }
  };

  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <div className="col-md-12 d-flex justify-content-center align-items-center flex-column mt-5">
        <h1>New Address Confirmation</h1>
        <p>
          please enter the details for your new address and upload a proof
          document
        </p>
        <div className="form-group col-md-6">
          <label htmlFor="country">Country</label>
          <input
            type="text"
            name="country"
            id="country"
            className="form-control"
            value={formData.country}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="city">City: </label>
          <input
            type="text"
            name="city"
            id="city"
            className="form-control"
            value={formData.city}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="street">Street: </label>
          <input
            type="text"
            name="street"
            id="street"
            className="form-control"
            value={formData.street}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="building_number">Building Number: </label>
          <input
            type="number"
            name="building_number"
            id="building_number"
            className="form-control"
            value={formData.building_number}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="floor_number">Floor Number: </label>
          <input
            type="number"
            name="floor_number"
            id="floor_number"
            className="form-control"
            value={formData.floor_number}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="apartment_number">Apartment Number: </label>
          <input
            type="number"
            name="apartment_number"
            id="apartment_number"
            className="form-control"
            value={formData.apartment_number}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="file">
            Upload a Proof Document: eg. utility bill, contract, pledge, etc.{" "}
          </label>
          <input
            type="file"
            name="proof_document"
            required={true}
            className="form-control"
            onChange={handleChange}
          />
        </div>
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
