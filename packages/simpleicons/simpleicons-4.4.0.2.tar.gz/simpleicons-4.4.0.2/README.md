# simpleicons
Use a wide-range of icons derived from the [simple-icons](https://github.com/simple-icons/simple-icons) repo in python.

## XML
The XML for each icon can be easily manipulated with either of two functions:

`get_xml(icon_name: str, **attrs) -> ElementTree`
```
from simpleicons.icon_xml import get_xml

# blue logo (simply adds <svg fill="blue"></svg>)
get_xml("github", fill="blue")
```

`get_xml_bytes(icon_name: str, **attrs) -> bytes`
```
from simpleicons.icon_xml import get_xml_bytes

get_xml_bytes("github", fill="blue")
```

To simply get the unparsed XML string for each icon, use `get_str(icon_name: str) -> str`:
```
from simpleicons.icon_xml import get_str

get_str("github")
```
This string representation will allow for quick implementation in web pages, however it cannot be manipulated. Use `get_xml_bytes` for easy web page implementation alongside manipulation.

## Image
Icons can be converted to PIL Images with `icon_to_img(icon_xml: bytes, bg: int=0xffffff, scale: Tuple[int, int]=(1, 1)) -> Image`:
```
from simpleicons.icon_xml import get_xml_bytes
from simpleicons.image import icon_to_image

github_xml_bytes = get_xml_bytes("github", fill="blue")

# black background and x5 scale
icon_to_img(github_xml_bytes, bg=0x000000, scale=(5, 5))
```
