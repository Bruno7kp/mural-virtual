(function() {
    let cep = document.querySelectorAll('.mask-cep');
    for (let i = 0; i < cep.length; i++) {
        IMask(cep[i], {
            mask: '00000-000',
        });
    }

    let phone = document.querySelectorAll('.mask-phone');
    for (let i = 0; i < phone.length; i++) {
        let dispatchMask = IMask(phone[i], {
                mask: [
                    {
                        mask: '(00) 0000-0000',
                        phone: false,
                    },
                    {
                        mask: '(00) 00000-0000',
                        phone: true,
                    },
                ],
                dispatch: function (appended, dynamicMasked) {
                    let number = (dynamicMasked.value + appended).replace(/\D/g,'');
                    let phone = number.length > 10;
                    return dynamicMasked.compiledMasks.find(function (m) {
                        return m.phone === phone;
                    });
                }
            }
        )
    }

    let cpf = document.querySelectorAll('.mask-cpf');
    for (let i = 0; i < cpf.length; i++) {
        IMask(cpf[i], {
            mask: '000.000.000-00',
        });
    }
})();
