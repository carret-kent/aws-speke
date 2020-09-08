import base64
import xml.etree.ElementTree as element_tree
import xml.etree.ElementTree as Element

HLS_AES_128_KEY_FORMAT = ''  # 'identity'
HLS_AES_128_KEY_FORMAT_VERSIONS = ''  # '1'

"""
Build SPEKE Response
"""
class SpekeResponseBuilder:
    def __init__(self, body: str, content_id: str, key_id: str, secret: str, derived_url: str):
        self.error_message = ''
        self.root = element_tree.fromstring(body)
        self.content_id = content_id
        self.key_id = key_id
        self.secret = secret
        self.derived_url = derived_url

        element_tree.register_namespace("cpix", "urn:dashif:org:cpix")
        element_tree.register_namespace("pskc", "urn:ietf:params:xml:ns:keyprov:pskc")
        element_tree.register_namespace("speke", "urn:aws:amazon:com:speke")
        element_tree.register_namespace("ds", "http://www.w3.org/2000/09/xmldsig#")
        element_tree.register_namespace("enc", "http://www.w3.org/2001/04/xmlenc#")

    def build(self):
        for drm_system in self.root.findall("./{urn:dashif:org:cpix}DRMSystemList/{urn:dashif:org:cpix}DRMSystem"):
            ext_x_key = self.derived_url
            drm_system.find("{urn:dashif:org:cpix}URIExtXKey").text=base64.b64encode(ext_x_key.encode('utf-8')).decode('utf-8')
            drm_system.find("{urn:aws:amazon:com:speke}KeyFormat").text=base64.b64encode(HLS_AES_128_KEY_FORMAT.encode('utf-8')).decode('utf-8')
            drm_system.find("{urn:aws:amazon:com:speke}KeyFormatVersions").text = base64.b64encode(HLS_AES_128_KEY_FORMAT_VERSIONS.encode('utf-8')).decode('utf-8')
            self.safe_remove(drm_system, "{urn:dashif:org:cpix}ContentProtectionData")
            self.safe_remove(drm_system, "{urn:aws:amazon:com:speke}ProtectionHeader")
            self.safe_remove(drm_system, "{urn:dashif:org:cpix}PSSH")

        for content_key in self.root.findall("./{urn:dashif:org:cpix}ContentKeyList/{urn:dashif:org:cpix}ContentKey"):
            data = element_tree.SubElement(content_key, "{urn:dashif:org:cpix}Data")
            secret = element_tree.SubElement(data, "{urn:ietf:params:xml:ns:keyprov:pskc}Secret")
            plain_value = element_tree.SubElement(secret, "{urn:ietf:params:xml:ns:keyprov:pskc}PlainValue")

            plain_value.text = base64.b64encode(self.secret).decode('utf-8')

    def safe_remove(self, element, match):
        """
        Helper to remove an element only if it exists.
        """
        if element.find(match):
            element.remove(match)

    def get_response(self):
        """
        Get the key request response as an HTTP response.
        """
        self.build()
        if self.error_message:
            return {"isBase64Encoded": False, "statusCode": 500, "headers": {"Content-Type": "text/plain"}, "body": self.error_message}

        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/xml",
                "Speke-User-Agent": "SPEKE Reference Server (https://github.com/awslabs/speke-reference-server)"
            },
            "body": element_tree.tostring(self.root).decode('utf-8')
        }


