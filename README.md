Sosreport
=========

Generate, Retrieve and **upload** sosreport to Red Hat Customer Portal.

Requirements
------------

Ansible 2.9 minimum

Role Variables
--------------

Variables `default/main.yaml`

```
# Red Hat Customer Portal credentials
rhn_user: ""
rhn_pass: ""

# Where to store the sosreport on the managed node
sosreport_remote_location: "/var/tmp"

# Where to store the sosreport(s) on the controller
sosreport_local_location: "/var/tmp/{{ caseNumber }}"

# Should we delete sosreport from remote hosts, once downloaded locally
sosreport_delete_remote_sosreports: true
# Should we delete downloaded sosreport once uploaded
sosreport_delete_local_sosreports: true

# Sos default options
sosreport_options: "--log-size 4096 --all-logs"
# Extra options to pass to sos command
sosreport_extra_options: ""

# Upload to Red Hat ?
upload: true
```

Variables `vars/main.yaml`

```
sosreport_packages:
  - sos

sosreport_command: "sos report {{ sosreport_options }} {{ sosreport_extra_options }} --batch --tmp-dir {{ sosreport_remote_location }} --case-id {{ caseNumber }}"
```

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: "Generate and Send sosreports to Red Hat Customer Portal"
      hosts: "{{ nodes }}"
      become: true
      gather_facts: false

      roles:
        - role: tinsjourney.sosreport
          vars:
            - rhn_user: "my_user"
            - rhn_pass: "my_password"
            - caseNumber: "01234567"

License
-------

BSD

Author Information
------------------

[Stephane V.](https://www.gnali.org) : tinsjourney@mastodon.top

Special Thanks
--------------

Role inspired by [Michael Buluma](https://github.com/buluma/ansible-role-sosreport)
