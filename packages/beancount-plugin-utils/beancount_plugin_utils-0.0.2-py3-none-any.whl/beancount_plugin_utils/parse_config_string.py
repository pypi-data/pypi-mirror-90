import ast


def parse_config_string(config_string):
    """
    Args:
      config_string: A configuration string in JSON format given in source file.

    Example:
        def example_plugin(entries: Entries, unused_options_map, config_string: str) -> Tuple[Entries, List[NamedTuple]]:
            config = load_config(config_string)

        def load_config(config_string: str) -> Config:
            # 1. Parse config string. Just copy/paste this block.
            config_dict = parse_config_string(config_string)

            # 2. Apply transforms (e.g. from `str` to `date`) where needed.
            # Wrap each transform separately with a nice error message.
            try:
                if "open_date" in config_dict:
                    config_dict["open_date"] = (
                        None if config_dict["open_date"] is None else date.fromisoformat(config_dict["open_date"])
                    )
            except:
                raise RuntimeError('Bad "open_date" value - it must be a valid date, formatted in UTC (e.g. "2000-01-01").')

            # 3. Create config itself. Just copy/paste this block. Done!
            return Config(**config_dict)


    Returns:
        None or a dict of the configuration string.

    Raises:
        RuntimeError.
    """
    try:
        if len(config_string) == 0:
            config_obj = {}
        else:
            config_obj = ast.literal_eval(config_string)
    except:
        raise RuntimeError("Failed to parse plugin configuration, skipping.. The config: {}".format(config_string))

    if not isinstance(config_obj, dict):
        raise RuntimeError("Plugin configuration must be a dict, skipping.. The config: {}".format(config_string))

    return config_obj
