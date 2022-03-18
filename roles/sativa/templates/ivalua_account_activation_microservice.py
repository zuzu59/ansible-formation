"""
IValuaAccountActivationMicroservice
"""
import logging, json, requests
from satosa.logging_util import satosa_logging
from satosa.micro_services.base import ResponseMicroService

logger = logging.getLogger(__name__)


class IValuaAccountActivationMicroservice(ResponseMicroService):
  """
  Just before allowing SAML authentication to complete, call the iValua account
  revalidation Web service.
  """

  def __init__(self, config, internal_attributes, *args, **kwargs):
    super().__init__(*args, **kwargs)
    satosa_logging(logger, logging.DEBUG, "ivalua microservice init", None)
    satosa_logging(logger, logging.DEBUG, json.dumps(config), None)
    self.websrv = config['epfl']['websrv']
    self.catalyse = config['epfl']['catalyse']

  def process(self, context, internal_response):
    """
    Manage consent and attribute filtering

    :type context: satosa.context.Context
    :type internal_response: satosa.internal.InternalData
    :rtype: satosa.response.Response

    :param context: response context
    :param internal_response: the response
    :return: response
    """
    satosa_logging(logger, logging.DEBUG, "ivalua microservice process", "XXX")

    # import pydevd; pydevd.settrace(open("/tmp/DEBUG-HOST").read(), port=int(open("/tmp/DEBUG-PORT").read()),  stdoutToServer=True, stderrToServer=True)

    satosa_logging(logger, logging.DEBUG, json.dumps(internal_response.data['attributes']), None)
    self.sciper = internal_response.data['subject_id']
    satosa_logging(logger, logging.DEBUG, self.sciper, None)


    try:
      if self.get_sig0000(self.sciper):
        self.postToCatalyse(self.sciper)
    except Exception as e:
      satosa_logging(logger, logging.ERROR, repr(e) + traceback.format_exc(), None)

    # import pydevd; pydevd.settrace(open("/tmp/DEBUG-HOST").read(), port=int(open("/tmp/DEBUG-PORT").read()),  stdoutToServer=True, stderrToServer=True)

    return super().process(context, internal_response)

  def get_sig0000(self, sciper):
    qs = {
      'app': self.websrv['app_name'],
      'caller': self.websrv['app_caller'],
      'password': self.websrv['app_password'],
      'rightid': 'sig0000',
      'persid': sciper,
    }
    url = self.websrv['url'] + 'cgi-bin/rwsaccred/getRights?' # mind the ?
    satosa_logging(logger, logging.DEBUG, "Getting data from %s " %  url, None)

    r = requests.get(url, params=qs)
    satosa_logging(logger, logging.DEBUG, "get_sig0000 status %d" %  r.status_code, None)

    if r.status_code != 200:
      satosa_logging(logger, logging.ERROR, "Non-200 response, body is %s" % r.text, None)

    response = json.loads(r.text)

    if not response.get('result'):
      satosa_logging(logger, logging.ERROR, "Negative API response: %s" % r.text, None)
      return false

    return len(response['result']) > 0

  def postToCatalyse(self, sciper):
    url = self.catalyse['url'] + 'User_VAL?apikey=' + self.catalyse['key']
    payload = '<User_VALs><User_VAL><LOGIN_NAME>'+sciper+'</LOGIN_NAME></User_VAL></User_VALs>'
    headers = {'Content-Type': 'application/xml'}

    r = requests.post(url=url, data=payload, headers=headers)
    satosa_logging(logger, logging.DEBUG, "postToCatalyse status %d" % r.status_code, None)
    return r.status_code == 200
