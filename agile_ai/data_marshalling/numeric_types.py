from typing import Any
from typing import Any, Literal
import numpy as np
import numpy.typing as npt

# --- Base NDArray Types by Precision/Dtype ---
# Note: npt.NDArray[np.float64] typed with tuple shapes works with modern static type checkers.

# 1D fixed shapes
Float4 = np.ndarray[tuple[Literal[4]], np.dtype[np.float64]]
Float3 = np.ndarray[tuple[Literal[3]], np.dtype[np.float64]]
Float2 = np.ndarray[tuple[Literal[2]], np.dtype[np.float64]]
Int3 = np.ndarray[tuple[Literal[3]], np.dtype[np.int64]]

# Fixed 2D shapes
Float33 = np.ndarray[tuple[Literal[3], Literal[3]], np.dtype[np.float64]]
Float44 = np.ndarray[tuple[Literal[4], Literal[4]], np.dtype[np.float64]]

# Dynamic 1D arrays (Unspecified size)
FloatN = npt.NDArray[np.float64]
IntN = npt.NDArray[np.int64]
BoolN = npt.NDArray[np.bool_]

# Dynamic 2D arrays with specific fixed dimension counts
Float3N = np.ndarray[tuple[Literal[3], Any], np.dtype[np.float64]]
Float2N = np.ndarray[tuple[Literal[2], Any], np.dtype[np.float64]]
FloatN3 = np.ndarray[tuple[Any, Literal[3]], np.dtype[np.float64]]
FloatN2 = np.ndarray[tuple[Any, Literal[2]], np.dtype[np.float64]]
IntN2 = np.ndarray[tuple[Any, Literal[2]], np.dtype[np.int64]]

# Explicit 2D general shapes
Float2D = np.ndarray[tuple[Any, Any], np.dtype[np.float64]]
Int2D = np.ndarray[tuple[Any, Any], np.dtype[np.int64]]
Bool2D = np.ndarray[tuple[Any, Any], np.dtype[np.bool_]]
FloatND = Float2D  # Alias matching your original script

# Explicit 3D general shapes
Float3D = np.ndarray[tuple[Any, Any, Any], np.dtype[np.float64]]
Int3D = np.ndarray[tuple[Any, Any, Any], np.dtype[np.int64]]
Bool3D = np.ndarray[tuple[Any, Any, Any], np.dtype[np.bool_]]
