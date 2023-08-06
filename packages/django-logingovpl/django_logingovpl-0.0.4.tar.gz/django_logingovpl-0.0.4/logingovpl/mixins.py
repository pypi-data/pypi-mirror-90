import logging

from django.conf import settings
from django.template.loader import render_to_string

import requests
import urllib3

from .services import add_sign
from .utils import get_issue_instant

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

logger = logging.getLogger(__name__)


class ACSMixin:
    def resolve_artifact(self, saml_art):
        xml = render_to_string(
            'ArtifactResolve.xml',
            {
                'artifact_resolve_issue_instant': get_issue_instant(),
                'artifact_resolve_artifact': saml_art,
                'issuer': settings.LOGINGOVPL_ISSUER,
            },
        )

        signed = add_sign(
            xml, settings.LOGINGOVPL_ENC_KEY, settings.LOGINGOVPL_ENC_CERT,
        )

        try:
            response = requests.post(
                settings.LOGINGOVPL_ARTIFACT_RESOLVE_URL,
                data=signed,
                timeout=settings.LOGINGOVPL_TIMEOUT,
            )
        except requests.RequestException:
            logger.exception('ArtifactResolve service request failed:')
            raise

        return response
