$(document).ready(function (){
    /*
        ===========
        Add to cart
        ===========
        */
        /** cart object
        ** items: array of items
        ** total: total price of items in cart
        **/
        /**
        ** product: (dict repr of product)
        ** quantity: (dict representation of quantity)
        **/

        $(".product").each(function (idx) {
            const productId = $(this).data("id")
            $(this).find(".product__btn").on("click", function(e){
                e.stopPropagation();
                e.preventDefault();

                if (isLoggedIn()) {
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
                    let cart = JSON.parse(localStorage.getItem("cart")) || {};
                    let items = inCart(productId, cart.items ?? [])
                    if (!items.length){
                        $.ajax(apiUrl + "/products/" + productId).done(function (data) {
                            items = cart.items ?? []
                            const product = data.data
                            const item = {
                                product
                            }

                            items = [item, ...items]
                            total = itemsTotal(items)
                            cart = {items, total}
                            renderCart(cart);
                            localStorage.setItem("cart", JSON.stringify(cart))
                        })
                    } else {
                        cart.total = itemsTotal(items)
                        cart.items = items;
                        renderCart(cart);
                        localStorage.setItem("cart", JSON.stringify(cart))
                    }
                }
            })
        })
})

// check if product is already in cart
const inCart = (productId, items)=> {
    const product = items.find(item => (item.product.id == productId))
    if (product) {
        items = items.map((item) => {
            if (item.product.id === productId)
                item.quantity = item.quantity ? item.quantity + 1 : 1;
            return item;
        })
        console.log(items)
        return items
    }
    return []
}

const renderCart = (cart) => {
    const cartItem = cart.items.map((item) => `
        <div class="box">
        <i class="fas fa-trash"></i>
        <img src="${item.product.images[0].image_url}" alt="${ item.product.images[0].alt_text }" />
        <div class="content">
        <h3>${ item.product.name }</h3>
        <span class="price">₦${ NigeriaNira.format(Number(item.product.price)) }/-</span>
        <span class="quantity">qty : ${ item.quantity ?? 1}</span>
        </div>
        </div>
        `)
    const cartTotal = `<div class="total">₦${NigeriaNira.format(Number(cart.total))} /-</div>
        <a href="#" class="btn">Check out</a>
        `
    cartItem.push(cartTotal)
    $("#shopping-cart-id").html(cartItem.join())
    $("#cart__total").text(cart.items.length)
}

const itemsTotal = (items) => {
    return (items.reduce((prevTotal, item) => {
        price = Number(item.product.price)
        quantity = item.quantity ?? 1
        return prevTotal + (price * quantity)
    }, 0))
}
