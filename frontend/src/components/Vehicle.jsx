export const Vehicle = ({ info, citizen }) => {
  return (
    <div className="card my-3 mx-2 shadow">
      <div className="row">
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          <img
            src={info.picture}
            alt="Vehicle"
            className="img-fluid document-picture"
          />
        </div>
        <div className="col-md-6 d-flex justify-content-center align-items-center">
          {/* Vehicle info */}
          <div className="col">
            <strong>Serial Number: </strong>
            <p>{info.serial_number}</p>
            <strong>Plate Number: </strong>
            <p>{info.plate_number}</p>
            <strong>Model: </strong>
            <p>{info.model}</p>
            <strong>Year: </strong>
            <p>{info.year}</p>
            <strong>Manufacturer: </strong>
            <p>{info.manufacturer}</p>
            <strong>Vehicle Type: </strong>
            <p>{info.vehicle_type}</p>
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
    </div>
  );
};
