const App = {
    startUp: () => {
        App.addFormListener();
        App.loader();
        let gal = document.querySelector(".owl-carousel");
        if (gal != null) {
            $(gal).owlCarousel({
                loop:true,
                margin:10,
                nav:true,
                navText: ['<i class="ti-angle-left"></i>', '<i class="ti-angle-right"></i>'],
                responsive:{
                    0:{
                        items:1
                    },
                }
            })
        }
    },
    loader: () => {
        $(window).on('load', function(event) {
            $('.preloader').delay(500).fadeOut(500);
        });
    },
    addFormListener: () => {
        let form = document.querySelector(".form-data");
        if (form != null) {
            form.addEventListener("submit", (ev) => {
                ev.preventDefault();
                let method = form.getAttribute("method");
                let action = form.getAttribute("action");
                let formData = new FormData(form);
                fetch(action, {
                    method: method,
                    body: formData
                }).then((response) => {
                    App.responseHandler(response);
                })
            });
        }
    },
    responseHandler: (response) => {
        if (response.status === 200 || response.status === 201) {
            response.json().then((jsonResponse) => App.onFormSuccess(jsonResponse));
        } else if (response.status === 401) {
            App.onNotAuth();
        } else if (response.status === 403) {
            response.json().then((jsonResponse) => App.onForbidden(jsonResponse));
        } else if (response.status === 500) {
            App.onServerError();
        } else {
            response.json().then((jsonResponse) => App.onFormError(jsonResponse));
        }
    },
    onFormError: (response) => {
        Swal.fire({
            text: response.message,
            icon: 'error',
        });
    },
    onNotAuth: () => {
        Swal.fire({
            title: 'Oops...',
            text: 'Entre no sistema para realizar esta ação.',
            icon: 'warning',
        });
    },
    onForbidden: (response) => {
        Swal.fire({
            title: 'Oops...',
            text: response.message,
            icon: 'warning',
        });
    },
    onServerError: () => {
        Swal.fire({
            title: 'Oops...',
            text: 'Ocorreu um erro no servidor, tente novamente mais tarde.',
            icon: 'error',
        });
    },
    onFormSuccess: (response) => {
        Swal.fire({
            title: response.message,
            timer: 2000,
            icon: 'success',
        }).then(() => {
            if (response.redirect && response.redirect.length > 0) {
                setTimeout(() => {
                    window.location.href = response.redirect;
                },300);
            }
        });
    },
};

(function () {
    App.startUp();
})();