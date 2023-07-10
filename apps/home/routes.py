# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests


@blueprint.route('/index')
@login_required
def index():
    print("template")
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        #etting form data
        if request.method == 'POST':
            # Process form data here 
            page_id = request.form.get('page_id')
            access_token = request.form.get('access_token')
            message = request.form.get('message')
            post_text_on_page(page_id, access_token, message)

           # if request.form.get('button') == 'form2_button':
            #    page_id = request.form.get('page_id')
             #   access_token = request.form.get('access_token')
              #  file = request.form.get('file')
               # publish_image_on_page(page_id, access_token, file, "test_caption")

            # Return a response with JavaScript code to show the pop-up alert
            return '''
                <script>
                    alert("Form submitted successfully!");
                    window.location.href = "/";
                </script>
                '''

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
    
# Function to post text on facebook page
def post_text_on_page(page_id, access_token, message):
    url = f"https://graph.facebook.com/v12.0/{page_id}/feed"
    params = {
        'access_token': access_token,
        'message': message
    }
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print('POST request failed with status code:', response.status_code)

    except requests.exceptions.RequestException as e:
                print('An error occurred during the POST request:', str(e))

# post images
def publish_image_on_page(page_id, access_token, image_url, caption):
    url = f"https://graph.facebook.com/v12.0/{page_id}/photos"
    params = {
        'access_token': access_token,
        'url': image_url,
        'caption': caption
    }
    response = requests.post(url, params=params)
    return response.json()

@blueprint.route('icons', methods=['GET', 'POST'])
#@app.route('/landing', methods=["POST", "GET"])
@login_required
def form_publication():
    if request.method == 'POST':
        # Retrieve form data
        page_id = request.form.get('page_id')
        message = request.form.get('message')
        # Perform additional actions with the data
        #return f'Page ID: {page_id}, Message: {message}'
        return render_template('home/icons.html')
    return render_template('home/icons.html', segment='icons')