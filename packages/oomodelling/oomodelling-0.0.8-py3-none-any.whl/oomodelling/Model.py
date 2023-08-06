import logging
from functools import reduce

import numpy as np


class Model:
    TIME = 'time'

    # TODO: Add check to make sure there's no unintentional override of variables while in the constructor.

    def __init__(self):
        super().__init__()

        # Bypasses the __set_attr_ as that method uses logging as well.
        logger_name = f"{__name__}.{type(self).__name__}"
        super().__setattr__("_l", logging.getLogger(logger_name))
        self._l.debug(f"Starting logger {logger_name}.")

        self._bypass_set_attr = True
        self._states = []
        self._num_states = 0
        self._inputs = []
        self._parameters = []
        self._vars = []
        self._models = []
        self._initial_values = {}
        self._current_state_values = {}
        self._state_derivatives = {}
        self.signals = {}
        self._under_construction = True
        self._bypass_set_attr = False

        self.time = self.state(0.0)
        self.der(self.TIME, lambda: 1.0)

    def _new_signal(self, name):
        assert name not in self.signals.keys(), "Signal already defined."
        self.signals[name] = []

    def state(self, init):
        assert self._under_construction, "Not under construction."
        return lambda name: self._new_state(name, init)

    def _new_state(self, name, init):
        assert self._under_construction, "Not under construction."
        assert name.isidentifier(), "Name must be valid identifier."
        assert not callable(init), "Init formula must not be callable."
        assert not hasattr(self, name), "Name must not be already defined."

        self._states.append(name)
        self._initial_values[name] = init
        self._current_state_values[name] = init

        self._new_signal(name)

        return self._get_state_function(name)

    def _set_input(self, name, value):
        assert name in self._inputs, "Name must be an input."
        self._bypass_set_attr = True
        setattr(self, name, value)
        self._bypass_set_attr = False

    def der(self, state, fun):
        assert self._under_construction, "Not under construction."
        assert callable(fun), "Fun must be callable."
        assert hasattr(self, state), "State must be an attribute of the object."
        der_name = self._der(state)
        self._new_signal(der_name)
        self._state_derivatives[state] = self._get_signal_function(der_name, fun)

    def _new_input(self, name, def_formula):
        assert self._under_construction, "Not under construction."
        assert name.isidentifier(), "Name must be valid identifier."
        assert not hasattr(self, name), "Name must not be already defined."
        self._inputs.append(name)
        self._new_signal(name)
        return self._get_signal_function(name, def_formula)

    def input(self, def_formula):
        assert self._under_construction, "Not under construction."
        assert callable(def_formula), "def_formula must be callable."
        return lambda name: self._new_input(name, def_formula)

    def _new_var(self, name, fun):
        assert self._under_construction, "Not under construction."
        assert callable(fun), "Fun must be callable."
        assert name.isidentifier(), "Name must be valid identifier."
        assert not hasattr(self, name), "Name must not be already defined."
        self._vars.append(name)
        self._new_signal(name)
        return self._get_signal_function(name, fun)

    def var(self, fun):
        assert self._under_construction, "Not under construction."
        return lambda name: self._new_var(name, fun)

    def _new_parameter(self, name, val):
        assert name.isidentifier(), "Name must be valid identifier."
        assert not callable(val), "val must be callable."
        assert not hasattr(self, name), f"Name {name} is already defined with value {getattr(self, name)}."
        self._parameters.append(name)
        return val

    def parameter(self, val):
        assert self._under_construction, "Not under construction."
        return lambda name: self._new_parameter(name, val)

    def model(self, name, obj):
        assert self._under_construction, "Not under construction."
        assert not callable(obj), "obj must not be callable."
        assert name.isidentifier(), "Name must be valid identifier."
        assert not hasattr(self, name), "Name must not be already defined."
        self._models.append(name)
        return obj

    def save(self):
        assert self._under_construction, "Not under construction."
        self._bypass_set_attr = True
        self._under_construction = False
        self._num_states = self.nstates()
        self._bypass_set_attr = False

    def set_time(self, t):
        """
        Sets the internal time, and all submodels's time, to t.
        :param t:
        :return:
        """
        self.time = t
        for m in self._models:
            getattr(self, m).set_time(t)

    """
    Sets every state to its initial value (provided at the constructor) and clears every signal to its initial value (or empty).
    If you want different initial values, then set them after calling this function.
    """

    def reset(self):
        assert not self._under_construction, "Under construction."

        def reset_signal(s):
            signal = self.signals[s]
            signal.clear()
            if s in self._current_state_values.keys():
                self._current_state_values[s] = self._initial_values[s]

        self._proc_signals(reset_signal,
                           lambda m: getattr(self, m).reset())

    """
    Ensures that every signal has a single initial value, or is empty.
    """

    def assert_initialized(self):

        def _assert_initialized(s):
            assert s in self.signals.keys(), "Signal must exist."
            assert len(self.signals[s]) == 0, "Signal must be empty."

        self._proc_signals(_assert_initialized,
                           lambda m: getattr(self, m).assert_initialized())

    def nstates(self):
        assert not self._under_construction, "Under construction."
        nstates_models = sum([getattr(self, m).nstates() for m in self._models])
        return nstates_models + len(self._states)

    def nsignals(self):
        """
        :return: The number of signals.
        """
        assert not self._under_construction, "Under construction."
        totallist = [len(self._states) * 2,
                     len(self._inputs),
                     len(self._vars)
                     ] + [getattr(self, m).nsignals() for m in self._models]

        return sum(totallist)

    def signal_names(self, prefix=''):
        assert not self._under_construction, "Under construction."
        return self._fmap_signals(lambda s: prefix + s,
                                  lambda m: getattr(self, m).signal_names(prefix + m + '.'))

    def state_names(self, prefix=''):
        assert not self._under_construction, "Under construction."
        return self._fmap_states(lambda s: prefix + s,
                                 lambda m: getattr(self, m).state_names(prefix + m + '.'))

    def state_vector(self):
        """
        Creates a flat state from the internal state and models
        """
        assert not self._under_construction, "Under construction."
        return self._fmap_states(lambda s: getattr(self, s)(),
                                 lambda m: getattr(self, m).state_vector())

    def derivatives(self):
        assert not self._under_construction, "Under construction."

        def model(t, npstate):
            assert not self._under_construction, "Under construction."
            # Map state to internal state
            self._update(npstate, t)
            ders = self._compute_derivatives()
            return ders

        return model

    # noinspection PyProtectedMember
    def _update(self, state, t, i=0):
        """
        Takes a flat state, and propagates it to the internal models.
        """
        assert not self._under_construction, "Under construction."

        init_i = i

        for s in self._states:
            assert i < len(state), "State index must lie within state array."
            setattr(self, s, state[i])
            i += 1

        for m in self._models:
            model = getattr(self, m)
            i += model._update(state, t, i)

        num_read = i - init_i
        assert len(state) >= num_read, "Cannot read more than the object has."

        return num_read

    def record_state(self, state, t, override=False):
        """
        Stores a new snapshot in the state history.
        :returns True if the model has a new continuous state (e.g., due to handling events).
        """
        if len(self.signals[self.TIME]):
            last_commit_time = self.get_last_commit_time()
            if override:
                if len(self.signals[self.TIME]) >= 2:
                    second_to_last_commit_time = self.signals[self.TIME][-2]
                    assert t >= second_to_last_commit_time, "Trying to override the past."
            else:
                assert t >= last_commit_time, "Trying to place new sample with a prior timestamp."

        self._update(state, t)
        internal_time = self.time()
        assert np.isclose(internal_time, t), "Internal time was updated."
        self._step_commit(override)

    # noinspection PyProtectedMember
    def _step_commit(self, override):
        current_length = self.get_history_size()

        def _commit_signal(name, value):
            if override:
                self.signals[name][-1] = value
            else:
                self.signals[name].append(value)

        self.__proc_signals(lambda s: _commit_signal(s, self._current_state_values[s]),
                            lambda d: _commit_signal(self._der(d), self._state_derivatives[d]()),
                            lambda u: _commit_signal(u, getattr(self, u)()),
                            lambda v: _commit_signal(v, getattr(self, v)()),
                            lambda m: getattr(self, m)._step_commit(override))
        if override:
            assert self.get_history_size() == current_length, "Override did not add new sample."
        else:
            assert self.get_history_size() == current_length + 1, "New sample was added."

    def get_last_commit_time(self):
        assert len(self.signals[self.TIME]) > 0, "Not supposed to call this function prior to any sampling."
        return self.signals[self.TIME][-1]

    def get_history_size(self):
        size = len(self.signals[self.TIME])

        def assertsize_signal(signal):
            assert len(self.signals[self.TIME]) == size, "Signals size is consistent."

        def assertsize_model(model):
            assert getattr(self, model).get_history_size() == size, "Signals size is consistent."

        self._proc_signals(assertsize_signal, assertsize_model)

        return size

    def current_signals(self):
        assert not self._under_construction, "Not under construction."
        return self._fmap_signals(lambda s: getattr(self, s)(),
                                  lambda m: getattr(self, m).current_signals())

    def _get_state_function(self, name):
        assert self._under_construction, "Under construction."
        assert name in self._current_state_values.keys(), "Name has been defined."

        def signal(d=None):
            if d is None or len(self.signals[name]) == 0 or np.isclose(d, 0.0):
                return self._current_state_values[name]
            else:
                return self._delayed_signal_value(name, d)

        return signal

    def _get_signal_function(self, name, fun):
        def signal(d=None):
            if d is None or len(self.signals[name]) == 0 or np.isclose(d, 0.0):
                try:
                    value = fun()
                except TypeError:
                    self._l.error(f"TypeError in signal {name}")
                    raise
            else:
                value = self._delayed_signal_value(name, d)
            assert value is not None, "Value is not None."
            return value

        return signal

    def _delayed_signal_value(self, name, d):
        assert name in self.signals.keys(), "Name must be a signal."
        t = self.time()
        ts = max(0, t + d)  # if -d goes beyond, we set ts=0
        idx = self._earliest_time(ts)
        assert idx <= len(self.signals[name]) - 1, "idx lies within the array domain."
        value = self.signals[name][idx]
        return value

    """
    Searches for the index of timestamp that is closest (from the left) to the argument t.
    Examples:
        [0,1,2,3,4] , 1.2 -> 1
        [0,1,2,3,4] , 4.2 -> 4
    """

    def _earliest_time(self, t):
        ts = self.signals['time']
        return self._find_sup(t, ts)

    def _signals_from_state(self, npstate, t):
        self._update(npstate, t)
        return self.current_signals()

    # noinspection PyProtectedMember
    def _compute_derivatives(self):
        # Assumes that state has been updated.
        res = self._fmap_states(lambda s: self._state_derivatives[s](),
                                lambda m: getattr(self, m)._compute_derivatives())
        return res

    @staticmethod
    def _der(s):
        return 'der_' + s

    def get_state_idx(self, state_name):
        assert not self._under_construction, "Not under construction."
        return self._states.index(state_name)

    def _fmap_states(self, f_states, f_models):
        internal_data = [f_states(s) for s in self._states]
        models_data = [f_models(m) for m in self._models]
        total = [np.array(internal_data)] + models_data
        total_flat = reduce(lambda a, b: np.concatenate((a, b)), total)
        assert len(total_flat) == self._num_states, "Flatten worked."
        return total_flat

    def __proc_signals(self, pstate, pder, pin, pvar, pmodel):
        for s in self._states:
            pstate(s)
            pder(s)
        for u in self._inputs:
            pin(u)
        for v in self._vars:
            pvar(v)
        for m in self._models:
            pmodel(m)

    def _proc_signals(self, psignal, pmodel):
        self.__proc_signals(psignal,
                            lambda d: psignal(self._der(d)),
                            psignal,
                            psignal,
                            pmodel
                            )

    def _fmap_signals(self, f_signal, f_models):
        res = []
        for s in self._states:
            res.append(f_signal(s))
            res.append(f_signal(self._der(s)))
        for u in self._inputs:
            res.append(f_signal(u))
        for v in self._vars:
            res.append(f_signal(v))

        res_models = [f_models(m) for m in self._models]
        assert res is not None, res
        assert res_models is not None, res_models
        total = [res] + res_models
        assert total is not None

        total_flat = reduce(lambda a, b: a + b, total)

        assert total_flat is not None

        num = self.nsignals()
        assert len(total_flat) == num, f"Flatten failed: expected {num} results. Got {len(total_flat)} instead."
        return total_flat

    def __setattr__(self, key, value):
        # self._l.debug(f"Setting attribute {key}={str(value)}.")
        if key == '_bypass_set_attr' or self._bypass_set_attr:
            super().__setattr__(key, value)
        elif self._under_construction:
            """
            When under construction, a trick is done to record the variables being declared.
            """
            # value as a lambda that we can use to recover the parameters of the variable being declared.
            if callable(value):
                # We recover the LHS of the assignment using the key
                super().__setattr__(key, value(key))
            elif isinstance(value, Model):
                # Submodel being instantiated
                super().__setattr__(key, self.model(key, value))
            else:
                super().__setattr__(key, value)
        else:
            """
            Overrides the assignment operation to something sensible.
            - When a state is assigned, this is actually the current value of the state that is being assigned, 
                and not the state function.
            - When an input is assigned, this is the input function that is assigned, so this does not need special treatment.
            """
            assert hasattr(self, key), "Not allowed to set new fields on an object. Set them in the constructor."
            if key in self._current_state_values.keys():
                # self._l.debug(f"Setting current state {key}={str(value)}.")
                self._current_state_values[key] = value
            elif key in self._inputs:
                # works for states, parameters, and also other inputs
                # and preserves the ability to get the history of an input.
                if callable(value):
                    # self._l.debug(f"Setting input to given callable {key}={str(value)}.")
                    fun = value
                else:
                    # self._l.debug(f"Setting input to wrapped callable {key}={str(value)}.")
                    fun = lambda: value
                super().__setattr__(key, self._get_signal_function(key, fun))
            else:
                msg = """Not allowed to redefine vars. 
                Either define them as inputs if you want to assign them after the constructor; 
                or define a new python field that can be assigned and read by the variable function."""
                assert key not in self._vars, msg
                super().__setattr__(key, value)

    @staticmethod
    def _find_sup(t, ts):
        assert (len(ts) > 0)
        idx = len(ts) - 1  # Start at the end
        while ts[idx] > t and idx > 0:
            idx -= 1
        assert (idx == len(ts) - 1 or idx == 0 or (
                    ts[idx] <= t and ts[idx + 1] > t)), "Idx lies within the correct domain."
        assert 0 <= idx <= len(ts) - 1, "Idx lies within the correct domain."
        return idx

    def discrete_step(self):
        """
        Override this when doing discrete time computations.
        This method will be executed approximately every time a max_step is completed in the ModelSolver.
        :return: True if any internal state as change as a result of the step.
            This informs the ModelSolver to get the updated state.
        """
        internal_models_changed = False
        for m in self._models:
            if getattr(self, m).discrete_step():
                internal_models_changed = True
        return internal_models_changed
