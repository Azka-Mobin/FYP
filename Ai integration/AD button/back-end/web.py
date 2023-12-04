from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_ad', methods=['POST'])
def generate_ad():
    data = request.json
    product_name = data['productName']
    product_details = data['productDetails']
    product_price = data['productPrice']
    
    # Call your generative AI model
    
    # Model Part 1: Generate ad title
    ad_title = generate_ad_title(product_name, product_details)

    # Model Part 2: Generate ad body
    ad_body = generate_ad_body(product_name, product_details, ad_title, product_price)

    ad = f"{ad_body}\n\nLink to the product: {product_link}"

    return jsonify({'generatedAd': ad})

if __name__ == '__main__':
    app.run(debug=True)