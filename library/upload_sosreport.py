#!/usr/bin/python

# Copyright: (c) 2023, Stephane Vigan <stef@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: upload_sosreport

short_description: Upload Sosreport to Red Hat Portal

version_added: "1.0.0"

description: Upload sosreport to Red Hat Support Case

options:
    username:
        description: Red Hat Portal Login
        required: true
        type: str
    password:
        description: Red Hat Portal Password
        required: true
        type: str
    case:
        description: Red Hat support case number
        required: true
        type: str
    file:
        description: The path to the file which has to be uploaded
        required: true
        type: path
    desc:
        description: Attached file description
        required: false
        type: str
author:
    - Stephane Vigan (@tinsjourney)
'''

EXAMPLES = r'''
 - name: 'Upload sosreport to case'
   upload_sosreport:
     username: "my_redhat_portal_user"
     password: "my_redhat_portal_password"
     case: "01234567"
     file: "files/sosreport-xxxxxxxx.tar.xz"
     desc: "sosreport from node1"

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
status_code:
  description: The HTTP Status Code of the response
  returned: success
  type: int
  sample: 201
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import json
from os import environ

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        case=dict(type='str', required=True),
        file=dict(type='path', required=True),
        desc=dict(type='str'),
        proxy=dict()
    )


    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    url =  "https://api.access.redhat.com/support/v1/cases/" + module.params['case'] + "/attachments/"

    try:
      filename = {
        'file': open(module.params['file'], 'rb')
      }
    except FileNotFoundError:
      module.fail_json(msg=module.params['file'] + ' does not exist', **result)

    data = {
      'description': module.params['desc']
    }

    try:
      if module.params['proxy']:
        r = requests.post(url, files=filename, data=data, proxies=module.params['proxy'], auth=(module.params['username'], module.params['password']))
      else:
        r = requests.post(url, files=filename, data=data, auth=(module.params['username'], module.params['password']))
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
      result['changed'] = False
      module.fail_json(msg=errh.args[0], **result)
    

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if r.status_code == 201:
        result['changed'] = True
        result['message'] = json.dumps(r.json(), indent=2)
    else:
        result['changed'] = False
        result['message'] = json.dumps(r.json(), indent=2)

    r.close()

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()


