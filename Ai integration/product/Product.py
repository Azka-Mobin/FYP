from flask import Flask, request, jsonify
import stripe
import os

app = Flask(__name__)

# Initialize Stripe with your API key
stripe.api_key = os.environ.get('STRIPE_API_KEY')

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

    # Save the generated ad to a file
    with open("generated_ad.txt", "w") as file:
        file.write(ad)

    return jsonify({'generatedAd': ad})

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Get the total amount to charge from the client request
    total_amount = request.json['totalAmount']

    try:
        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount),
            currency='usd'
        )
        return jsonify(clientSecret=intent.client_secret), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/payment_confirmation', methods=['POST'])
def payment_confirmation():
    # Handle payment confirmation logic here
    # This is where you would update your database or trigger other actions upon successful payment
    return jsonify(message="Payment successful"), 200

@app.route('/share_on_social_media', methods=['POST'])
def share_on_social_media():
    # Get the ad content to share from the client request
    ad_content = request.json['adContent']

    # Placeholder for social media sharing logic
    # Implement sharing on social media platforms like Facebook, Twitter, etc.
    return jsonify(message="Shared on social media"), 200

def generate_ad_title(product_name, product_details):
    # Placeholder for generating ad title
    return f"New Ad: {product_name} - {product_details}"

def generate_ad_body(product_name, product_details, ad_title, product_price):
    # Placeholder for generating ad body
    return f"{ad_title}\nPrice: ${product_price}\nDescription: {product_details}"

# Placeholder for product link
product_link = "https://example.com/product"

if __name__ == '__main__':
    app.run(debug=True)