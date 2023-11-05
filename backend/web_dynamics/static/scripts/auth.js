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
      error: (xhr, msg) => console.log(msg)
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
        console.log("click")
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        $.ajax("/logout").done(function(){
            console.log("done")
            location.reload()
        })
    })




})

const setupLogin = () => {
  const logoutBtn = `<a class="nav__logout logout__section" href="/logout">
          logout
        <a>`
  $('#logout__section').html(logoutBtn)
  $('#login-btn').css('display', 'none')
}

const loginApiUser = function (formData) {
  if (!localStorage.getItem('accessToken')) {
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
      }

    })
  }
}

var isLoggedIn = () => (!!localStorage.getItem("accessToken"))
