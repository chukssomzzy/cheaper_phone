$(document).ready(function (){
    /*
        Add to cart
        ==========
        ==========
        */

        $(".product").each(function (idx) {
            const productId = $(this).data("id")
            let NigeriaNira = new Intl.NumberFormat('en-US', {minimumFractionDigits:2})
            $(this).find(".product__btn").on("click", function(e){
                e.stopPropagation();

                if (isLoggedIn) {
                    $.ajax(apiUrl + "/customer/cart/" + productId,
                        {type: "POST",
                        })
                        .done(function (data){
                            const cartItem = data.cart.items.map((item) => `
                                <div class="box">
                                <i class="fas fa-trash"></i>
                                <img src="${item.product.image.image_url}" alt="${ item.product.image.alt_text }" />
                                <div class="content">
                                <h3>${ item.product.name }</h3>
                                <span class="price">₦${ NigeriaNira.format(Number(item.product.price)) }/-</span>
                                <span class="quantity">qty : ${ item.quantity}</span>
                                </div>
                                </div>
                                `)
                            const cartTotal = `<div class="total">₦${NigeriaNira.format(Number(data.cart.data.total_price))} /-</div>
                                <a href="#" class="btn">Check out</a>
                                `
                            cartItem.push(cartTotal)
                            $("#shopping-cart-id").html(cartItem.join())
                            $("#cart__total").text(data.cart.items.length)
                        })
                } else {
                    /* --- get product --- */
                        $.ajax(apiUrl + "/product/" + productId).done(function (data) {
                            console.log(data)
                        })
                }
            })
        })
})
