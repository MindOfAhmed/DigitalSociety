import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export const Card = ({ description, icon, title }) => {
  return (
    <div className="col-md-3 mx-5 card shadow">
      <div className="mt-2 d-flex justify-content-center align-items-center">
        <FontAwesomeIcon
          icon={icon}
          className="mx-3 fa-2x"
          aria-label="an icon that matches the card's title"
        />
        <h5 className="card-title">{title}</h5>
      </div>
      <p className="card-body">{description}</p>
    </div>
  );
};
