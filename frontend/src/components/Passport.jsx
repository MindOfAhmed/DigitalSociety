export const Passport = ({ citizen, picture, info }) => {
  return (
    <div className="card my-3 mx-2 shadow">
      <div className="row">
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <img
            src={picture}
            alt="a passport"
            className="img-fluid document-picture"
          />
        </div>
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          {/* citizen info */}
          <div className="col me-3">
            <strong>Name Surname:</strong>
            <p>{`${citizen.first_name} ${citizen.last_name}`}</p>
            <strong>National ID:</strong>
            <p>{citizen.national_id}</p>
            <strong>DOB:</strong>
            <p>{citizen.date_of_birth}</p>
            <strong>Sex:</strong>
            <p>{citizen.sex}</p>
          </div>
          {/* passport info */}
          <div className="col">
            <strong>Passport Number:</strong>
            <p>{info.passport_number}</p>
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
