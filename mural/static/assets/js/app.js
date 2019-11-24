const App = {
    startUp: () => {
        App.addFormListener();
        let fixClick = document.querySelector("[data-toggle=\"dropdown\"]");
        if (fixClick != null) {
            // Pra resolver o problema de ter que dar clique duplo pra abrir o menu, já deixamos um clique ao abrir a página
            fixClick.click();
        }
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