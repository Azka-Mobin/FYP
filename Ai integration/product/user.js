//Send request to server

fetch('/register_lead', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        productId: productId
    })
});