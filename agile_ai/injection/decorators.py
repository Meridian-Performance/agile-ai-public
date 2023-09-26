from agile_ai.injection import Marker  # noqa
from agile_ai.injection.autowire_context import AutowireContext
from agile_ai.utilities.introspection import Introspection


def autowire(cls):
    return autowire_context.autowire(cls)


def reset_autowire():
    autowire_context.reset()


def autowire_services(cls):
    marker_groups = Introspection.get_marker_groups(cls)
    service_group = marker_groups.get("__services__", {})
    for service_name, service_cls in service_group.items():
        setattr(cls, service_name, autowire(service_cls))


autowire_context = AutowireContext()
