import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export const VehicleRegistrationForm = () => {
  // create state variable to control the form
  const [formData, setFormData] = useState({
    serial_number: "",
    manufacturer: "",
    model: "",
    year: "",
    vehicle_type: "",
    picture: "",
    proof_document: "",
    previous_owner_id: "",
    plate_number: "",
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
    // ensure that the previous owner ID is 11 characters long without any special characters other than a dash
    if (!/^(?!.*\/)[a-zA-Z0-9\s-]{1,11}$/.test(data.previous_owner_id)) {
      return "Previous owner ID must be 11 characters long without slashes or spaces";
    }
    // ensure that the model and manufacturer only contain alphabets with no special characters
    if (
      !/^[a-zA-Z\s]+$/.test(data.model) ||
      !/^[a-zA-Z\s]+$/.test(data.manufacturer)
    ) {
      return "Model and Manufacturer must contain only alphabets";
    }
    // ensure the plate number only contains alphabets and numbers with dashes and no other special characters
    if (!/^[a-zA-Z0-9-]+$/.test(data.plate_number)) {
      return "Plate Number must contain only alphabets, numbers, and dashes. eg. 34-jwt-45";
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
      // make an API request to the server to register the citizen's alleged vehicle
      const response = await axios.post(
        "http://127.0.0.1:8080/api/register_vehicle/",
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
        <h1>Vehicle Confirmation</h1>
        <p>please enter the new vehicle details and upload a proof document</p>
        <div className="form-group col-md-6">
          <label htmlFor="serial_number">Serial Number: </label>
          <input
            type="number"
            name="serial_number"
            id="serial_number"
            className="form-control"
            value={formData.serial_number}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="previous_owner_id">Previous Owner National ID:</label>
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
          <label htmlFor="model">model: </label>
          <input
            type="text"
            name="model"
            id="model"
            placeholder="In the exact format in the proof document. eg. Toyota Corolla"
            className="form-control"
            value={formData.model}
            required={true}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="vehicle_type">Vehicle Type: </label>
          <select
            className="form-control"
            name="vehicle_type"
            id="vehicle_type"
            value={formData.vehicle_type}
            onChange={handleChange}
            required={true}
          >
            <option value="">Select A Vehicle Type</option>
            <option value="SUV">SUV</option>
            <option value="Sedan">Sedan</option>
            <option value="Truck">Truck</option>
            <option value="Van">Van</option>
            <option value="Bus">Bus</option>
            <option value="Sports Car">Sports Car</option>
            <option value="Motorcycle">Motorcycle</option>
          </select>
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="manufacturer">Manufacturer: </label>
          <input
            type="text"
            name="manufacturer"
            id="manufacturer"
            className="form-control"
            value={formData.manufacturer}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="year">Year: </label>
          <input
            type="number"
            name="year"
            id="year"
            className="form-control"
            value={formData.year}
            onChange={handleChange}
          />
        </div>
        <div className="form-group col-md-6">
          <label htmlFor="plate_number">Plate Number: </label>
          <input
            type="text"
            name="plate_number"
            id="plate_number"
            placeholder="eg. 34-jwt-45"
            className="form-control"
            value={formData.plate_number}
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
          <label htmlFor="file">Upload a picture of The Vehicle:</label>
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
