Changelog
=========


1.0.5 (2021-01-04)
------------------

- Improve Anysurfer integration.
  [bsuttor]

- Added revoke-user-access page to remove a user from its groups and revoke its roles.
  [odelaere]


1.0.4 (2020-10-08)
------------------

- Plugin also provide IUserIntrospection so user from Authentic PAS plugin will also listed in api.user.get_users().
  [bsuttor]

- Use IItem for Object to redirect imio_login instead of INavigation. It's solved bug to redirect from other page than root navigation, and so page which required access.
  [bsuttor]

- Fix redirect after login for Plone < 5.2.
  [odelaere]


1.0.3 (2020-07-30)
------------------

- Add Plone 5 testing profile.
  [bsuttor]


1.0.2 (2020-07-16)
------------------

- Fix(testing profile): dependency of plone4 profile do not exists, use default.
  [bsuttor]


1.0.1 (2020-07-16)
------------------

- Add plone 4 testing profile.
  [bsuttor]

- Do not install usager login by default.
  [bsuttor]

- Fix: import zcml permission from plone.app.controlpanel
  [bsuttor]


1.0.0 (2020-05-29)
------------------

- Fix: set username on python3 when new user added.
  [bsuttor]


1.0b11 (2020-03-27)
-------------------

- Also see came_from on request for next url.
  [bsuttor]


1.0b10 (2020-03-27)
-------------------

- Fix: redirect on homepage.
  [bsuttor]

- Improve next_url login.
  [bsuttor]


1.0b9 (2020-02-26)
------------------

- Use state / user_state to redirect to page which apply SSO.
  [bsuttor]


1.0b8 (2020-02-21)
------------------

- Set talk less.
  [bsuttor]


1.0b7 (2020-02-11)
------------------

- Fix french typo.
  [bsuttor]


1.0b6 (2020-02-07)
------------------

- Add plone.app.changeownership dependency.
  [bsuttor]


1.0b5 (2020-02-07)
------------------

- Improve python3 compatibility, check if python 2 before safe_utf8.
  [bsuttor]


1.0b4 (2020-02-07)
------------------

- Bad release.
  [bsuttor]


1.0b3 (2020-02-07)
------------------

- Override plone userlist page to add link to WCA on Plone 5.
  [bsuttor]

- Add zope_login to bypass SSO auth.
  [bsuttor]


1.0b2 (2020-02-04)
------------------

- Fix python3 EnumerateUsers.
  [bsuttor]

- Override plone userlist page to add link to WCA.
  [bsuttor]


1.0b1 (2019-12-16)
------------------

- Python 3 support.
  [bsuttor]


1.0a10 (2019-11-18)
-------------------

- Add css for login-page
  [bsuttor]

- Add fr translations.
  [bsuttor]


1.0a9 (2019-11-05)
------------------

- Override default login_form template (with z3c.jbot) to allow login with zope admin and an external url set.
  [bsuttor]


1.0a8 (2019-09-04)
------------------

- Set Site Manager role to user with admin of service role on Authentic.
  [bsuttor]


1.0a7 (2019-06-28)
------------------

- Set Manager role if you are into admin role on Authentic.
  [bsuttor]

- Add Member role to user connected with Authentic.
  [bsuttor]


1.0a6 (2019-05-20)
------------------

- Get logout hostname redirect from agents config.
  [bsuttor]

- Add roles scope on agents.
  [bsuttor]


1.0a5 (2019-05-09)
------------------

- Add userfactories to connect with email for usagers and with userid of agents.
  [bsuttor]


1.0a4 (2019-04-26)
------------------

- Use different OU for usagers and agents.
  [bsuttor]


1.0a3 (2019-04-25)
------------------

- Use different usagers and agents environement variables to connect to SOO.
  [bsuttor]


1.0a2 (2019-04-25)
------------------

- Use agents and usagers to connect to Plone.
  [bsuttor]


1.0a1 (2018-03-28)
------------------

- Initial release.
  [bsuttor]
