import passport from "../assets/passport.jpg";
import driver from "../assets/driver.jpg";
import address from "../assets/address.jpg";
import vehicle from "../assets/vehicle.jpg";
import property from "../assets/property.jpg";
import { Service } from "./Service";
import {
  faHouseUser,
  faUser,
  faPassport,
  faIdCard,
  faMapMarker,
  faCheckCircle,
  faCar,
} from "@fortawesome/free-solid-svg-icons";

export const Services = () => {
  const passportSteps = [
    { step: "Fill in your personal details", icon: faUser },
    { step: "Confirm your address", icon: faMapMarker },
    {
      step: "Confirm your current passport details and upload new picture",
      icon: faPassport,
    },
    {
      step: "You're all set & we will process your request!",
      icon: faCheckCircle,
    },
  ];
  const licensetSteps = [
    { step: "Fill in your personal details", icon: faUser },
    { step: "Confirm your address", icon: faMapMarker },
    {
      step: "Confirm your current license details and upload new picture",
      icon: faIdCard,
    },
    {
      step: "You're all set & we will process your request!",
      icon: faCheckCircle,
    },
  ];
  const addressSteps = [
    { step: "Fill in your personal details", icon: faUser },
    {
      step: "Enter new address details & upload a proof document",
      icon: faMapMarker,
    },
    {
      step: "You're all set & we will process your request!",
      icon: faCheckCircle,
    },
  ];
  const vehicleSteps = [
    { step: "Fill in your personal details", icon: faUser },
    {
      step: "Enter the vehicle details & upload a proof document",
      icon: faCar,
    },
    {
      step: "You're all set & we will process your request!",
      icon: faCheckCircle,
    },
  ];
  const propertySteps = [
    { step: "Fill in your personal details", icon: faUser },
    {
      step: "Enter the property details & upload a proof document",
      icon: faHouseUser,
    },
    {
      step: "You're all set & we will process your request!",
      icon: faCheckCircle,
    },
  ];

  return (
    <>
      <Service
        title="Passport Renewal"
        picture={passport}
        stepsContext={passportSteps}
        serviceLink={"/services/passport_citizen"}
      />
      <Service
        title="Address Registration"
        picture={address}
        stepsContext={addressSteps}
        serviceLink={"/services/address_citizen"}
      />
      <Service
        title="Vehicle Registration"
        picture={vehicle}
        stepsContext={vehicleSteps}
        serviceLink={"/services/vehicle_citizen"}
      />
      <Service
        title="Driver's License Renewal"
        picture={driver}
        stepsContext={licensetSteps}
        serviceLink={"/services/DriversLicense_citizen"}
      />
      <Service
        title="Property Registration"
        picture={property}
        stepsContext={propertySteps}
        serviceLink={"/services/property_citizen"}
      />
    </>
  );
};
