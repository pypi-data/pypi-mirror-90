from typing import List, Union

class Step(object):
    """Step to run in a Pipeline.

    A Step is a function and a set of arguments that
    are called during Pipeline.run().
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self.func(*self.args, **self.kwargs)


class Transform(Step):
    """Transform to run in a data pipeline.

    A Transform is a subclass of Step. When run, its function
    is passed Pipeline.data as the first positional argument.
    """
    def run(self, data:DataFrame):
        return self.func(data, *self.args, **self.kwargs)


class Extract(Transform):
    """Extraction to run in a data pipeline.

    Extract is a subclass of Transform. It requires a source keyword
    argument (indicates where the data will be sourced from).
    """
    def __init__(self, *args, **kwargs):
        if kwargs.get('source') is None:
            raise Exception("No source provided for Extract.")
        super(Load, self).__init__(*args, **kwargs)


class Load(Transform):
    """Load to run in a data pipeline.

    A Load is a subclass of Transform. It requires a
    destination keyword argument (indicates where the data will be
    saved or passed to).
    """
    def __init__(self, *args, **kwargs):
        if kwargs.get('destination') is None:
            raise Exception("No destination provided for Load.")
        super(Load, self).__init__(*args, **kwargs)


class Pipeline(object):
    """Class to create and run an ETL pipeline.

    ATTRIBUTES
    - data: (Optional) The data object for the Pipeline.
    - extract: (Optional) Extract step to run if a data object is not provided.
    - steps: List of Steps and Transforms to run.
    - load: (Optional) The final Step in a pipeline. Should save or
            pass Pipeline.data somewhere.
    """

    def __init__(self,
                 data=None,
                 extract:Extract=None,
                 steps:List[Union[Step, Transform, Load]],
                 load:Load=None):
        self.data = data
        self.extract = extract
        self.steps = steps
        self.load = load

    def _extract(self)->DataFrame:
        """Run Step for extraction.

        Step is passed Pipeline.source as its first positional arg.
        """
        new_args = [arg for args in self.extract.args]
        new_args.insert(0, self.source)
        self.extract.args = new_args
        return self.extract.run()

    def run(self):
        # set data
        if self.data is None:
            # run extract if no data source provided.
            # NOTE: wait til run() to call _extract() in case
            #       source depends on other Pipelines.
            self.data = self._extract()

        # run steps
        for step in self.steps:
            if isinstance(step, Load):
                step.run(self.data)
            elif isinstance(step, Transform):
                # update data
                self.data = step.run(self.data)
            else:
                step.run()

        # load data
        if self.load is None:
            # return data if no load step provided
            return self.data
        else:
            self.load.run(self.data)
