window.ShowToastr = (type, message) => {

    toastr.options.toastClass = "toastr";

    if (type === "success") {
        toastr.success(message, "Operación satisfactoria", { timeOut: 3000 });
    }
    if (type === "error") {
        toastr.error(message, "Operación fallida", { timeOut: 3000 });
    }
};