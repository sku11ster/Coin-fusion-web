//BTC PRICE

fetch("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
  .then(response => response.json())
  .then(data => {
    const btcPrice = parseFloat(data.price);
    const btcPriceSpan = document.getElementById("btc-price");
    btcPriceSpan.textContent = `$${btcPrice.toFixed(2)}`;
  })
  .catch(error => {
    console.error("Failed to fetch BTC price:", error);
  });

//BTC PRICE CHANGE


fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
  .then(response => response.json())
  .then(data => {

    const btcPriceChange = parseFloat(data.priceChangePercent);

    const btcPriceChangeSpan = document.getElementById("btc-growth-rate");
    btcPriceChangeSpan.textContent = `${btcPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch BTC price change:", error);
  });

//ETH PRICE
  

  fetch("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    .then(response => response.json())
    .then(data => {
     
      const ethPrice = parseFloat(data.price);
  

      const ethPriceSpan = document.getElementById("eth-price");
      ethPriceSpan.textContent = `$${ethPrice.toFixed(2)}`;
    })
    .catch(error => {
      console.error("Failed to fetch ETH price:", error);
    });
//ETH GROWTH RATE

fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT")
  .then(response => response.json())
  .then(data => {
    const ethPriceChange = parseFloat(data.priceChangePercent);

    const ethPriceChangeSpan = document.getElementById("eth-growth-rate");
    ethPriceChangeSpan.textContent = `${ethPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch ETH price change:", error);
  });
//LTC PRICE
fetch("https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT")
  .then(response => response.json())
  .then(data => {
    const ltcPrice = parseFloat(data.price);
    const ltcPriceSpan = document.getElementById("ltc-price");
    ltcPriceSpan.textContent = `$${ltcPrice.toFixed(2)}`;
  })
  .catch(error => {
    console.error("Failed to fetch LTC price:", error);
  });
//LTC PRICE CHANGE



// Fetch the 24-hour ticker statistics for the LTC/USDT trading pair from the Binance API
fetch("https://api.binance.com/api/v3/ticker/24hr?symbol=LTCUSDT")
  .then(response => response.json())
  .then(data => {
    const ltcPriceChange = parseFloat(data.priceChangePercent);
    const ltcPriceChangeSpan = document.getElementById("ltc-growth-rate");
    ltcPriceChangeSpan.textContent = `${ltcPriceChange.toFixed(2)}%`;
  })
  .catch(error => {
    console.error("Failed to fetch LTC price change:", error);
  });

  //Function for Button to hold value of usdt amount
  function displayValueBuy() {
    var input = document.getElementById("usdt-amount").value;
    var button = document.getElementById("display-button");
    button.innerHTML = "Purchase $" + input;
  }



  const targetDiv = document.getElementById("third");
  const btn = document.getElementById("toggle");
  btn.onclick = function () {
    if (targetDiv.style.display !== "none") {
      targetDiv.style.display = "none";
    } else {
      targetDiv.style.display = "block";
    }
  };