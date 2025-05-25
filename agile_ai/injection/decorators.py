from typing import Type, TypeVar

from agile_ai.injection import Marker  # noqa
from agile_ai.injection.autowire_context import AutowireContext
from agile_ai.injection.interfaces import Service
from agile_ai.utilities.introspection import Introspection


def autowire(cls):
    return autowire_context.autowire(cls)


def reset_autowire():
    autowire_context.reset()


def autowire_services(cls):
    marker_groups = Introspection.get_marker_groups(cls)
    service_group = marker_groups.get("__services__", {})
    for service_name, service_cls in service_group.items():
        from agile_ai.injection.interfaces import Service
        if Introspection.is_subclass(service_cls, Service):
            setattr(cls, service_name, autowire(service_cls))
    return cls


autowire_context = AutowireContext()

ServiceT = TypeVar("ServiceT", bound=Service)


def get_service(service_cls: Type[ServiceT]) -> ServiceT:
    return autowire_context.get_service(service_cls)


def inject(instance, for_cls=None):
    autowire_context.inject(instance, for_cls)
    return instance