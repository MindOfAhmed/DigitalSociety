import axios from "axios";
import React from "react";
import { render, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { Passport } from "../components/Passport";
import { DrivingLicense } from "../components/DrivingLicense";
import { Address } from "../components/Address";
import { Property } from "../components/Property";
import { Vehicle } from "../components/Vehicle";
import { Card } from "../components/Card";
import { Service } from "../components/Service";
import { Services } from "../components/Services";
import { Steps } from "../components/steps";
import { Footer } from "../components/Footer";
import { Nav } from "../components/Nav";
import { Home } from "../components/Home";
import { RegistrationRequest } from "../components/RegistrationRequest";
import { RegistrationRequests } from "../components/RegistrationRequests";
import { RenewalRequest } from "../components/RenewalRequest";
import { faIdCard, faCheckCircle } from "@fortawesome/free-solid-svg-icons";

/** Note: there might be a warning when running the test suite:
 * "When testing, code that causes React state updates should be wrapped into act(...):"
 * The problem is with the library insisting on wrapping into act while ESlint produces an error if wrapped into act
 * saying it's not necessary. However, all tests pass. */

// mock the axios module
jest.mock("axios");

// test for the component snapshots
describe("Component Snapshots", () => {
  // test for Passport component
  test("Passport component renders correctly with given props", () => {
    // define mock data for the Passport component
    const citizen = {
      first_name: "John",
      last_name: "Doe",
      national_id: "123456789",
      date_of_birth: "1980-01-01",
      sex: "M",
    };
    const picture = "../assets/passport.jpg";
    const info = {
      passport_number: "A1234567",
      issue_date: "2020-01-01",
      expiry_date: "2030-01-01",
    };
    // render the Passport component with the given props
    const { asFragment } = render(
      <Passport citizen={citizen} picture={picture} info={info} />
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for DrivingLicense component
  test("DrivingLicense component renders correctly with given props", () => {
    // define mock data for the DrivingLicense component
    const citizen = {
      first_name: "John",
      last_name: "Doe",
      national_id: "123456789",
      date_of_birth: "1980-01-01",
      blood_type: "A+",
      nationality: "X",
      emergency_contact: "+90123456789",
    };
    const picture = "../assets/passport.jpg";
    const info = {
      license_number: "A1234567",
      license_class: "A",
      issue_date: "2020-01-01",
      expiry_date: "2030-01-01",
    };
    // render the DrivingLicense component with the given props
    const { asFragment } = render(
      <DrivingLicense citizen={citizen} picture={picture} info={info} />
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Address component
  test("Address component renders correctly with given props", () => {
    // define mock data for the Address component
    const citizen = {
      first_name: "John",
      last_name: "Doe",
      national_id: "123456789",
      date_of_birth: "1980-01-01",
      sex: "M",
    };
    const info = {
      country: "X",
      city: "City",
      street: "Street",
      building_number: "1",
      floor_number: "2",
      apartment_number: "3",
    };
    // render the Address component with the given props
    const { asFragment } = render(<Address citizen={citizen} info={info} />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Property component
  test("Property component renders correctly with given props", () => {
    // define mock data for the Property component
    const citizen = {
      first_name: "John",
      last_name: "Doe",
      national_id: "123456789",
      date_of_birth: "1980-01-01",
      sex: "M",
    };
    const info = {
      property_id: "A1234567",
      property_type: "House",
      size: "100",
      location: "City",
      description: "Description",
      picture: "../assets/property.jpg",
    };
    // render the Property component with the given props
    const { asFragment } = render(<Property citizen={citizen} info={info} />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Vehicle component
  test("Vehicle component renders correctly with given props", () => {
    // define mock data for the Vehicle component
    const citizen = {
      first_name: "John",
      last_name: "Doe",
      national_id: "123456789",
      date_of_birth: "1980-01-01",
      sex: "M",
    };
    const info = {
      serial_number: "123456789",
      plate_number: "34-jwt-45",
      model: "Model",
      year: "2020",
      manufacturer: "Manufacturer",
      vehicle_type: "Car",
      picture: "../assets/vehicle.jpg",
    };
    // render the Vehicle component with the given props
    const { asFragment } = render(<Vehicle citizen={citizen} info={info} />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Card component
  test("Card component renders correctly with given props", () => {
    // define mock data for the Card component
    const description = "Description";
    const title = "Title";
    // render the Card component with the given props
    const { asFragment } = render(
      <Card description={description} icon={faIdCard} title={title} />
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Service component
  test("Service component renders correctly with given props", () => {
    // define mock data for the Service component
    const title = "Title";
    const picture = "../assets/banner.jpg";
    const stepsContext = [
      { step: "Step 1", icon: faIdCard },
      { step: "Step 2", icon: faCheckCircle },
    ];
    const serviceLink = "/services/passport_citizen";
    // render the Service component with the given props
    const { asFragment } = render(
      <BrowserRouter>
        <Service
          title={title}
          picture={picture}
          stepsContext={stepsContext}
          serviceLink={serviceLink}
        />
      </BrowserRouter>
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Services component
  test("Services component renders correctly", () => {
    // render the Services component
    const { asFragment } = render(
      <BrowserRouter>
        <Services />
      </BrowserRouter>
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Steps component
  test("Steps component renders correctly with given props", () => {
    // define mock data for the Steps component
    const stepsContext = [
      { step: "Step 1", icon: faIdCard },
      { step: "Step 2", icon: faCheckCircle },
    ];
    // render the Steps component with the given props
    const { asFragment } = render(<Steps stepsContext={stepsContext} />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Footer component
  test("Footer component renders correctly", () => {
    // render the Footer component
    const { asFragment } = render(<Footer />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Nav component
  test("Nav component renders correctly with given props", async () => {
    // mock the API response
    axios.get.mockResolvedValue({ data: { groups: ["Inspectors"] } });
    // define props
    const props = {
      isLoggedIn: true,
      onLogout: jest.fn(),
      notifications: [{ message: "New notification" }],
      userGroups: ["Inspectors", "Citizens"],
    };
    // render the Nav component with the given props
    const { asFragment } = render(
      <BrowserRouter>
        <Nav {...props} />
      </BrowserRouter>
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for Home component
  test("Home component renders correctly", () => {
    // render the Home component
    const { asFragment } = render(
      <BrowserRouter>
        <Home />
      </BrowserRouter>
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for RegistrationRequest component
  test("RegistrationRequest component renders correctly with given props", () => {
    // define mock data for the RegistrationRequest component
    const request = {
      id: 1,
      request_type: "Property Registration",
      citizen_info: {
        first_name: "John",
        last_name: "Doe",
        national_id: "123456789",
        date_of_birth: "1980-01-01",
        sex: "M",
      },
      property_info: {
        property_id: "A1234567",
        property_type: "House",
        size: "100",
        location: "City",
        description: "Description",
        picture: "../assets/property.jpg",
      },
      proof_document: "Proof Document Link",
    };
    // render the RegistrationRequest component with the given props
    const { asFragment } = render(<RegistrationRequest request={request} />);
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for RegistrationRequests component
  test("RegistrationRequests component renders correctly", async () => {
    // define mock data for the API response
    const mockData = [
      {
        id: 1,
        request_type: "Property Registration",
        citizen_info: {
          first_name: "John",
          last_name: "Doe",
          national_id: "123456789",
          date_of_birth: "1980-01-01",
          sex: "M",
        },
        property_info: {
          property_id: "A1234567",
          property_type: "House",
          size: "100",
          location: "City",
          description: "Description",
          picture: "../assets/property.jpg",
        },
        proof_document: "Proof Document Link",
      },
      {
        id: 2,
        request_type: "Vehicle Registration",
        citizen_info: {
          first_name: "Jane",
          last_name: "Doe",
          national_id: "987654321",
          date_of_birth: "1990-01-01",
          sex: "F",
        },
        vehicle_info: {
          serial_number: "987654321",
          plate_number: "34-jwt-45",
          model: "Model",
          year: "2020",
          manufacturer: "Manufacturer",
          vehicle_type: "Car",
          picture: "../assets/vehicle.jpg",
        },
        proof_document: "Proof Document Link",
      },
    ];
    // mock the API response
    axios.get.mockResolvedValue({ data: mockData });
    // render the component
    const { asFragment } = render(<RegistrationRequests />);
    // wait for the component to update with the mock data
    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        "http://127.0.0.1:8080/api/registration_requests/"
      );
    });
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
  // test for RenewalRequest component
  test("RenewalRequest component renders correctly with given props", () => {
    // define mock data for the RenewalRequest component
    const request = {
      id: 1,
      request_type: "Passport Renewal",
      citizen_info: {
        first_name: "John",
        last_name: "Doe",
        national_id: "123456789",
        date_of_birth: "1980-01-01",
        sex: "M",
      },
      passport_info: [
        {
          passport_number: "A1234567",
          issue_date: "2020-01-01",
          expiry_date: "2030-01-01",
          picture: "../assets/passport.jpg",
        },
      ],
      reason: "Reason",
      proof_document: "Proof Document Link",
    };
    const onAccept = jest.fn();
    const onReject = jest.fn();
    const setRejectionReason = jest.fn();
    const rejectionReason = "";
    // mock useState to return the state and the mock setter function
    jest
      .spyOn(React, "useState")
      .mockImplementation((initialValue) => [
        initialValue === "" ? rejectionReason : initialValue,
        setRejectionReason,
      ]);
    const oldDoc = (
      <Passport
        citizen={request.citizen_info}
        info={request.passport_info[0]}
        picture={request.passport_info[0].picture}
      />
    );
    const newDoc = (
      <Passport
        citizen={request.citizen_info}
        info={{
          ...request.passport_info[0],
          issue_date: new Date().toISOString().split("T")[0],
          expiry_date: new Date().toISOString().split("T")[0],
        }}
        picture={request.passport_info[0].picture}
      />
    );
    // render the RenewalRequest component with the given props
    const { asFragment } = render(
      <RenewalRequest
        request={request}
        oldDoc={oldDoc}
        newDoc={newDoc}
        onAccept={onAccept}
        onReject={onReject}
        onRejectionReason={setRejectionReason}
        onsetRejectionReason={setRejectionReason}
      />
    );
    // compare the rendered component with a saved snapshot
    expect(asFragment()).toMatchSnapshot();
  });
});
