from time import time
from logging import getLogger

from pycloudia.defer import inline_callbacks, maybe_deferred, DeferredList, DeferredListFactory
from pycloudia.decorators import generate_dict


class ServicesRegistry(object):
    logger = getLogger('pycloudia.services')

    def __init__(self, service_factory):
        self.service_factory = service_factory

    def configure(self, bean_list):
        self.services_map = self._create_services_map(bean_list)

    @generate_dict
    def _create_services_map(self, bean_list):
        for bean in bean_list:
            yield bean.name, self.service_factory(bean)

    def run(self):
        deferred_list = []
        for service in self.services_map.values():
            deferred_list.append(self._create_deferred_service_run(service))
        return DeferredListFactory.create(deferred_list)

    @inline_callbacks
    def _create_deferred_service_run(self, service):
        start = time()
        try:
            yield maybe_deferred(service.run)
        except RuntimeError as e:
            self._log_service_failure(service, e)
        else:
            self._log_service_success(service, time() - start)

    def _log_service_failure(self, service, exception):
        self.logger.error(
            'Channel %s has not been started on %s:%s: %s',
            service.name,
            service.host,
            service.port,
            exception
        )

    def _log_service_success(self, service, start_duration):
        self.logger.info(
            'Channel %s started on %s:%s in %.3f seconds',
            service.name,
            service.host,
            service.port,
            start_duration
        )
