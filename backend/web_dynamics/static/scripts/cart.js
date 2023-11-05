$(document).ready(function (){
    cart = JSON.parse(localStorage.getItem("cart"))
    if (cart)
        renderCart(cart)



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
                            cart = {
                                total: data.cart.data.total,
                                items: data.cart.items
                            }
                            renderCart(cart);
                            localStorage.setItem("cart", JSON.stringify(cart))
                        })
                } else {
                    let cart = JSON.parse(localStorage.getItem("cart")) || {};
                    let items = inCart(productId, cart.items ?? [])
                    if (!items.length){
                        $.ajax(apiUrl + "/products/" + productId).done(function (data) {
                            items = cart.items ?? []
                            let product = data.data
                            product.image = product.images[0]
                            product.images = null
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
