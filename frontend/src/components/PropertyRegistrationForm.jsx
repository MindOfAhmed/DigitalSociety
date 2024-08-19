import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const PropertyRegistrationForm = () => {
  // create state variable to control the form
  const [formData, setFormData] = useState({
    property_id: "",
    location: "",
    property_type: "",
    description: "",
    size: "",
    picture: "",
    proof_document: "",
    previous_owner_id: "",
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
    // ensure that the property id is 8 characters long without any special characters other than a dash
    if (!/^(?!.*\/)[a-zA-Z0-9\s-]{1,8}$/.test(data.property_id)) {
      return "Property ID must be 8 characters long without slashes or spaces";
    }
    // ensure that the previous owner ID is 11 characters long without any special characters other than a dash
    if (!/^(?!.*\/)[a-zA-Z0-9\s-]{1,11}$/.test(data.previous_owner_id)) {
      return "Previous owner ID must be 11 characters long without slashes or spaces";
    }
    // ensure that the location, description, and size have no special characters
    if (
      !/^[a-zA-Z0-9\s]+$/.test(data.location) ||
      !/^[a-zA-Z0-9\s]+$/.test(data.description) ||
      !/^[a-zA-Z0-9\s]+$/.test(data.size)
    ) {
      return "Location, Description, and size must contain only alphabets and numbers";
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
      // make an API request to the server to register the citizen's alleged property
      const response = await axios.post(
        "http://127.0.0.1:8080/api/register_property/",
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
        <h1>Property Confirmation</h1>
        <p>
          please enter the details for your new property and upload a proof
          document
        </p>
        <div className="form-group col-md-6">
          <label htmlFor="property_id">Propert ID: </label>
          <input
            type="text"
            name="property_id"
            id="property_id"
            className="form-control"
            value={formData.property_id}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="previous_owner_id">
            Previous Owner National ID:{" "}
          </label>
          <input
            type="text"
            name="previous_owner_id"
            id="previous_owner_id"
            className="form-control"
            value={formData.previous_owner_id}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="location">Property Location: </label>
          <input
            type="text"
            name="location"
            id="location"
            placeholder="In the exact format in the proof document. eg. 123 Main Street, New York"
            className="form-control"
            value={formData.location}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="property_type">Property Type: </label>
          <select
            className="form-control"
            name="property_type"
            id="property_type"
            value={formData.property_type}
            onChange={handleChange}
            required={true}
          >
            <option value="">Select A Property Type</option>
            <option value="Residential">Residential</option>
            <option value="Commercial">Commercial</option>
            <option value="Industrial">Industrial</option>
            <option value="Agricultural">Agricultural</option>
            <option value="Land">Land</option>
            <option value="Intellectual">Intellectual</option>
          </select>
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="description">Property Description: </label>
          <textarea
            className="form-control"
            name="description"
            id="description"
            value={formData.description}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="size">Property Size: </label>
          <input
            type="text"
            name="size"
            id="size"
            placeholder="In the exact format in the proof document. eg. 1000 sqft"
            className="form-control"
            value={formData.size}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="file">Upload a Proof Document: eg. contract</label>
          <input
            type="file"
            name="proof_document"
            required={true}
            className="form-control"
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="file">Upload a picture of The Property:</label>
          <input
            type="file"
            name="picture"
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
