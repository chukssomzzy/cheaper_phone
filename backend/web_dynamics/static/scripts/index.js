$(document).ready(function () {
/*
    =============
    Navigation
    =============
    */
const navOpen = $(".nav__hamburger");
const navClose = $(".close__toggle");
const menu = $(".nav__menu");
const scrollLink = $(".scroll-link");
const navContainer = $(".nav__menu");

navOpen.on("click", () => {
    menu.addClass("open");
    $(this).addClass("active");
    navContainer[0].style.left = '0';
    navContainer[0].style.width = "30rem"
});

navClose.on("click", () => {
    menu.removeClass("open");
    $(this).removeClass("active");
    navContainer[0].style.left = "-30rem";
    navContainer[0].style.width = 0;
});


/*
    =============
    Fixed Navigation
    =============
    */

const navBar = $(".navigation");
const gotoTop = $(".goto-top");
// Smooth Scroll
scrollLink.each(function(idx) {
    $(this).on("click", e => {
        // Prevent Default
        e.preventDefault();

        const id = e.currentTarget.getAttribute("href").slice(1);
        const element = document.getElementById(id);
        const navHeight = navBar.height();
        const fixNav = navBarhasClass("fix__nav");
        let position = element.offsetTop - navHeight;

        if (!fixNav) {
            position = position - navHeight;
        }

        window.scrollTo({
            left: 0,
            top: position,
        });
        navContainer.css(left , "-30rem");
        document.body.classList.remove("active");
    });
});

// Fix NavBar

window.addEventListener("scroll", e => {
    const scrollHeight = window.scrollY;
    const navHeight = navBar.height();
    if (scrollHeight > navHeight) {
        navBaraddClass("fix__nav");
    } else {
        navBar.removeClass("fix__nav");
    }

    if (scrollHeight > 300) {
        gotoTop.addClass("show-top");
    } else {
        gotoTop.addClass("show-top");
    }
});

let login = $('.login-form');

if ($("#login-btn")) {
    $('#login-btn').onclick=()=>{
        login.toggle('active');
        searchForm.removeClass('active');
        if (shoppingCart)
            shoppingCart.removeClass('active');

    }
}

let shoppingCart=$('.shopping-cart');

cartBtn = $("#cart-btn")
if (cartBtn) {
    cartBtn.on("click", (e)=>{
        e.stopPropagation()
        shoppingCart.toggle('active');
        searchForm.removeClass('active');
        if (login)
            login.removeClass('active');
    })
}

let searchForm=$('.search-form');

$('#search-btn').onclick=()=>{
    searchForm.toggle('active');
    shoppingCart.removeClass('active');
    if (login)
        login.removeClass('active');
}
})
