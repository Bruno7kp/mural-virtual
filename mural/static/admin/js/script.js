const App = {
    init: () => {
        App.loadTable();
        App.addFormListener();
        App.addDeleteListener(() => {});
        App.addTextEditor();
        App.addSort();
        App.loader();
    },
    loader: () => {
        $(window).on('load', function(event) {
            $('.preloader').delay(500).fadeOut(500);
        });
    },
    openLoader: () => {
        console.log('open');
        $('.preloader').fadeIn(100);
    },
    closeLoader: () => {
        $('.preloader').fadeOut(0);
    },
    addSort: () => {
        let sort = document.querySelector('[data-sort]');
        if (sort != null) {
            let sorturl = sort.getAttribute('data-sort');
            let sortable = new Sortable(sort, {
                swapThreshold: 0.50,
                animation: 150,
                filter: '[data-delete]',
                onUpdate: function (evt) {
                    let formData = new FormData();
                    formData.append('ordem', sortable.toArray());
                    fetch(sorturl, {
                        method: 'post',
                        body: formData
                    }).then((response) => {
                        if (response.status !== 200) {
                            App.responseHandler(response);
                        }
                    })
                },
            });
        }
    },
    addTextEditor: () => {
        let textarea = document.querySelector('#conteudo');
        if (textarea != null) {
            let editor = CKEDITOR.replace( 'conteudo', {
                language: 'pt-br',
            });
            editor.on( 'change', function( evt ) {
                textarea.value = evt.editor.getData()
            });
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
                App.openLoader();
                fetch(action, {
                    method: method,
                    body: formData
                }).then((response) => {
                    App.responseHandler(response);
                    App.closeLoader();
                })
            });
        }
    },
    addDeleteListener: (call) => {
        let del = document.querySelectorAll("[data-delete]");
        if (del.length > 0) {
            for (let i = 0; i < del.length; i++) {
                let d = del[i];
                d.addEventListener("click", (ev) => {
                    Swal.fire({
                        title: "Tem certeza que dejesa remover?",
                        icon: 'warning',
                        showCancelButton: true,
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Sim, remova!',
                        cancelButtonText: 'Cancelar',
                    }).then((result) => {
                        if (result.value) {
                            App.openLoader();
                            let url = d.getAttribute("data-delete");
                            fetch(url, {
                                method: 'delete'
                            }).then((response) => {
                                call();
                                App.responseHandler(response);
                                App.closeLoader();
                            });
                        }
                    });
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
    dataTableLang: () => {
        return {
            "sEmptyTable": "Nenhum registro encontrado",
            "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
            "sInfoFiltered": "(Filtrados de _MAX_ registros)",
            "sInfoPostFix": "",
            "sInfoThousands": ".",
            "sLengthMenu": "_MENU_ resultados por página",
            "sLoadingRecords": "Carregando...",
            "sProcessing": "Processando...",
            "sZeroRecords": "Nenhum registro encontrado",
            "sSearch": "Pesquisar",
            "oPaginate": {
                "sNext": "Próximo",
                "sPrevious": "Anterior",
                "sFirst": "Primeiro",
                "sLast": "Último"
            },
            "oAria": {
                "sSortAscending": ": Ordenar colunas de forma ascendente",
                "sSortDescending": ": Ordenar colunas de forma descendente"
            },
            "select": {
                "rows": {
                    "_": "Selecionado %d linhas",
                    "0": "Nenhuma linha selecionada",
                    "1": "Selecionado 1 linha"
                }
            }
        }
    },
    loadTable: () => {
        let table = document.querySelector("[data-table-url]");
        if (table != null) {
            let url = table.getAttribute("data-table-url");
            App.datatable = $(table).DataTable( {
                "ajax": url,
                "processing": true,
                "serverSide": true,
                "ordering": false,
                "language": App.dataTableLang()
            });
            $(table).on('draw.dt', function () {
                App.addDeleteListener(() => App.datatable.ajax.reload());
            });
        }
    },
};

(function() {
   App.init();
})();
