# About Environment Variables (For New people)

## Using OS Environment Variables

To use OS Environment Variables,

1. For Windows Powershell,
`$env:EMAIL_ID = "aanshojha@zohomail.in"`

2. For Bash,
`export EMAIL="aanshojha@zohomail.in"`

3. Python code to test:
```py
import os

# Get the value of the environment variable 'EMAIL'
email_value = os.environ.get('EMAIL')

# Check if the variable is set
if email_value is not None:
    print(f"The value of the environment variable 'EMAIL' is: {email_value}")
else:
    print("The environment variable 'EMAIL' is not set.")

```

### ⚠️ **Warning**

In the same terminal, same directory, same terminal session,
1. environment variable declaration,
2. running of python file

should be done. Otherwise use global variables or other options.