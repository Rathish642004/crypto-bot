function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Utility function to check if CSRF protection is needed
function csrfSafeMethod(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

// Function to send AJAX request
function sendAjaxRequest(url, data, successCallback, errorCallback) {
  $.ajax({
      type: "POST",
      url: url,
      data: data,
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
          }
      },
      success: successCallback,
      error: errorCallback
  });
}

$(document).ready(function() {
  $("#buy").click(function() {
      var symbol = $("#symbol").val();
      var quantity = $("#quantity").val();
      sendAjaxRequest(
          "{% url 'buy_order_market' %}",
          { 'symbol': symbol, 'qty': quantity },
          function(response) {
              console.log(response);
              alert('Your buy order is placed');
          },
          function(xhr, status, error) {
              console.error(xhr.responseText);
          }
      );
  });

  $("#sell").click(function() {
      var symbol = $("#symbol").val();
      var quantity = $("#quantity").val();
      sendAjaxRequest(
          "{% url 'sell_order_market' %}",
          { 'symbol': symbol, 'qty': quantity },
          function(response) {
              console.log(response);
              alert('Your sell order is placed');
          },
          function(xhr, status, error) {
              console.error(xhr.responseText);
          }
      );
  });
});
