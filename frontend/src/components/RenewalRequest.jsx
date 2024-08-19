import { useState } from "react";

export const RenewalRequest = ({
  request,
  oldDoc,
  newDoc,
  onAccept,
  onReject,
  onRejectionReason,
  onsetRejectionReason,
}) => {
  // define state variables to control the rejection reason form's visibility
  const [showReasonForm, setShowReasonForm] = useState(false);
  // handle the form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // reject the request
    onReject(request.id);
  };
  return (
    <div className="card my-5 shadow-sm">
      {/* request title */}
      <h3 className="d-flex col-md-12 justify-content-center align-items-center mb-3">
        {request.request_type} Request
      </h3>
      {/* previous and proposed passports */}
      <div className="row">
        <div className="col-md-6">
          <h4 className="d-flex justify-content-center align-items-center">
            Old {request.request_type}
          </h4>
          {oldDoc}
        </div>
        <div className="col-md-6">
          <h4 className="d-flex justify-content-center align-items-center">
            New {request.request_type}
          </h4>
          {newDoc}
        </div>
      </div>
      {/* early renewal reason and proof document */}
      {request.reason && (
        <div className="row my-3 d-flex flex-column justify-content-center align-items-center">
          <div className="text-center">
            <p>
              <strong>Early Renewal Reason:</strong> {request.reason}
            </p>
            <p>
              <strong>Proof Document Link:</strong> {request.proof_document}
            </p>
          </div>
        </div>
      )}
      {/* accept or reject buttons */}
      <div className="row  d-flex justify-content-center align-items-center mb-3">
        <div className="col-md-8 d-flex justify-content-between">
          <button
            className="button"
            onClick={() => setShowReasonForm(!showReasonForm)}
          >
            {showReasonForm ? "Close" : "Reject"}
          </button>
          <button className="button" onClick={() => onAccept(request.id)}>
            Accept
          </button>
        </div>
      </div>
      {/* rejection reason form */}
      {showReasonForm && (
        <form onSubmit={handleSubmit}>
          <div className="col-md-4 d-flex justify-content-center align-items-center flex-column mx-5 mb-3">
            <div className="form-group">
              <label htmlFor="reason">
                <strong>Reason for Rejection:</strong>
                <textarea
                  className="form-control shadow-sm"
                  name="reason"
                  id="reason"
                  value={onRejectionReason}
                  onChange={(e) => {
                    onsetRejectionReason(e.target.value);
                  }}
                />
              </label>
            </div>
            <button type="submit" className="button mt-3">
              Reject
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
