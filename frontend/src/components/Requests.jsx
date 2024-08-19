import { Tab, Tabs } from "react-bootstrap";
import { RegistrationRequests } from "./RegistrationRequests";
import { RenewalRequests } from "./RenewalRequests";

export const Requests = () => {
  return (
    // split the page into two tabs
    <Tabs defaultActiveKey="Renewal Requests" id="requests-tab">
      <Tab eventKey="Renewal Requests" title="Renewal Requests">
        <RenewalRequests />
      </Tab>
      <Tab eventKey="Registration Requests" title="Registration Requests">
        <RegistrationRequests />
      </Tab>
    </Tabs>
  );
};
