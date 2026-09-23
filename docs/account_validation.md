# TECHNICAL DOCUMENTATION

## Account Validation
Validating user information before creating an account protects both the platform and its users by ensuring data accuracy, security, and system integrity. Authentication, authorization and database constraints provide additional protection.

- **Validation** - Is the information supplied acceptable?
- **Authentication** - Has the person verified their claimed identity?
- **Authorization** - What is that person permitted to access?

## Name Validation (First and Last name)
- **Required**: the field cannot be submitted empty.
- **Not blank**: a field containing only spaces is treated as blank and rejected. If spaces are before or after name then an error message should be sent to the user. Internal spaces are approved
- **Maximum length**: 30 characters.
- **No digits**: numeric characters (0–9) are not allowed.
- **Allowed characters**: letters (including accented characters, e.g. é, ñ, ü), spaces, apostrophes ('), and hyphens (-).
- **No other symbols**: any character not listed above (e.g. @, #, $, %, &, *) is rejected.

## Email Validation
- required and cannot be blank
- maximum length — 50 characters is workable for TicketFlow v1, although real-world email addresses can be longer
- must have a valid basic email structure
- exactly one @
- must have something before the @
- must have a valid domain portion after it
- must be unique in the database

- why the UNIQUE database constraint is necessary even when Python checks whether an email address is already registered - Because Python's check and the database insert aren't atomic — two requests can both check at the same time, both see "email free," and both insert before either commits. The UNIQUE constraint blocks the second insert at the database level, closing that race condition. App checks are for UX; the constraint is what actually guarantees correctness.

## Password Validation

- Minimum 15 characters; accept at least 64.
- No mandatory character combinations.
- Allow spaces and passphrases.
- Reject commonly used and known compromised passwords.
- Store secure password hashes, never plaintext.
- Consider password-history checks as a later feature.

## Username generation and Validation

- first attempt: first initial + last name
- if taken: first two letters + last name
- then first three, and so on
- if the full first name + last name is still taken, append a number
- Employees do not select their usernames. TicketFlow generates them and provides them only after successful account creation.
- Python checks whether each proposed username is available. If it is taken, the application generates another candidate and tries again.
- SQLite's UNIQUE constraint provides the final protection against duplicate usernames, including when two registrations happen simultaneously.

## Department
- **Employee selects, administrator verifies** - During registration, employees select HR, Marketing, Sales or Operations. Their selection is treated as unverified until account approval. An administrator can correct it if necessary.

## Role Assignment

- **TicketFlow assigns, administrator controls** - New accounts receive the Employee role automatically but remain inactive. Only an authorized administrator can grant the Admin role.
- allowing self-assignment turns a permission system into a suggestion. The constraint isn't about distrust of any one employee — it's about making sure elevated access always requires independent approval, so one compromised or careless account can't cascade into full system compromise.

## Account Activation and Deactivation

- **What is_active controls** - is_active gates access independently of whether the credentials are correct. Even with a correct password, login should fail if is_active is false
- **Who can activate/deactivate accounts** - This should be restricted to Admins (or a specifically scoped role like HR/account-management), never the account owner themselves or arbitrary employees.
- **What happens to an existing session after deactivation** - every protected action must verify that the account is still active and has the necessary permissions. If the user is deactivated, their existing session should be invalidated, and their next protected action must be denied.
- **Why deactivate instead of delete** - Referential integrity — Preserving the account is useful because it maintains the user's identity and associated audit history. Audit trail — you often need to know who did what, even for former employees; deletion erases that. Reversibility — offboarding decisions (rehire, mistaken termination) can be undone; deletion can't. Data retention — deactivation helps organizations meet their applicable retention policies.