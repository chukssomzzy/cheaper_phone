$(document).ready(function() {
    const loc = document.location;
    if (loc.hash === "#login-btn") {
        $(".login-form").toggleClass('active');
        $(".shopping-cart").removeClass('active');
    }

    /*
        =============
        PopUp
        =============
        */

        $(".popup__close").on("click", () => {
            $(".popup").addClass("hide__popup");
        });

    if (loc.hash !== "#login-btn"){
        setTimeout(() => {
            $(".popup").removeClass("hide__popup");
        }, 500);
    }

    /*
        =============
        login a user
        =============
        */
        $("#form-login").on("submit", function(e) {
            const formData = {
                email: $(".login__email").val(),
                password: $(".login__password").val()
            }

            $.ajax({
                type: "POST",
                url: "/login",
                data: formData,
                dataType: "json",
                encode: true,
                error: (msg) => console.log(msg)
            }).done(function (data) {
                console.log(data)
            })
            $(this).removeClass("active");
            e.preventDefault()
        })

})
