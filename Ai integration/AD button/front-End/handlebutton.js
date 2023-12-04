// Send request to server to generate ad
document.getElementById('generateAdButton').addEventListener('click', function() {


    fetch('/generate_ad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            productName: 'Product Name',
            productDetails: 'Product Details',
            productPrice: 'Product Price'
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('generatedAd').innerHTML = data.generatedAd;
    });
});