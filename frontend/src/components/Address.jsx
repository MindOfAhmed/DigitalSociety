export const Address = ({ info, citizen }) => {
  return (
    <div className="card my-3 mx-2 shadow">
      <div className="row d-flex justify-content-center align-items-center">
        <div className="col-md-8 d-flex justify-content-center align-items-center">
          {/* address info */}
          <div className="col mx-3">
            {/* only display the country if it's different from home country */}
            {info.country !== "X" ? (
              <>
                <strong>Country: </strong>
                <p>{info.country}</p>
              </>
            ) : null}
            <strong>City: </strong>
            <p>{info.city}</p>
            <strong>Street: </strong>
            <p>{info.street}</p>
            <strong>Building: </strong>
            <p>{info.building_number}</p>
            <strong>Floor: </strong>
            <p>{info.floor_number}</p>
            <strong>Apartment: </strong>
            <p>{info.apartment_number}</p>
          </div>
          {/* citizen info */}
          <div className="col">
            <strong>
              {info.state === "Pending Request"
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
