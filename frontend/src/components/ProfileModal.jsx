import { useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

export const ProfileModal = ({ show, handleClose, citizen, onSubmit }) => {
  // define state variables to control the form
  const [username, setUsername] = useState(citizen?.user?.username || "");
  const [profilePicture, setProfilePicture] = useState(null);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // define state variable that controls the visibility of the password fields
  const [changePassword, setChangePassword] = useState(false);

  // define the function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // ensure that the new password and confirm password match
    if (newPassword !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    // send the form data to the parent component
    onSubmit(username, profilePicture, currentPassword, newPassword);
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Edit Profile</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              defaultValue={username}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="formProfilePicture" className="mt-3">
            <Form.Label>Profile Picture</Form.Label>
            <Form.Control
              type="file"
              onChange={(e) => setProfilePicture(e.target.files[0])}
            />
          </Form.Group>
          {/* button that renders the password fields */}
          <Button
            className="mt-3"
            variant="secondary"
            onClick={() => setChangePassword((s) => !s)}
          >
            {changePassword ? "Cancel" : "Change Password"}
          </Button>
          {changePassword && (
            <>
              <Form.Group controlId="formCurrentPassword" className="mt-3">
                <Form.Label>Current Password</Form.Label>
                <Form.Control
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </Form.Group>
              <Form.Group controlId="formNewPassword" className="mt-3">
                <Form.Label>New Password</Form.Label>
                <Form.Control
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </Form.Group>
              <Form.Group controlId="formConfirmPassword" className="mt-3">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </Form.Group>
            </>
          )}
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
            <Button type="submit" variant="primary">
              Save Changes
            </Button>
          </Modal.Footer>
        </Form>
      </Modal.Body>
    </Modal>
  );
};
// copilot ^_^
