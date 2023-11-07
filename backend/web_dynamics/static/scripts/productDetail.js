$(document).ready(function () {
    if (!isLoggedIn())
    {
        const cart = JSON.parse(localStorage.getItem("cart"))
        const productId = $("main").data("id")
        renderProduct(cart, productId)
    }
    $(".product-details__btn .add").on("click", function (e) {
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
    if (isLoggedIn()) {
        $(".input-counter .minus-btn").on("click", function(e){
            e.preventDefault()
            productId = $(this).data("id")
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
        })
        $(".input-counter .plus-btn").on("click", function (e){
            e.preventDefault()
            productId = $(this).data("id")
            $.ajax(apiUrl + "/customer/cart/" + productId, {
                type: "POST"
            }).done(function (data) {
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
        })
    } else {
        $(".input-counter .plus-btn").on("click", function (e){
            e.preventDefault()
            const productId = $(this).data("id")
            let cart = JSON.parse(localStorage.getItem("cart")) || {items: []}
            let items = inCart(productId, cart.items)
            let total = 0
            let item = {}
            if (!items.length) {
                $.ajax(apiUrl + "/products/" + productId).done(function (data){
                    let product = data.data
                    product.image = product.images[0]
                    product.images = null
                    item = {product, quantity: 1}
                    items = [item, ...items]
                    renderProduct(cart, productId)
                })
            }
            renderProduct(cart, productId)
        })

    }
})

const renderProduct = (cart, productId) => {
    const item = cart?.items?.find(item=> item.product.id === productId)
    const total = itemsTotal(cart?.items)
    cart.total = total
    renderCart(cart)
    $("li a.new__price").text("₦" + NigeriaNira.format(Number(item.product?.price) * Number(item?.quantity)))
    $(".input-counter .counter-btn").val(item?.quantity)
    localStorage.setItem("cart", JSON.stringify(cart))
}
