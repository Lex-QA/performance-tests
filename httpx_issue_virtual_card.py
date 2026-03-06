import time

import httpx

create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

open_debit_card_account_payload = {
    "userId": f"{create_user_response_data['user']['id']}"
}

open_debit_card_account_response = httpx.post("http://localhost:8003/api/v1/accounts/open-debit-card-account",
                                           json=open_debit_card_account_payload)
open_debit_card_account_response_data = open_debit_card_account_response.json()

print(open_debit_card_account_response_data)