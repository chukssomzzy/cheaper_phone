$(document).ready(function (){
 /** Cart Details Page */

        /** Decrease A product **/
        removeFromCart("span.minus-btn")
    observe(((removeFromCart("span.minus-btn"))()), $("tbody.product__content")[0])
    increaseCartQuantity("span.plus-btn")
    observe(((increaseCartQuantity("span.plus-btn"))()), $("tbody.product__content")[0])
    deleteFromCart()
    observe(((deleteFromCart("a.remove__cart-item"))()), $("tbody.product__content")[0])
})


 const renderCartPage = (cart) => {
    if (cart) {
        const cartProduct = cart.items.map((item) => `
            <tr>
            <td class="product__thumbnail">
            <a href="/product/${ item.product.id }">
            <img src="${ item.product.image.image_url }" alt="${ item.product.image.alt_text }">
            </a>
            </td>
            <td class="product__name">
            <a href="#">${ item.product.name.slice(0, 20) }</a>
            <br><br>
            <small>${ item.product.brand && item.product.brand.name || "" }</small>
            </td>
            <td class="product__price">
            <div class="price">
            <span class="new__price">₦${ NigeriaNira.format(item.product.price) }</span>
            </div>
            </td>
            <td class="product__quantity">
            <div class="input-counter">
            <div>
            <span class="minus-btn" data-id="${ item.product.id }">
            <svg>
            <use xlink:href="/static/images/sprite.svg#icon-minus"></use>
            </svg>
            </span>
            <input value="${ item.quantity }" type="text" min="1"  max="10" class="counter-btn">
            <span class="plus-btn" data-id="${ item.product.id }">
            <svg>
            <use xlink:href="/static/images/sprite.svg#icon-plus"></use>
            </svg>
            </span>
            </div>
            </div>
            </td>
            <td class="product__subtotal">
            <div class="price">
            <span class="new__price">₦${ NigeriaNira.format(item.subtotal) }</span>
            </div>
            <a href="/customer/cart/${item.product.id}" class="remove__cart-item" data-id="${item.product.id}">
            <svg>
            <use xlink:href="/static/images/sprite.svg#icon-trash"></use>
            </svg>
            </a>
            </td>
            </tr>
            `)
        $("tbody.product__content").html(cartProduct.join())
        $("span.new__price.total").text("₦" + NigeriaNira.format(cart.total))
    }
}


