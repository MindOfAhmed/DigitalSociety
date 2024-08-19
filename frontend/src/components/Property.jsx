export const Property = ({ info, citizen }) => {
  return (
    <div className="card my-3 mx-2 shadow">
      <div className="row">
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <img
            src={info.picture}
            alt="Property"
            className="img-fluid document-picture"
          />
        </div>
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          {/* property info */}
          <div className="col">
            <strong>Property ID: </strong>
            <p>{info.property_id}</p>
            <strong>Type: </strong>
            <p>{info.property_type}</p>
            {info.size && (
              <>
                <strong>Size: </strong>
                <p>{info.size}</p>
              </>
            )}
            <strong>Location: </strong>
            <p>{info.location}</p>
          </div>
          {/* citizen info */}
          <div className="col me-2">
            <strong>
              {info.is_under_transfer
                ? "New Owner's National ID:"
                : "National ID:"}
            </strong>
            <p>{citizen.national_id}</p>
            <strong>Name: </strong>
            <p>{citizen.first_name}</p>
            <strong>Surname: </strong>
            <p>{citizen.last_name}</p>
            <strong>DOB: </strong>
            <p>{citizen.date_of_birth}</p>
            <strong>Sex: </strong>
            <p>{citizen.sex}</p>
          </div>
        </div>
      </div>
      <div className="row d-flex justify-content-center align-items-center">
        <div>
          <p className="mx-3">{info.description}</p>
        </div>
      </div>
    </div>
  );
};
