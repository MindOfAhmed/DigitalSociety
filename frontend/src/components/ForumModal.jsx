import { useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

export const ForumModal = ({ show, handleClose, onSubmit }) => {
  // define state variables to control the form
  const [title, setTitle] = useState("");
  const [region, setRegion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // ensure the title and region are not empty
    if (!title || !region) {
      return;
    }
    // send the form data to the parent component
    onSubmit(title, region);
    // reset the state variables
    setTitle("");
    setRegion("");
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Create Forum</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formTitle">
            <Form.Label>Forum Title</Form.Label>
            <Form.Control
              type="text"
              defaultValue={title}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="formRegion" className="mt-3">
            <Form.Label>
              Select region by city or type "nation" for nationwide forum
            </Form.Label>
            <Form.Control
              type="text"
              defaultValue={region}
              value={region}
              onChange={(e) => setRegion(e.target.value)}
            />
          </Form.Group>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
            <Button type="submit" variant="primary">
              Create Forum
            </Button>
          </Modal.Footer>
        </Form>
      </Modal.Body>
    </Modal>
  );
};
