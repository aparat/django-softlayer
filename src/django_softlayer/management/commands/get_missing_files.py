### -*- coding: utf-8 -*- ####################################################
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app, get_model, FieldDoesNotExist
from django.conf import settings

class Command(BaseCommand):
    '''Calculates similar albums for each album in database'''
    args = ''
    help = 'Returns missing or empty track files from the SoftLayer'
    option_list = BaseCommand.option_list + (
        make_option('--app',
                    dest='app',
                    help='Django application to get models from. Example: myApp'),
        make_option('--models',
                    dest='models',
                    help='Model names list. Example: User,Album,Track'),
        make_option('--fields',
                    dest='fields',
                    help='File fields list. Example: file,image,audio_track'),
    )


    def handle(self, app, models, fields, *args, **options):
        self.index = 1
        if hasattr(settings, 'CMD_MISSING_FILES_SETTINGS'):
            cmd_settings=settings.CMD_MISSING_FILES_SETTINGS
            app = cmd_settings.get('app', False)
            models = cmd_settings.get('models', False)
            fields = cmd_settings.get('fields', False)

        if not app:
            raise CommandError('You must specify --app option')
        if not models:
            raise CommandError('You must specify --models option')
        if not fields:
            raise CommandError('You must specify --fields option')

        def printTrack(obj, reason):
            print "%s. Instance: %s\n\tID: %s\n\tReason: %s" % \
                  (self.index, unicode(obj), obj.pk, reason)
            self.index += 1

        def get_missing_files(model, field_name):
            print '----------------Searching missing or incomplete %ss in %s:--------------\n' % \
                  (field_name, model.__name__)
            for obj in model.objects.all():
                try:
                    if getattr(obj, field_name).file.size == 0:
                        printTrack(obj, 'Size is 0')
                except:
                    printTrack(obj, 'FILE NOT FOUND')
            print '----------------------------------Done--------------------------------------'

        model_names = models.split(',')
        field_names = fields.split(',')

        for model_name in model_names:
            model = get_model(app, model_name)
            for field_name in field_names:
                try:
                    model._meta.get_field(field_name)
                except FieldDoesNotExist:
                    continue
                get_missing_files(model, field_name)




