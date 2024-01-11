from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Tuple, Optional, NamedTuple

import numpy as np
from matplotlib import pyplot as plt
from sklearn.svm import LinearSVC

from agile_ai.data_marshalling.numeric_types import FloatN3, FloatN2, IntN, BoolN, FloatND, FloatN
from agile_ai.injection.interfaces import Service


class SvmExemplars(NamedTuple):
    X: FloatND
    y: IntN
    Mp: BoolN

    @staticmethod
    def from_points_and_mask(X, mask) -> SvmExemplars:
        y = np.zeros(len(X), dtype=int)
        y[mask] = 1
        return SvmExemplars(X, y, mask)

    @staticmethod
    def from_points_and_labels(X, labels) -> SvmExemplars:
        mask = labels == 1
        return SvmExemplars(X, labels, mask)

    def with_labels(self, labels: IntN) -> SvmExemplars:
        return SvmExemplars.from_points_and_labels(self.X, labels)

    def with_points(self, points) -> SvmExemplars:
        return SvmExemplars(points, self.y, self.Mp)

    @property
    def Mn(self) -> BoolN:
        return ~self.Mp

    @property
    def Xp(self) -> FloatN2:
        return self.X[self.Mp]

    @property
    def Xn(self) -> FloatN2:
        return self.X[self.Mn]

    def visualize(self, show=True):
        import matplotlib.pyplot as plt
        plt.scatter(*self.Xp.T[:2], color='c')
        plt.scatter(*self.Xn.T[:2], color='r')
        if show:
            plt.show()


class EmbeddedSvmEstimator(Service, ABC):
    exemplars_2D: SvmExemplars
    exemplars_ND: SvmExemplars
    predictions_2D: SvmExemplars
    predictions_ND: SvmExemplars
    embedding_parameters: Tuple
    svc: LinearSVC
    normal: FloatN
    intercept: FloatN

    def set_exemplars(self, exemplars_2D: SvmExemplars):
        self.exemplars_2D = exemplars_2D

    @abstractmethod
    def embed_exemplars(self, *args, **kwargs):
        raise NotImplementedError

    def visualize_exemplars_2D(self):
        self.exemplars_2D.visualize()

    def visualize_exemplars_ND(self):
        Xp = self.exemplars_ND.Xp
        Xn = self.exemplars_ND.Xn
        self.visualize_3D([(Xp, 'c'), (Xn, 'r')])

    def visualize_predictions_ND(self, show=True):
        Xp = self.predictions_ND.Xp
        Xn = self.predictions_ND.Xn
        return self.visualize_3D([(Xp, 'c'), (Xn, 'r')], (self.normal, self.intercept), show=show)

    def visualize_predictions_2D(self, show=True):
        self.predictions_2D.visualize(show=show)

    @staticmethod
    def visualize_3D(points_and_colors: List[Tuple[FloatN3, str]], normal_intercept: Optional[Tuple] = None, show=True):
        # Create a plot
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for points, color in points_and_colors:
            ax.scatter(*points.T, color=color)

        # Plot the decision plane
        if normal_intercept:
            w, b = normal_intercept
            xx, yy = np.meshgrid(range(-1, 2), range(-1, 2))
            zz = (w[0] * xx + w[1] * yy + b) / -w[2]
            ax.plot_surface(xx, yy, zz, alpha=0.5)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        if show:
            plt.show()
        return ax

    @abstractmethod
    def compute_parameters(self):
        pass

    def fit(self):
        self.svc = LinearSVC()  # (dual="auto", random_state=0, tol=1e-5)
        self.svc.fit(self.exemplars_ND.X, self.exemplars_ND.y)
        self.normal = self.svc.coef_[0]
        self.intercept = self.svc.intercept_
        labels = self.svc.predict(self.exemplars_ND.X)
        self.predictions_ND = self.exemplars_ND.with_labels(labels)
        self.predictions_2D = self.exemplars_2D.with_labels(labels)
        self.compute_parameters()
