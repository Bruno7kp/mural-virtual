(function() {
    let cep = document.querySelectorAll('.mask-cep');
    for (let i = 0; i < cep.length; i++) {
        IMask(cep[i], {
             mask: '00000-000',
        });
    }

    let phone = document.querySelectorAll('.mask-phone');
    for (let i = 0; i < phone.length; i++) {
        IMask(phone[i], {
             mask: '(00) 00000-0000',
        });
    }

    let cpf = document.querySelectorAll('.mask-cpf');
    for (let i = 0; i < cpf.length; i++) {
        IMask(cpf[i], {
             mask: '000.000.000-00',
        });
    }
})();
