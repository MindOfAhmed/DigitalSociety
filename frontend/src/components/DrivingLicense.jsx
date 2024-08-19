export const DrivingLicense = ({ picture, info, citizen }) => {
  return (
    <div className="card my-3 mx-2 shadow">
      <div className="row col-md-12 d-flex justify-content-center align-items-center">
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <img
            src={picture}
            alt="Driving License"
            className="img-fluid document-picture"
          />
        </div>
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <div className="col me-3">
            <strong>Name Surname:</strong>
            <p>{`${citizen.first_name} ${citizen.last_name}`}</p>
            <strong>National ID:</strong>
            <p>{citizen.national_id}</p>
            <strong>Blood Type:</strong>
            <p>{citizen.blood_type}</p>
            <strong>Nationality:</strong>
            <p>{info.nationality}</p>
            <strong>Emergency Contact:</strong>
            <p>{info.emergency_contact}</p>
          </div>
          <div className="col">
            <strong>License Number:</strong>
            <p>{info.license_number}</p>
            <strong>License Class:</strong>
            <p>{info.license_class}</p>
            <strong>Issued:</strong>
            <p>{info.issue_date}</p>
            <strong>Expires:</strong>
            <p>{info.expiry_date}</p>
          </div>
        </div>
      </div>
    </div>
  );
};