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
    secrets_json_path = "{{ satosa_secrets_mountpoint }}/secrets.json"
    self.secrets = json.loads(open(secrets_json_path).read())
    satosa_logging(logger, logging.INFO, "Loaded secrets from %s" % secrets_json_path, None)

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
    satosa_logging(logger, logging.INFO, "Ivalua microservice process", context.state)

    # import pydevd; pydevd.settrace(open("/tmp/DEBUG-HOST").read(), port=int(open("/tmp/DEBUG-PORT").read()),  stdoutToServer=True, stderrToServer=True)

    try:
      satosa_logging(logger, logging.DEBUG, "Attributes : %s" % json.dumps(internal_response.data['attributes']), context.state)
      # Get SCIPER (SAML NameID => subject_id)
      self.sciper = internal_response.data['subject_id']
      satosa_logging(logger, logging.DEBUG, "SCIPER = %s" % self.sciper, context.state)

      # Get Catalyse URL from SP entity ID URL ex "sp_entity_id"="https://catalyse-test-proj.epfl.ch"
      self.sp_entity_id = context.state[context.state["ROUTER"]]["resp_args"]["sp_entity_id"]
      satosa_logging(logger, logging.DEBUG, "SP entity id = %s" % self.sp_entity_id, context.state)
    except Exception as e:
      satosa_logging(logger, logging.ERROR, repr(e) + traceback.format_exc(), context.state)

    try:
      if self.get_sig0000(self.sciper):
        if self.postToCatalyse(self.sciper, self.sp_entity_id):
          satosa_logging(logger, logging.INFO, "User %s was successfully validated in Ivalua" %  self.sciper, context.state)
    except Exception as e:
      satosa_logging(logger, logging.ERROR, repr(e) + traceback.format_exc(), context.state)

    # import pydevd; pydevd.settrace(open("/tmp/DEBUG-HOST").read(), port=int(open("/tmp/DEBUG-PORT").read()),  stdoutToServer=True, stderrToServer=True)

    return super().process(context, internal_response)

  def get_sig0000(self, sciper):
    qs = {
      'app': self.websrv['app_name'],
      'caller': self.websrv['app_caller'],
      'password': self.secrets['websrv_password'],
      'rightid': 'sig0000',
      'persid': sciper,
    }
    url = self.websrv['url'] + 'cgi-bin/rwsaccred/getRights?' # mind the ?
    satosa_logging(logger, logging.DEBUG, "Getting data from %s " %  url, None)

    r = requests.get(url, params=qs, allow_redirects=False)
    satosa_logging(logger, logging.INFO, "get_sig0000 status %d" %  r.status_code, None)

    if r.status_code != 200:
      satosa_logging(logger, logging.ERROR, "Non-200 response, body is %s" % r.text, None)

    response = json.loads(r.text)

    if not response.get('result'):
      satosa_logging(logger, logging.ERROR, "Negative API response: %s" % r.text, None)
      return False

    return len(response['result']) > 0

  def postToCatalyse(self, sciper, sp_entity_id = ''):
    if sp_entity_id !='':
      url = sp_entity_id + "/page.aspx/en/eai/api/"
    else:
      url = self.catalyse['url']
    url = url + 'User_VAL'
    satosa_logging(logger, logging.INFO, "Updating data to %s" % url, None)

    url = url + '?apikey=' + self.secrets['catalyse_key'] # add apikey
    payload = '<User_VALs><User_VAL><LOGIN_NAME>'+sciper+'</LOGIN_NAME></User_VAL></User_VALs>'
    headers = {'Content-Type': 'application/xml'}

    r = requests.post(url=url, data=payload, headers=headers, allow_redirects=False)
    satosa_logging(logger, logging.DEBUG, "postToCatalyse status %d" % r.status_code, None)
    if r.status_code != 200:
      satosa_logging(logger, logging.ERROR, "Non-200 response, body is %s" % r.text, None)

    return r.status_code == 200
