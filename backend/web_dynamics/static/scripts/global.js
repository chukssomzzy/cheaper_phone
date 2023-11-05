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
            <a href="#" class="btn">Check out</a>
            `
        cartItem.push(cartTotal)
        $("#shopping-cart-id").html(cartItem.join())
        $("#cart__total").text(cart.items.length)
    }
}
