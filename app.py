from flask import Flask, request,send_file,jsonify # type:ignore 
from flask_cors import CORS # type:ignore
from PIL import Image # type:ignore
import io
import numpy as np # type:ignore
import cv2 # type:ignore

from color_palette import preprocess_image, apply_mask, generate_multiple_palettes, U2NET_MODEL

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Paletto API is running',
        'version': '1.0.0'
    }), 200


### end point for generating color palette
######################################################################

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Access the raw image data from the request body
        image_data = request.data
        
        if not image_data:
            return jsonify({'error': 'No image data found in the request'}), 400

        # Convert the raw image data to a PIL Image
        image = Image.open(io.BytesIO(image_data))
        print(f"Original image size: {image.size}") 

        # Process the image as before
        image_size = 256
        input_array = preprocess_image(image, image_size)
        y_pred = U2NET_MODEL.predict(input_array)
        print(f"Prediction shape: {y_pred.shape}")
        predicted_mask = y_pred[0]
        predicted_mask = cv2.resize(predicted_mask, (image_size, image_size))
        original_image = np.array(image.resize((image_size, image_size)))


        focal_object = apply_mask(original_image, predicted_mask)
        all_palettes = generate_multiple_palettes(focal_object, num_palettes=5, n_colors=3, n_new_colors=3)
        print(f"Generated palettes: {all_palettes}")  # Log generated palettes
        return jsonify({
            'color_palettes': all_palettes,  # Return multiple palettes
        }), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print the error message to the console
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)