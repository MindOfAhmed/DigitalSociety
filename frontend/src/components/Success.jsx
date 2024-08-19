import { Link } from "react-router-dom";

export const Success = () => {
  return (
    <div className="col-md-12 mt-5 d-flex flex-column justify-content-center align-items-center">
      <h1>Your request is under process!</h1>
      <p>We will send you a notification with updates</p>
      <Link to="/" className="button">
        Home
      </Link>
    </div>
  );
};
