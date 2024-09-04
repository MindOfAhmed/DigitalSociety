import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export const Steps = ({ stepsContext }) => {
  const [step, setStep] = useState(1); // this will control what's viewed on the card

  // handle the incrementing and decrementing of the step
  const handleIncrementStep = () => {
    if (step < stepsContext.length) {
      setStep((s) => s + 1);
    }
  };
  const handleDecrementStep = () => {
    if (step > 0) {
      setStep((s) => s - 1);
    }
  };

  return (
    <div className="row justify-content-center align-items-center mt-3">
      <div className="card shadow d-flex col-md-10 flex-column justify-content-center align-items-center my-3 py-3">
        <h3>Step: {step}</h3>
        {/* step context */}
        <div className="d-flex flex-column my-3">
          <FontAwesomeIcon
            icon={stepsContext[step - 1].icon}
            size="2x"
            aria-label="an icon that matches the step"
          />
          <p className="mt-2"> {stepsContext[step - 1].step} </p>
        </div>
        {/* steps tracker */}
        <div className="d-flex flex-row col-md-8 justify-content-between mb-3">
          {/* loop over each item in the context array and display a step tracker for it */}
          {stepsContext.map((_, i) => {
            return (
              <div
                className={step >= i + 1 ? "active_step" : "inactive_step"}
                key={i}
              >
                {i + 1}
              </div>
            );
          })}
        </div>
        {/* prev and next buttons */}
        <div className="col-md-12 d-flex justify-content-between">
          <button
            className={step === 1 ? "invisible" : "button"}
            onClick={handleDecrementStep}
          >
            Prev
          </button>
          <button
            className={step === stepsContext.length ? "invisible" : "button"}
            onClick={handleIncrementStep}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};
