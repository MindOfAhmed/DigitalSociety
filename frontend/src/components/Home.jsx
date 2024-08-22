import { Card } from "./Card";
import { Link } from "react-router-dom";
import bannerImage from "../assets/banner.jpg";
import townhall from "../assets/th.jpg";
import townhallGov from "../assets/thGov.jpg";
import townhallCitizens from "../assets/thCitizens.jpg";
import {
  faHouseUser,
  faPassport,
  faIdCard,
} from "@fortawesome/free-solid-svg-icons";

export const Home = () => {
  return (
    <>
      {/* header and image */}
      <div className="row mt-5">
        <div className="col-md-6">
          <h1>Welcome To The Digital Society!</h1>
          <p>
            The Digital Society is a platform that provides digital services to the citizens of 
            country X. We aim to provide a seamless experience for citizens to renew, register, 
            and access their documents all in one place.
          </p>
        </div>
        <div className="col-md-6 d-flex align-items-center justify-content-center">
          <img
            src={bannerImage}
            alt="a group of people communicating"
            width={300}
            height={200}
            className="shadow-lg"
          />
        </div>
      </div>
      {/* services */}
      <div className="row mt-5 mb-3">
        <div className="col-md-12 d-flex justify-content-center">
          <h3>Available Services</h3>
        </div>
      </div>
      <div className="row d-flex justify-content-center">
        <Card
          title="Passport Renewal"
          icon={faPassport}
          description="Renewing your passport has never been easier! Simply fill out the form and submit your documents."
        />
        <Card
          title="Driver's License Renewal"
          icon={faIdCard}
          description="Time to renew your Driver's license? We've got you covered. Follow the steps provided & leave the rest to us."
        />
        <Card
          title="Property Registration"
          icon={faHouseUser}
          description="Got a new property? Register it with us in a few simple steps. We'll take care of the rest."
        />
      </div>
      <div className="row d-flex justify-content-center mt-4 mb-3">
        <div className="col-md-12 d-flex justify-content-center">
          <Link to="/services" className="button">
            Learn More
          </Link>
        </div>
      </div>
      {/* Town Hall */}
      <div className="row d-flex mt-5">
        <div className="col-md-4 d-flex justify-content-end image-container">
          <img
            src={townhallGov}
            alt="government representatives listening in townhall"
            className="first-image"
          />
        </div>
        <div className="col-md-1">
          <p className="town_hall_text">Town Hall</p>
        </div>
      </div>
      <div className="row d-flex">
        <div className="col-md-3 mt-5 d-flex align-items-center">
          <p>
            The town hall is a place where citizens can voice their concerns and
            discuss important issues with government representatives. Join the local
            or national open forums and be a part of the conversation.
          </p>
        </div>
        <div className="col-md-5 image-container">
          <img src={townhall} alt="A townhall" className="second-image" />
        </div>
      </div>
      <div className="row d-flex">
        <div className="col-md-4 image-container">
          <img
            src={townhallCitizens}
            alt="citizens speaking in townhall"
            className="third-image"
          />
        </div>
        <div className="col-md-3 d-flex justify-content-center align-items-center">
          <Link to="/townhall" className="text-center button">
            Join Now
          </Link>
        </div>
      </div>
    </>
  );
};
