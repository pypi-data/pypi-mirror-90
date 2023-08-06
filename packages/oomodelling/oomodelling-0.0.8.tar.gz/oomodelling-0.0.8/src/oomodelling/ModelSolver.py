import logging

import numpy as np
from scipy.integrate import solve_ivp, RK45

from oomodelling.Model import Model


class ModelSolver:
    def __init__(self):
        super().__init__()
        self._l = logging.getLogger("ModelSolver")

    def simulate(self, model: Model, start_t, stop_t, h, t_eval=None):
        model.set_time(start_t)
        model.assert_initialized()
        f = model.derivatives()
        x = model.state_vector()
        # Record first time.
        model.record_state(x, start_t)
        sol = solve_ivp(f, (start_t, stop_t), x, method=StepRK45, max_step=h, model=model, t_eval=t_eval)
        if not sol.success:
            raise ValueError(sol)
        if t_eval is not None:
            expected = len(t_eval)
            results_len = len(sol.y[0])
            assert expected == results_len, f"t_eval was ignored. Expected {expected} results. " \
                                            f"Got {results_len} instead. " \
                                            "This is a problem with scipy solver or you used the wrong type for t_eval."
            model_signals = len(model.signals["time"])
            if not expected == model_signals:
                self._l.info(f"The signals attribute is computed based on max_step and not based on t_eval. "
                             f"Therefore model.signals contains {model_signals} points and t_eval contains {expected} points."
                             f"Using t_eval implies that you rely on sol.y instead of the stored signals.")

        return sol


class StepRK45(RK45):

    def __init__(self, fun, t0, y0, t_bound, max_step=np.inf,
                 rtol=1e-3, atol=1e-6, vectorized=False,
                 first_step=None, **extraneous):
        assert max_step<np.inf, "Max step is infinity."
        self._model: Model = extraneous.pop('model')
        super().__init__(fun, t0, y0, t_bound, max_step=max_step,
                 rtol=rtol, atol=atol, vectorized=vectorized,
                 first_step=first_step, **extraneous)

    def step(self):
        msg = super().step()
        if msg is not None:
            raise ValueError(msg)
        step_taken = self.t - self._model.get_last_commit_time()
        if step_taken >= self.max_step:  # Improves performance by not recording every sample.
            self._model.record_state(self.y, self.t)
            update_state = self._model.discrete_step()
            if update_state:
                self.y = self._model.state_vector()
            assert np.isclose(self.t, self._model.get_last_commit_time()), "Commit was made to the model."
