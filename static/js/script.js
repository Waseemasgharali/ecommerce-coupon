/*==increase-cart-quanity========================*/
$('.increase-cart-quanity').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    $.ajax({
        type: "GET",
        url: "pluscart",
        data: {
            cart_id: id
        },
        success: function (data){
            eml.innerText = data.quantity;
            document.getElementById("subtotal-amount").innerText = data.total_amount.toFixed(2);
        }
    });
});


/*==decrese-cart-quanity===============*/
$('.decrease-cart-quanity').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[1];
    $.ajax({
        type: "GET",
        url: "minuscart",
        data: {
            cart_id: id
        },
        success: function (data){
            eml.innerText = data.quantity;
            document.getElementById("subtotal-amount").innerText = data.total_amount.toFixed(2);
        }
    });
});


/*==Remove-Cart===============*/
$('.removecart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "removecart",
        data: {
            cart_id: id
        },
        success: function (data){
            document.getElementById("subtotal-amount").innerText = data.total_amount.toFixed(2);
            eml.parentNode.parentNode.remove();
        }
    });
});

/*==Apply Coupon================*/
$('#apply-coupon-btn').click(function(){
    var couponCode = $('#coupon-code').val(); // Update to match your input field ID
    $.ajax({
        type: "POST",
        url: "{% url 'apply_coupon' %}",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            coupon_code: couponCode
        },
        success: function (data){
            if (data.success) {
                // Coupon applied successfully
                alert(data.message);
                // Update the total amount displayed on the page
                document.getElementById("subtotal-amount").innerText = data.total_amount.toFixed(2);
            } else {
                // Invalid coupon code
                alert(data.message);
            }
        },
        error: function(xhr, status, error) {
            alert("An error occurred while applying the coupon. Please try again.");
            console.log(xhr.responseText);
        }
    });
});
