import click


class Mutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.get('not_required_if')

        assert self.not_required_if, "'not_required_if' parameter required"
        del kwargs['not_required_if']
        kwargs['help'] = \
            f"{kwargs.get('help', '').strip()} Option is mutually exclusive with {', '.join(self.not_required_if)}."
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for m_opt in self.not_required_if:
            if m_opt in opts:
                if current_opt in opts:
                    raise click.UsageError(f"Illegal usage: '{self.name}' is mutually exclusive with {m_opt}.")
                else:
                    self.prompt = None
        
        return super(Mutex, self).handle_parse_result(ctx, opts, args)
