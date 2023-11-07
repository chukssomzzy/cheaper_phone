const apiUrl = "http://localhost:5000/api/v1"
const NigeriaNira = new Intl.NumberFormat('en-US', {minimumFractionDigits:2})
const renderCart = (cart) => {
    if (cart) {
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

