

$(document).ready(function() {
    const loc = document.location;
    console.log(loc)
    if (loc.hash === "#login-btn") {
            login.classList.toggle('active');
            searchForm.classList.remove('active');
            shoppingCart.classList.remove('active');
    }
})
