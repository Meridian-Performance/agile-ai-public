from typing import Any

from nptyping import NDArray, Float, Int, Bool, Shape

Float4 = NDArray[Shape["4"], Float]
Float3 = NDArray[Shape["3"], Float]
Float2 = NDArray[Shape["2"], Float]
Float3N = NDArray[Shape["3, Any"], Float]
Float33 = NDArray[Shape["3, 3"], Float]
Float44 = NDArray[Shape["4, 4"], Float]
Float2N = NDArray[Shape["2, Any"], Float]
FloatN3 = NDArray[Shape["Any, 3"], Float]
FloatN2 = NDArray[Shape["Any, 2"], Float]
FloatN = NDArray[Any, Float]
BoolN = NDArray[Any, Bool]
IntN = NDArray[Any, Int]
Int3 = NDArray[Shape["3"], Int]

Float2D = NDArray[Shape["Any, Any"], Float]
Int2D = NDArray[Shape["Any, Any"], Float]
Bool2D = NDArray[Shape["Any, Any"], Float]

Float3D = NDArray[Shape["Any, Any, Any"], Float]
Int3D = NDArray[Shape["Any, Any, Any"], Float]
Bool3D = NDArray[Shape["Any, Any, Any"], Float]
