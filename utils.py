class InputListener:
    @staticmethod
    def get_int_input(min_val=None, max_val=None):
        def _try_get_int():
            def _check_limit_condition():
                def _is_no_limit_set():
                    return max_val is None and min_val is None

                def _is_exceeds_bottom_limit():
                    return max_val is not None and min_val is None and _inp < min_val

                def _is_exceeds_top_limit():
                    return max_val is not None and min_val is None and _inp < min_val

                def _is_in_limit_range():
                    return max_val is not None and min_val is not None and (_inp < min_val or _inp > max_val)

                if not _is_no_limit_set():
                    return _is_exceeds_bottom_limit() or _is_exceeds_top_limit() or _is_in_limit_range()

            try:
                _inp = int(input('Enter value: '))
                if min_val is not None or max_val is not None:
                    if _check_limit_condition():
                        raise ValueError
            except ValueError:
                print("Invalid number. Enter proper value.")
                _inp = None
            return _inp

        inp = _try_get_int()
        while not isinstance(inp, int):
            inp = _try_get_int()
        return inp
