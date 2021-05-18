import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views import View

from .models import *

# API endpoints of FIELD BUZZ
# access authentication API
FIELD_BUZZ_AUTHENTICATION_API = f'{settings.FIELD_BUZZ_API}api/login/'
# basic user/candidate information upload API
FIELD_BUZZ_APPLICATION_INFORMATION_SUBMISSION_API = f'{settings.FIELD_BUZZ_API}api/v1/recruiting-entities/'
# CV file upload API
FIELD_BUZZ_CV_FILE_UPLOAD_API = f'{settings.FIELD_BUZZ_API}api/file-object/'


class PersonalInformationView(View):
    template_name = 'info_uploader/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data, success, response = dict(), True, None

        # set posted data into dict
        for post_data in request.POST:
            data[post_data] = request.POST.get(post_data)

        # remove unnecessary keys
        for key in ['csrfmiddlewaretoken', 'submit']:
            data.pop(key, None)

        # if no field buzz reference then remove it from dict
        if data.get('field_buzz_reference') == "":
            data.pop('field_buzz_reference', None)

        # check file type, size
        file = request.FILES.get('cv_file')
        if 4 < (file.size / 1000000):
            # file size can't be more than 4 MB
            context = {
                'success': False,
                'response': "File size can't be more than 4 MB."
            }
            return render(request, self.template_name, context)

        if file.content_type != 'application/pdf':
            # only pdf files are allowed
            context = {
                'success': False,
                'response': "Only pdf files are allowed."
            }
            return render(request, self.template_name, context)

        # store file into media directory
        path = default_storage.save(f'{file.name}', ContentFile(file.read()))
        # set file_path
        data.update({'cv_file_path': f'/media/{path}'})

        # set cv_file.tsync_id in dict
        cv_file = {'tsync_id': f'{random_unique_string()}'}
        data.update({'cv_file': json.dumps(cv_file)})

        # set data into PersonalInformation class
        instance = PersonalInformation(**data)
        try:
            # validate PersonalInformation's data
            instance.full_clean()
        except Exception as ex:
            context = {
                'success': False,
                'response': ex.__str__()
            }
        else:
            # save all information into personal_information table
            instance.save()
            response = self.send_request_to_field_buzz_end_point(data, instance)

            context = {
                'success': response['success'],
                'response': response['response']
            }
        return render(request, self.template_name, context)

    def send_request_to_field_buzz_end_point(self, requested_data, personal_information):
        success, response = True, ''

        # set header information
        auth_token = AuthToken.objects.filter(is_valid=True).last().token
        headers = {"Authorization": f"Token {auth_token}", "content-type": "application/json"}

        # send 1st request (Personal Information)
        # make the json proper
        requested_data['cv_file'] = json.loads(requested_data['cv_file'])
        data = json.dumps(requested_data)

        # send request with personal information to field buzz api endpoint
        response = requests.post(FIELD_BUZZ_APPLICATION_INFORMATION_SUBMISSION_API, data, headers=headers).json()

        # store cv_file id in database
        if response['success']:
            cv_file = {'id': f'{response["cv_file"]["id"]}', 'tsync_id': f'{response["cv_file"]["tsync_id"]}'}
            personal_information.cv_file = json.dumps(cv_file)
            personal_information.save()

            # send/upload cv file
            files = {"file": ('CV_MD.ASHIKUN_NABI.pdf',
                              open(f'{settings.BASE_DIR}{personal_information.cv_file_path}', 'rb'),
                              'application/octet-stream')
                     }

            # send cv file
            headers.pop("content-type", None)
            resp = requests.put(f'{FIELD_BUZZ_CV_FILE_UPLOAD_API}{response["cv_file"]["id"]}/', files=files,
                                headers=headers).json()

            if not resp['success']:
                success = False
                response = resp
                if resp['status_code'] == 473:
                    # reauthenticate user
                    self.reauthenticate()
                    response = response['message'] + ' Please try again.'
                else:
                    response = response['message']
        else:
            success = False
            if response['status_code'] == 473:
                # reauthenticate user
                self.reauthenticate()
                response = response['message'] + ' Please try again.'
            else:
                response = response['message']
        return {'success': success, 'response': response}

    def authenticate(self):
        """Authenticate/login to field buzz api"""
        response = requests.post(FIELD_BUZZ_AUTHENTICATION_API, data=settings.FIELD_BUZZ_API_CREDENTIALS).json()
        if response['success']:
            """save access token into AuthToken"""
            AuthToken.objects.create(
                token=response['token']
            )
        return response

    def make_is_valid_false_auth_token_object(self):
        # make all valid tokens invalid
        AuthToken.objects.filter(is_valid=True).update(is_valid=False)

    def reauthenticate(self):
        # invalid all valid AuthToken
        self.make_is_valid_false_auth_token_object()
        # reauthenticate user
        self.authenticate()
