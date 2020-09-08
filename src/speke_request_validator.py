import base64
import os
import xml.etree.ElementTree as element_tree
import xml.etree.ElementTree as Element

"""
Validate SPEKE request and get value
"""
class SpekeRequestValidator:
    def __init__(self, body: str, isEncoded: bool):
        self.body = base64.b64decode(body) if isEncoded else body
        self.root = element_tree.fromstring(body)
        self.content_id = self.root.get('id')

        for drm_system in self.root.findall("./{urn:dashif:org:cpix}DRMSystemList/{urn:dashif:org:cpix}DRMSystem"):
            self.kid = drm_system.get('kid')
            self.system_id = drm_system.get('systemId')

    """
    environ.system_id not match request.
    request has kid
    """
    def fail(self) -> bool:
        return os.environ['SYSTEM_ID'] != self.system_id or self.kid is None

    def get_body(self) -> str:
        return self.body

    def get_content_id(self) -> str:
        return self.content_id

    def get_key_id(self) -> str:
        return self.kid

    def get_root(self) -> Element:
        return self.root
