from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.utils.html import format_html
from .models import Translation,Language

import openai,json
import portfolio.settings as settings
from django.views.decorators.csrf import csrf_exempt
from traceback import print_exc

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('text', 'lang', 'result', 'translate_action_button')
    list_filter = ('lang',)  # Add filters
    search_fields = ('text', 'result')

    def translate_action_button(self, obj):
        # Create the translation button
        translate_button = format_html(
            '<a href="#" class="btn btn-sm btn-outline-primary custom-translate-btn d-inline-flex align-items-center" data-id="{}">'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" width="20" height="20" fill="currentColor" stroke="none" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="me-1">'
            '<path d="M234.7 42.7L197 56.8c-3 1.1-5 4-5 7.2s2 6.1 5 7.2l37.7 14.1L248.8 123c1.1 3 4 5 7.2 5s6.1-2 7.2-5l14.1-37.7L315 71.2c3-1.1 5-4 5-7.2s-2-6.1-5-7.2L277.3 42.7 263.2 5c-1.1-3-4-5-7.2-5s-6.1 2-7.2 5L234.7 42.7zM46.1 395.4c-18.7 18.7-18.7 49.1 0 67.9l34.6 34.6c18.7 18.7 49.1 18.7 67.9 0L529.9 116.5c18.7-18.7 18.7-49.1 0-67.9L495.3 14.1c-18.7-18.7-49.1-18.7-67.9 0L46.1 395.4zM484.6 82.6l-105 105-23.3-23.3 105-105 23.3 23.3zM7.5 117.2C3 118.9 0 123.2 0 128s3 9.1 7.5 10.8L64 160l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L128 160l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L128 96 106.8 39.5C105.1 35 100.8 32 96 32s-9.1 3-10.8 7.5L64 96 7.5 117.2zm352 256c-4.5 1.7-7.5 6-7.5 10.8s3 9.1 7.5 10.8L416 416l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L480 416l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L480 352l-21.2-56.5c-1.7-4.5-6-7.5-10.8-7.5s-9.1 3-10.8 7.5L416 352l-56.5 21.2z"/>'
            '</svg></a>',
            obj.id
        )

        # Add placeholders for the Confirm and Cancel buttons
        confirm_cancel_buttons = format_html(
            '<div id="confirm-cancel-buttons-{}" style="display:none;">'
            '<button id="confirm-btn-{}" '
            'style="background-color: #5cb85c; color: white; border: none; padding: 3px; '
            'border-radius: 3px; cursor: pointer; margin-right: 5px;">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" '
            'viewBox="0 0 16 16">'
            '<path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022Z"/>'
            '</svg>'
            '</button>'
            '<button id="cancel-btn-{}" '
            'style="background-color: #d9534f; color: white; border: none; padding: 3px; '
            'border-radius: 3px; cursor: pointer;">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" '
            'viewBox="0 0 16 16">'
            '<path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>'
            '</svg>'
            '</button>'
            '</div>',
            obj.id, obj.id, obj.id
        )

        # Return the translation button along with placeholders for Confirm and Cancel buttons
        return translate_button + confirm_cancel_buttons

    
    translate_action_button.short_description = 'reTranslate'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/translate-with-ai/', 
                self.admin_site.admin_view(self.translate_with_ai),
                name='translation_ai_translate'
            ),
            
            path(
                '<path:object_id>/update-translate/', 
                self.admin_site.admin_view(self.update_translation),
                name='update_translation'
            ),
        ]
        return custom_urls + urls
    
    @csrf_exempt
    def translate_with_ai(self, request, object_id):
        try:
            print('translate_with_ai')
            
            if request.method != 'POST':
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Invalid request'
                }, status=400)
            
            # Fetch the translation object
            translation = Translation.objects.get(pk=object_id)

            # Use OpenAI to translate
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            lang = translation.lang
            
            # If translation.lang is 'ber', adjust language code to 'ber-Tifinagh'
            if lang == 'ber':
                lang = 'ber-Tifinagh'
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional translator. This is for a web scraping project, and the translation is part of the portfolio of a web scraping and automation developer (PHP-Python-TS/JS). do not remove symbols"},
                    {"role": "user", "content": f"Translate the following text to {lang}: {translation.text}"}
                ]
            )

            # Extract the translated text
            translated_text = response.choices[0].message.content.strip()
            
            # Return translation result without updating the database yet
            return JsonResponse({
                'status': 'success', 
                'message': 'Translation completed',
                'translated_text': translated_text
            })
        
        except Translation.DoesNotExist:
            print_exc()
            return JsonResponse({
                'status': 'error', 
                'message': 'Translation not found'
            }, status=404)
        except Exception as e:
            print_exc()
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=500)

    @csrf_exempt
    def update_translation(self, request, object_id):
        try:
            if request.method != 'POST':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid request'
                }, status=400)

            # Fetch the translation object
            translation = Translation.objects.get(pk=object_id)

            # Get translated text from the request
            data = json.loads(request.body)
            translated_text = data.get('translation')
            print(translated_text)
            # Update the translation result in the database
            translation.result = translated_text
            translation.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Translation updated successfully'
            })

        # except Translation.DoesNotExist:
        #     print_exc()
        #     return JsonResponse({
        #         'status': 'error',
        #         'message': 'Translation not found'
            # }, status=404)
        except Exception as e:
            print(e)
            print_exc()
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)