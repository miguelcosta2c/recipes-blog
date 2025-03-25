function myScope () {
    const FORMS = document.querySelectorAll('.form-delete');
    for (const FORM of FORMS) {
        FORM.addEventListener('submit', function(e) {
            e.preventDefault();
            const CONFIRMED = confirm('Are you sure?');
            if (CONFIRMED) {
                FORM.submit();
            };
        }
        );
    };
};

myScope()