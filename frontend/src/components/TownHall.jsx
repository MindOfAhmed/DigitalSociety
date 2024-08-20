import { useState, useEffect } from "react";
import { ForumModal } from "./ForumModal";
import axios from "axios";

export const TownHall = ({ userGroups }) => {
  // define state variable to store the list of forums
  const [forums, setForums] = useState([]);
  // this function will check if the user is in a specific group
  const isInGroup = (group) => userGroups.includes(group);
  // define state variable that will control the visibility of the modal
  const [showModal, setShowModal] = useState(false);
  // define handlers for showing and hiding the modal
  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);
  // define a handler for submitting the form
  const handleSubmit = async (title, region) => {
    try {
      // create a FormData object to send the form data
      const formData = new FormData();
      formData.append("title", title);
      formData.append("region", region);
      // make an API call to create a new forum
      const response = await axios.post(
        "http://127.0.0.1:8080/api/create_forum/",
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
      handleCloseModal();
    } catch (error) {
      console.error("Failed to create forum", error);
    }
  };

  // on mount, fetch the list of forums
  useEffect(() => {
    try {
      (async () => {
        const response = await axios.get(
          "http://127.0.0.1:8080/api/get_forums/"
        );
        if (!response || !response.data) {
          throw new Error("Invalid server response");
        }
        setForums(response.data);
      })();
    } catch (error) {
      console.error("Failed to fetch forums", error);
    }
  }, []);

  return (
    <>
      <div className="row my-3">
        {isInGroup("Reps") && (
          <div className="d-flex justify-content-end align-items-center">
            <button className="button" onClick={handleShowModal}>
              Create Forum
            </button>
          </div>
        )}
      </div>
      {/* list of forums */}
      {forums.map((forum, index) => (
        <div key={index} className="card my-2">
          <div className="card-body">
            <h5 className="card-title">{forum.title}</h5>
            <p className="card-text">Region: {forum.region}</p>
          </div>
        </div>
      ))}
      {/* modal to create forums */}
      <ForumModal
        show={showModal}
        handleClose={handleCloseModal}
        onSubmit={handleSubmit}
      />
    </>
  );
};
