const NigeriaNira = new Intl.NumberFormat('en-US', {minimumFractionDigits:2})
const renderCart = (cart) => {
    if (cart && cart.items.length > 0) {
        const cartItem = cart.items.map((item) => {
            return `<div class="box">
                <i class="fas fa-trash"></i>
                <img src="${item.product.image.image_url}" alt="${ item.product.image.alt_text }" />
                <div class="content">
                <h3>${ item.product.name }</h3>
                <span class="price">₦${ NigeriaNira.format(Number(item.product.price)) }/-</span>
                <span class="quantity">qty : ${ item.quantity ?? 1}</span>
                </div>
                </div>
                `
        })
        const cartTotal = `<div class="total">₦${NigeriaNira.format(Number(cart.total))} /-</div>
            <a href="/customer/cart" class="btn check-out">Check out</a>
            `
        cartItem.push(cartTotal)
        $("#shopping-cart-id").html(cartItem.join())
        $("#cart__total").text(cart.items.length)
    }else {
        $("#shopping-cart-id").html(`<div class="box">
            <svg
            xmlns="http://www.w3.org/2000/svg"
            height="3em"
            viewBox="0 0 576 512"
            >
            <!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
            <path
            d="M0 24C0 10.7 10.7 0 24 0H69.5c22 0 41.5 12.8 50.6 32h411c26.3 0 45.5 25 38.6 50.4l-41 152.3c-8.5 31.4-37 53.3-69.5 53.3H170.7l5.4 28.5c2.2 11.3 12.1 19.5 23.6 19.5H488c13.3 0 24 10.7 24 24s-10.7 24-24 24H199.7c-34.6 0-64.3-24.6-70.7-58.5L77.4 54.5c-.7-3.8-4-6.5-7.9-6.5H24C10.7 48 0 37.3 0 24zM128 464a48 48 0 1 1 96 0 48 48 0 1 1 -96 0zm336-48a48 48 0 1 1 0 96 48 48 0 1 1 0-96z"
            />
            </svg>
            <div class="content">
            <h2>Your Cart is currently empty</h2>
            </div>
            </div>  `)
    }
}

/** Mutation Observer **/

    const config = {attributes: true, childList: true, subtree: true};

const observe = (callback, targetNode) => {
    const observer = new MutationObserver(callback)
    observer.observe(targetNode, config)
}

// check if product is already in cart
const inCart = (productId, items)=> {
    const product = items.find(item => (item.product.id == productId))
    if (product) {
        items = items.map((item) => {
            if (item.product.id === productId)
                item.quantity = item.quantity ? item.quantity + 1 : 1;
            return item;
        })
        return items
    }
    return []
}



const itemsTotal = (items) => {
    return (items.reduce((prevTotal, item) => {
        price = Number(item.product.price)
        quantity = item.quantity ?? 1
        return prevTotal + (price * quantity)
    }, 0))
}

const removeFromCart = (removeSelector) => {
    /** Decrease A product **/

        $(removeSelector).on("click", function(e) {
            productId = $(this).data("id")
            $.ajax(apiUrl + "/customer/cart/" + productId, {
                type: "PUT",
            }).done(function (data){
                cart = {
                    total: data.cart.data.total_price,
                    items: data.cart.items
                }
                renderCartPage(cart)
                renderCart(cart)
                localStorage.setItem("cart", JSON.stringify(cart))
            })
        })
}

const increaseCartQuantity = (increaseSelector) => {
    /** increase cart quatity **/

        $(increaseSelector).on("click", function(e) {
            productId = $(this).data("id")
            $.ajax(apiUrl + "/customer/cart/" + productId, {
                type: "POST"
            }).done(function (data) {
                cart = {
                    total: data.cart.data.total_price,
                    items: data.cart.items
                }
                renderCartPage(cart)
                renderCart(cart)
                localStorage.setItem("cart", JSON.stringify(cart))
            })
        })
}
const deleteFromCart = (deleteSelector) => {
    /** delete product from cart **/
        $(deleteSelector).on("click", function(e) {
            e.preventDefault()
            e.stopPropagation()
            const productId = $(this).data("id")
            $.ajax(apiUrl + "/customer/cart/" + productId, {
                type: "DELETE"
            }).done(function (data) {
                cart = {
                    total: data.cart.data.total_price,
                    items: data.cart.items
                }
                renderCartPage(cart)
                renderCart(cart)
                localStorage.setItem("cart", JSON.stringify(cart))
            })
        })
}

