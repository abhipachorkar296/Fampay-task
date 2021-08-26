from django.apps import AppConfig


class TaskConfig(AppConfig):
    name = 'task'

    def ready(self):
        print("start....")
        from task import videos_caller
        videos_caller.begin()