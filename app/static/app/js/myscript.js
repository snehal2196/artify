$("#slider1, #slider2, #slider3").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: false,
      autoplay: true,
    },
    600: {
      items: 3,
      nav: true,
      autoplay: true,
    },
    1000: {
      items: 5,
      nav: true,
      loop: true,
      autoplay: true,
    },
  },
});

$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var elm = this.parentNode.children[2];
  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      id: id,
    },
    success: function (data) {
      elm.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText = data.total_amount;
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var elm = this.parentNode.children[2];
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      id: id,
    },
    success: function (data) {
      elm.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText = data.total_amount;
    },
  });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var elm = this;
  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      id: id,
    },
    success: function (data) {
      console.log("delete");
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText = data.total_amount;
      elm.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});
// MY SCRIPT
$(document).ready(function () {
  $(".filter-button").click(function () {
    var value = $(this).attr("data-filter");

    if (value == "all") {
      $(".filter").show("1000");
    } else {
      $(".filter")
        .not("." + value)
        .hide("3000");
      $(".filter")
        .filter("." + value)
        .show("3000");
    }

    if ($(".filter-button").removeClass("active")) {
      $(this).removeClass("active");
    }
    $(this).addClass("active");
  });
});


jQuery(function($) {
  var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
  $('ul a').each(function() {
   if (this.href === path) {
    $(this).addClass('active');
   }
  });
 });

 $(".add-to").click(function(){
   var id = $(this).attr("pid").toString();
   console.log(id)
   $.ajax({
     type: 'GET',
     url: '/add-to-cart/',
     data:{
       id:id
     },
     success:function(data){
       console.log(data)
       document.getElementById('totalitems').innerText = data.totalitems;
       if (data.in_cart){
        document.getElementById('addtocart').style.display = 'none';
        document.getElementById('gotocart').style.display = 'block';
       }
       
       
     }
   })

 });