# Dishify
Application for parsing text from recipe image to be imported into MyDish user's recipe.

## Table of Contents
- Installation
- Usage
- Contributing
- Credits
- License

## Installation
Pull repository into local directory. Create a new environment using desired handler. Required libraries will be installed through the requirements.txt file.

## Usage
- End user must upload an image to MyDish APP.
- MyDish APP sends a request to Dishify API Gateway with the image's URI.
- API Gateway handles the request and calls the Dishify function.
- Dishify function makes a call to Google Vision's OCR API with the image's URI as a parameter.
- Dishify returns Vision API's parsed text in JSON dictionary format.
- Future release: Dishify returns text in "Ingredients" and "Instructions" format ready for MyDish use.

## Contributing
Fork repo and work locally. Upload changes to personal repository and create a pull request to this branch.

## Credits
Todd Gonzalez - Machine Learning Engineer, Data Engineer.

John Humenczuk - Machine Learning Engineer, Data Engineer.

## License
MIT
