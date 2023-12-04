import os

os.environ["REPLICATE_API_TOKEN"]= 'ENTER YOUR API KEY HERE'

import replicate





def get_ad_title(product_name, product_description):
    
    # Prompts
    pre_prompt_1 = "Generate a compelling ad title for the following product: Product Name:"
    pre_prompt_2 = "Product Description:"
    
    # Generate LLM response
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{pre_prompt_1} {product_name} {pre_prompt_2} {product_description}.Make the ad title short and concise. Do not return a complete sentence instead just return the ad title. Ad Title: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    
    full_response = ""

    for item in output:
        full_response += item
        
    return full_response

def get_ad_body(product_name, product_description, product_price):
    
    # Prompts
    pre_prompt_0 = "Donot use emojis and unicode characters. "
    pre_prompt_1 = "Generate a compelling ad for the following product: "
    pre_prompt_2 = "Product Name:"
    pre_prompt_3 = "Product Description:"
    pre_prompt_4 = "Product Price:"
    
    # Generate LLM response
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{pre_prompt_0}{pre_prompt_1} {pre_prompt_2} {product_name} {pre_prompt_3} {product_description} {pre_prompt_4} PKR {product_price} Ad: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":1024, "repetition_penalty":1})
    
    full_response = ""

    for item in output:
        full_response += item
        
    return full_response
