from dramatiq.brokers.stub import StubBroker


class EagerBroker(StubBroker):
    """Used by tests to simulate CELERY_ALWAYS_EAGER behavior.
    https://github.com/Bogdanp/dramatiq/issues/195
    Modified by @dnmellen to support pipelines and groups
    """
    def process_message(self, message):
        try:
            actor = self.get_actor(message.actor_name)

            # Adds pipeline support
            if 'pipe_target' in message.options:
                result = actor(*message.args, **message.kwargs)
                actor = self.get_actor(message.options['pipe_target']['actor_name'])
                if message.options['pipe_target']['options'].get('pipe_ignore', False):
                    extra_args = tuple()
                else:
                    extra_args = (result,)
                actor.send_with_options(
                    args=message.options['pipe_target']['args'] + extra_args,
                    kwargs=message.options['pipe_target']['kwargs'],
                    **message.options['pipe_target']['options']
                )
            else:
                actor(*message.args, **message.kwargs)
        except Exception as exc:
            message.failed = True
            message._exception = exc
        else:
            message.failed = False

        # Ensure middlewares are executed (I need GroupCallbacks middleware)
        self.emit_after('process_message', message)

    def enqueue(self, message, *, delay=None):
        self.process_message(message)