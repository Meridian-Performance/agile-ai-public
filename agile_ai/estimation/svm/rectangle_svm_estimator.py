import numpy as np

from agile_ai.estimation.svm.embedded_svm_estimator import EmbeddedSvmEstimator


class RectangleSvmEstimator(EmbeddedSvmEstimator):
    def embed_exemplars(self, x_split: float):
        Px, Py = self.exemplars_2D.X.T
        Pz = abs(Px - x_split)
        Xup = np.array((Px, Py, Pz)).T
        self.exemplars_ND = self.exemplars_2D.with_points(Xup)

