import Swal from 'sweetalert2';
let errorPopupShown = false;

const checkConnectivity = async () => {
    try {
      const response = await fetch('/check-connectivity');
      if (response.ok) {
        return true; 
      } else {
        return false; 
      }
    } catch (error) {
      return false; 
    }
  };

  const handleApiError = async (error) => {
  console.log("ErrorTypeCommon::",error);
  console.log("Online status:", navigator.onLine);
  const isOnline = await checkConnectivity();
  
  if (!isOnline) {
    Swal.fire({
      icon: "error",
      title: "No Internet",
      text: "You are currently offline. Please check your internet connection.",
      confirmButtonText: "OK",
      showCloseButton: false,
      allowOutsideClick: false,
      allowEscapeKey: false,
    });
    return;
  }
  if (!errorPopupShown) {
    errorPopupShown = true;
    console.log("errormessage::")
    if (error.code === "ECONNREFUSED") {
        Swal.fire({
          icon: "error",
          title: "Server Unavailable",
          text: "The server is currently unavailable. Please try again later.",
          confirmButtonText: "OK",
          showCloseButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
        }).then(() => {
          errorPopupShown = false; 
        });
      } else if (error.code==="ERR_NETWORK"|| error.code === "ERR_ADDRESS_UNREACHABLE") {
      Swal.fire({
        icon: "error",
        title: "Server Unavailable",
        text: "The server is currently unavailable. Please try again later.",
        confirmButtonText: "OK",
        showCloseButton: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
      }).then(() => {
        errorPopupShown = false; 
      });
    } else if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        Swal.fire({
          icon: "error",
          title: "Unauthorized",
          text: "You are not authorized to access this resource.",
          confirmButtonText: "OK",
          showCloseButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
        }).then(() => {
          errorPopupShown = false; 
        });
      }
      else if (status === 404) {
        Swal.fire({
          icon: "error",
          title: "Not Found",
          text: "The requested resource was not found on the server.",
          confirmButtonText: "OK",
          showCloseButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
        }).then(() => {
          errorPopupShown = false; 
        });
      } else if (status === 500) {
        Swal.fire({
          icon: "error",
          title: "Internal Server Error",
          text: "An internal server error occurred. Please try again later.",
          confirmButtonText: "OK",
          showCloseButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
        }).then(() => {
          errorPopupShown = false; 
        });
      } else if (status === 200 && error.response.data.status === "error") {
        Swal.fire({
          icon: "error",
          title: "API Error",
          text: "An error occurred while processing the request.",
          confirmButtonText: "OK",
          showCloseButton: false,
          allowOutsideClick: false,
          allowEscapeKey: false,
        }).then(() => {
          errorPopupShown = false; 
        });
      } else {
        console.error(`HTTP error with status code ${status}:`, error.response.data);
      }
    }
    else if (error instanceof TypeError) {
        Swal.fire({
            icon: "error",
            title: "Server Unavailable",
            text: "The server is currently unavailable. Please try again later.",
            confirmButtonText: "OK",
            showCloseButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
          }).then(() => {
            errorPopupShown = false; 
          });
      }
    else if (error.message && error.message.startsWith && error.message.startsWith("cannot read properties of")) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "An error occurred while processing. Please check your input.",
        confirmButtonText: "OK",
        showCloseButton: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
      }).then(() => {
        errorPopupShown = false; 
      });
    }
    else {
      console.error("Unhandled error:", error);
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "An error occurred while processing.",
        confirmButtonText: "OK",
        showCloseButton: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
      }).then(() => {
        errorPopupShown = false;
      });
    }

  }
};

export default handleApiError;
