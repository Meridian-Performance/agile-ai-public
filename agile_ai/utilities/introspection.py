
class Introspection:
    @staticmethod
    def get_annotations(cls):
        return cls.__annotations__

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


