import { useState } from "react";
import { useRouteError, useNavigate } from "react-router-dom";

const ErrorBoundary = () => {
  const error = useRouteError();
  const navigate = useNavigate();

  const errorMsg = {
    404: {
      title: "Page Not Found️ ⚠️",
      statusCode: 404,
      message: "We couldn't find the page you are looking for.",
    },
    403: {
      title: "You are not authorized! 🔐",
      statusCode: 403,
      message: "You don’t have permission to access this page. Go Home!",
    },
    500: {
      title: "Network Error 🚧",
      statusCode: 500,
      message: "Please try again later.",
    },
  };

  const currentError = errorMsg[error?.status] || errorMsg[500];

  return (
    <>
      <div className="container-xxl container-p-y">
        <div className="misc-wrapper">
          <h1
            className="mb-2 mx-2"
            style={{ lineHeight: "6rem", fontSize: "6rem" }}
          >
            {currentError.statusCode}
          </h1>
          <h4 className="mb-2 mx-2">{currentError.title}</h4>
          <p className="mb-6 mx-2">{currentError.message}</p>
          <a
            href="javascript:void(0);"
            className="btn btn-primary mb-10 waves-effect waves-light"
            onClick={() => navigate(-1)}
          >
            Back to home
          </a>
          <div className="mt-12">
            <img
              src="/assets/img/illustrations/page-misc-under-maintenance.png"
              alt="page-misc-under-maintenance"
              width={550}
              className="img-fluid"
            />
          </div>
        </div>
      </div>
      <div className="container-fluid misc-bg-wrapper misc-under-maintenance-bg-wrapper">
        <img
          src="/assets/img/illustrations/bg-shape-image-light.png"
          height={355}
          alt="page-misc-under-maintenance"
          data-app-light-img="illustrations/bg-shape-image-light.png"
          data-app-dark-img="illustrations/bg-shape-image-dark.html"
        />
      </div>
    </>
  );
};

export default ErrorBoundary;
