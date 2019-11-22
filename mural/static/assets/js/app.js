const App = {
    startUp: () => {
        App.addFormListener();
        App.addDeleteListener();
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
    addDeleteListener: () => {
        let del = document.querySelectorAll("[data-delete]");
        if (del.length > 0) {
            for (let i = 0; i < del.length; i++) {
                let d = del[i];
                d.addEventListener("click", (ev) => {
                    if (confirm("Tem certeza que dejesa remover?")) {
                        let url = d.getAttribute("data-delete");
                        fetch(url, {
                            method: 'delete'
                        }).then((response) => {
                            App.responseHandler(response);
                        });
                    }
                });
            }
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
        alert(response.message);
    },
    onNotAuth: () => {
        alert('não logado');
    },
    onForbidden: (response) => {
        alert(response.message);
    },
    onServerError: () => {
        alert('erro no servidor, tente mais tarde');
    },
    onFormSuccess: (response) => {
        alert(response.message);
        if (response.redirect && response.redirect.length > 0) {
            setTimeout(() => {
                window.location.href = response.redirect;
            },300);
        }
    },
};

(function () {
    App.startUp();
})();