Feature: User Invitation

  Scenario: Registered user invites a new user
    Given the invitee is registered
    And the invited user is NOT registered
    And the invite is valid
    When invitation is requested
    Then the server responds with a success code
    And the response contains the payload sent by the user
    And the signature is valid
    And sends an email to the invited user
    And the DB contains a new invite

  Scenario: Non-registered user invites a new user
    Given the invitee is NOT registered
    And the invited user is NOT registered
    And the invite is valid
    When invitation is requested
    Then the server responds with a Not Found code

  Scenario: Inviting a user that is already registered
    Given the invitee is registered
    And the invited user is already registered
    And the invite is valid
    When invitation is requested
    Then the server responds with a Bad Request code

  Scenario Outline: User does not include the "<parameter>" parameter in the POST request
    Given the invitee is registered
    And the invited user is already registered
    And the invite is valid
    When invitation is requested without the "<parameter>" parameter
    Then the server responds with a Bad Request code

    Examples:
      | parameter |
      | author    |
      | payload   |
      | signature |

  Scenario Outline: The invite is missing attribute <attribute>
    Given the invitee is registered
    And the invited user is not registered
    But the payload is missing "<attribute>" attribute
    When invitation is requested
    Then the server responds with a Bad Request code

    Examples:
      | attribute |
      | invitee   |
      | invited   |

  Scenario: User making the invitation is not the same as the one in the
    Given the invitee is registered
    And the invited user is not registered
    But the invite's ID does not match the ID of the author
    When Invitation is requested
    Then the server responds with a Bad Request code
