from typing import Any

from nptyping import NDArray, Float, Int, Bool

Float4 = NDArray[(4,), Float]
Float3 = NDArray[(3,), Float]
Float2 = NDArray[(2,), Float]
Float3N = NDArray[(3, Any), Float]
Float33 = NDArray[(3, 3), Float]
Float44 = NDArray[(4, 4), Float]
Float2N = NDArray[(2, Any), Float]
FloatN3 = NDArray[(Any, 3), Float]
FloatN2 = NDArray[(Any, 2), Float]
FloatN = NDArray[(Any,), Float]
BoolN = NDArray[(Any,), Bool]
IntN = NDArray[(Any,), Int]
Int3 = NDArray[(3,), Int]

Float2D = NDArray[(Any, Any), Float]
Int2D = NDArray[(Any, Any), Float]
Bool2D = NDArray[(Any, Any), Float]

Float3D = NDArray[(Any, Any, Any), Float]
Int3D = NDArray[(Any, Any, Any), Float]
Bool3D = NDArray[(Any, Any, Any), Float]
