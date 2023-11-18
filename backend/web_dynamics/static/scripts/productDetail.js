$(document).ready(function () {
    if (!isLoggedIn())
    {
        const cart = JSON.parse(localStorage.getItem("cart"))
        const productId = $("main").data("id")
        renderProduct(cart, productId)
    }
    $(".plus-btn").on("click", function (e) {
        e.preventDefault()
        e.stopPropagation()
        const productId = $(this).data("id")
        if (isLoggedIn()) {
            $.ajax(apiUrl + "/customer/cart/" + productId,
                {type: "POST",
                })
                .done(function (data){
                    cart = {
                        total: data.cart.data.total_price,
                        items: data.cart.items
                    }
                    const item = cart.items.find((item)=> item.product.id === productId)
                    console.log(item.subtotal)
                    $("li a.new__price").text("₦" + NigeriaNira.format(item.subtotal))
                    $(".input-counter .counter-btn").val(item.quantity)
                    renderCart(cart)
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
                    renderProduct(cart, productId);
                    localStorage.setItem("cart", JSON.stringify(cart))
                })
            } else {
                cart.total = itemsTotal(items)
                cart.items = items;
                renderProduct(cart, productId);
                localStorage.setItem("cart", JSON.stringify(cart))
            }
        }
    })
    $(".input-counter .minus-btn").on("click", function(e){
        e.preventDefault()
        productId = $(this).data("id")
        if (isLoggedIn()) {
            $.ajax(apiUrl + "/customer/cart/" + productId, {
                type: "PUT",
            }).done(function (data){
                cart = {
                    total: data.cart.data.total_price,
                    items: data.cart.items
                }
                const item = cart.items.find((item)=> item.product.id === productId)
                $("li a.new__price").text("₦" + NigeriaNira.format(item.subtotal))
                $(".input-counter .counter-btn").val(item.quantity)
                renderCart(cart)
                localStorage.setItem("cart", JSON.stringify(cart))
            })
        } else {
            let cart = JSON.parse(localStorage.getItem("cart")) || {};
            cart = reduceOrRemove(cart, productId)

            renderProduct(cart, productId);
            localStorage.setItem("cart", JSON.stringify(cart))
        }
    })

})

const renderProduct = (cart, productId) => {
    if (cart) {
        const item = cart?.items?.find(item=> item.product.id === productId)
        const total = itemsTotal(cart?.items)
        cart.total = total
        renderCart(cart)
        if (item) {
            $("li a.new__price").text("₦" + NigeriaNira.format(Number(item.product?.price) * Number(item?.quantity || 1)))
            $(".input-counter .counter-btn").val(item?.quantity || 1)
        }
        localStorage.setItem("cart", JSON.stringify(cart))
    }
}

const reduceOrRemove = (cart, productId) => {
    if (cart && cart.items) {
        items = cart.items.map(item => {
            if (item.product.id == productId)
                item.quantity = item.quantity ? (item.quantity - 1) : 0
            return item
        }).filter(item => item.quantity)
        total = itemsTotal(items)
        return {items, total}
    }
    return null
}
