$(document).ready(function () {
  const emailRe = /.*?@.*?[.].{2,6}/
  const loc = document.location
  if (loc.hash === '#login-btn') {
    $('.login-form').toggleClass('active')
    $('.shopping-cart').removeClass('active')
  }

  /*
        =============
        PopUp
        =============
*/

  $('.popup__close').on('click', () => {
    $('.popup').addClass('hide__popup')
  })

  if (loc.hash !== '#login-btn') {
    setTimeout(() => {
      $('.popup').removeClass('hide__popup')
    }, 500)
  }

  /*
        =============
        login a user
        =============
        */

  $('#form-login').on('submit', function (e) {
    const formData = {
      password: $('.login__password').val()
    }
    if ($('.login__email').val().match(emailRe)) {
      formData.email = $('.login__email').val()
    } else {
      formData.username = $('.login__email').val()
    }
    $.ajax({
      type: 'POST',
      url: '/login',
      data: formData,
      dataType: 'json',
      encode: true,
        error: (xhr, msg) => notifier.warning("Incorrect Username or Password", {duration: {warning: 1000}})
    }).done(function () {
      loginApiUser(formData)
      $(this).removeClass('active')
        setupLogin()
    }.bind(this))
    e.preventDefault()
  })

    /* Logout callback */
        $('.logout__section').on('click', function(e) {
        e.preventDefault()
        e.stopPropagation()
            $.ajax("/logout").done(function(){

            localStorage.removeItem("accessToken")
            location.reload()
        })
    })




})

const setupLogin = () => {
  const logoutBtn = `<a class="nav__logout logout__section" href="/logout">
          logout
        <a>`
    console.log(cart)
  $('#logout__section').html(logoutBtn)
  $('#login-btn').css('display', 'none')
}

const loginApiUser = function (formData) {
  if (!isLoggedIn()) {
    $.ajax(apiUrl + '/customer/login', {
      type: 'POST',
      dataType: 'json',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: function (response) {
        accessToken = response.access_token
        refreshToken = response.refresh_token

        localStorage.setItem('accessToken', accessToken)
          localStorage.setItem('refreshToken', refreshToken)
        setupCart()
      }

    })
  }
}

var isLoggedIn = () => (!!localStorage.getItem("accessToken"))
var setupCart = () => {
    $.ajax(apiUrl + "/customer/cart").done(function (data) {
        cart = {
            items: data.items,
            total: data.data.total
        }
        localStorage.setItem("cart", JSON.stringify(cart))
        renderCart(cart)
    })
}
