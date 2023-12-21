def params_to_ints(queryset) -> list[int]:
    """Change string with ids to list[int] with ids"""
    return [int(str_id) for str_id in queryset.split(",")]
