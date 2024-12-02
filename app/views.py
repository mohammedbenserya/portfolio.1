# myapp/views.py

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .services.google_lens import upload_to_google_lens, parse_af_callback_data, get_match
from app.services.zillow import zillow_scraper
import re,pandas as pd
from django.shortcuts import redirect

@csrf_exempt
def extract_text(request): 
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        regex = request.POST.get('regex')
        
        try:
            soup = upload_to_google_lens(image_file)
            if not soup:
                return JsonResponse({"error": "Failed to upload image to Google Lens."}, status=500)
            script_tag = soup.find('script', class_='ds:1')
            if not script_tag:
                return JsonResponse({"error": "Failed to find the required script tag in the response."}, status=500)
            parsed_data = parse_af_callback_data(script_tag.string)
            text_data = get_match(parsed_data)   
            if not regex:
                return JsonResponse({"extracted_text": text_data})
            match = re.search(regex, text_data)
            if match:
                return JsonResponse({"extracted_text": match.group(1)})
            return JsonResponse({"extracted_text": text_data})
        except re.error as regex_error:
            return JsonResponse({"extracted_text": text_data, "error": f"Invalid regex pattern: {str(regex_error)}"}, status=400)
        except Exception as e:
            return JsonResponse({"extracted_text": text_data, "error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return HttpResponse("Only POST method is allowed.", status=405)
    
from django.shortcuts import render
def lens_view(request):
    return render(request, 'lens.html')

def zillow_view(request):
    return render(request, 'zillow.html')

def portfolio_view(request):
    return render(request, 'portfolio.html')
def aboutme_view(request):
    return render(request, 'aboutme.html')

@csrf_exempt
def get_zillow_data(request): 
    if request.method == 'POST':
        query = request.POST.get('query')
        get_all_pages = request.POST.get('get_all_pages', False)
        try:
            data = zillow_scraper(query, get_all_pages)
            df = pd.json_normalize(data['cat1']['searchResults']['listResults'])
            df.drop_duplicates(subset=['id'], inplace=True)

            # Replace NaN values with None
            df = df.where(pd.notnull(df), None)

            #replace nan with -
            df.fillna('-', inplace=True)



            return JsonResponse(df.to_dict(orient='records'), safe=False)
        except Exception as e:
            raise HttpResponse(str(e),status=500)
    else:
        return HttpResponse("Only POST method is allowed.", status=405)
    
    
    
# views.py
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            project_type = form.cleaned_data['project_type']
            message = form.cleaned_data['message']
            
            email_message = f"""
            New Contact Form Submission:
            Name: {name}
            Email: {email}
            Project Type: {project_type}
            Message: {message}
            """
            
            try:
                send_mail(
                    subject=f'New Contact Form Submission from {name}',
                    message=email_message,
                    from_email=email,
                    recipient_list=['benseryamohammed1@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully!')
                 
            except Exception as e:
                messages.error(request, f'An error occurred while sending the message: {str(e)}')
        else:
            messages.error(request, 'An error occurred while sending the message.')
    return redirect('portfolio')