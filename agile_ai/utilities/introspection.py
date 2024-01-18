

class Introspection:
    @staticmethod
    def get_annotations(cls):
        if not hasattr(cls, "__annotations__"):
            return dict()
        return cls.__annotations__

    @staticmethod
    def get_annotation_items(cls):
        return Introspection.get_annotations(cls).items()

    @staticmethod
    def get_marker_groups(cls):
        annotations = Introspection.get_annotations(cls)
        current_group = dict()
        marker_groups = dict()
        for annotation_name, annotation_type in annotations.items():
            if "Marker" in str(annotation_type):
                current_group = dict()
                marker_groups[annotation_name] = current_group
            else:
                current_group[annotation_name] = annotation_type
        return marker_groups

    @classmethod
    def get_class_name(cls, object_cls):
        return object_cls.__name__

    @classmethod
    def is_subclass(cls, subclass_cls, parent_cls):
        try:
            return issubclass(subclass_cls, parent_cls)
        except:
            return False

    @staticmethod
    def is_object_option(object_instance) -> bool:
        from agile_ai.memoization.object_option import ObjectOption
        return isinstance(object_instance, ObjectOption)

    @staticmethod
    def is_object_option_cls(cls) -> bool:
        cls_str = str(cls)
        return "ObjectOption" in cls_str or "StreamOption" in cls_str

    @staticmethod
    def get_object_option_cls(cls_type):
        cls_str = str(cls_type)
        from agile_ai.memoization.object_option import ObjectOption
        from agile_ai.processing.stream_object import StreamOption
        if "StreamOption" in cls_str:
            return StreamOption
        if "ObjectOption" in cls_str:
            return ObjectOption



