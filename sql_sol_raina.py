import requests 

generate_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

payload = {
   "name": "Raina Dhanyase",
    "regNo": "REG0871",
    "email": "rainadhanyase220245@acropolis.in"
}

response = requests.post(generate_url, json=payload)
if response.status_code != 200:
    raise Exception(f"Failed to generate webhook: {response.text}")

response_data = response.json()
webhook_url = response_data['webhook']
access_token = response_data['accessToken']

print(f"Webhook: {webhook_url}")
print(f"Access Token: {access_token}")

# TODO: Replace with your actual SQL query after solving
final_query = """SELECT 
    P.AMOUNT AS SALARY,
    CONCAT(E.FIRST_NAME, ' ', E.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, E.DOB, CURDATE()) AS AGE,
    D.DEPARTMENT_NAME
FROM PAYMENTS P
JOIN EMPLOYEE E ON P.EMP_ID = E.EMP_ID
JOIN DEPARTMENT D ON E.DEPARTMENT = D.DEPARTMENT_ID
WHERE DAY(P.PAYMENT_TIME) != 1
  AND P.AMOUNT = (
      SELECT MAX(AMOUNT)
      FROM PAYMENTS
      WHERE DAY(PAYMENT_TIME) != 1
  );
"""

# Step 3: Submit the final query
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
submission_payload = {
    "finalQuery": final_query
}

submission_response = requests.post(webhook_url, headers=headers, json=submission_payload)

if submission_response.status_code == 200:
    print("Successfully submitted the SQL query.")
else:
    print(f"Submission failed: {submission_response.status_code}, {submission_response.text}")