import { Steps } from "./steps";
import { Link } from "react-router-dom";

export const Service = ({ title, picture, stepsContext, serviceLink }) => {
  return (
    <>
      <div className="row my-5">
        <div className="col-md-12 d-flex justify-content-center">
          <h1>{title}</h1>
        </div>
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <img
            src={picture}
            alt="a passport"
            width={500}
            height={275}
            className="service_image shadow-lg"
          />
        </div>
        <div className="col-md-6 d-flex flex-column align-items-center justify-content-center">
          <div className="w-100">
            <Steps stepsContext={stepsContext} />
          </div>
        </div>
        <div className="col-md-12 d-flex justify-content-center mt-2">
          <Link to={serviceLink} className="button">
            Start!
          </Link>
        </div>
      </div>
    </>
  );
};
