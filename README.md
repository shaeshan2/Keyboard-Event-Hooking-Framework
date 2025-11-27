**HOW TO SETUP ENVIRONMENT**
-Make sure input monitoring and accessibility for the code editor(VS code, pycharm) you are using is turned on in settings

**For Mac**
1. Open Settings
2. Go to privacy and security
3. Go to Accessibility --> Enable it for the code editor you are using
4. Go to Accessibility --> Input Monitoring --> Enable for code editor (it will restart app)


**HOW TO RUN CODE**

**For Mac**
1. Change lines 34, 35 and 37 to a burner email for test cases and learning purposes only
  1.1 2FA Must be enabled and you need to generate an app password on gmail app (16 digit code)
2. On line 46 add the key from GenerateKey.py
3. In DecryptFile.py add the key from GenerateKey.py
4. Run code as is
5. Use 'ESC' key to terminate program and successfuly log keystrokes

**For Windows**
1. Change this import on line 13 "import pyperclip" to "import win32clipboard"
2. Change this on line 46 "extend = "/"" to "extend = "\\""
3. Change lines 34, 35 and 37 to a burner email for test cases and learning purposes only
   3.1 2FA Must be enabled and you need to generate an app password on gmail app (16 digit code)
4. On line 46 add the key from GenerateKey.py
5. In DecryptFile.py add the key from GenerateKey.py
6. Run code after makign above changes
7. Use 'ESC' key to terminate program and successfuly log keystrokes
