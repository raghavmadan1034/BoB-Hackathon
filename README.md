Zero Trust API Security & Third-Party Risk Management - Testing Guide
=====================================================================

This guide will walk you through setting up the project, running the Flask application, and testing the API endpoints using Postman.

**1\. Setup Instructions**
--------------------------

Follow these steps to set up the project on your local machine:

### **1.1. Install Python**

Ensure that Python 3.8+ is installed on your system. You can check this by running:

`   python --version   `

If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

### **1.2. Set Up a Virtual Environment**

It's best practice to create a virtual environment for your project to avoid conflicts with other Python projects.

1.  Navigate to your project folder
    
        cd /path/to/your/project
    
2.  Create a virtual environment

        python -m venv venv
    
3.  Activate the virtual environment:
    
    *     venv\Scripts\activate  (For windows)
        
    *     source venv/bin/activate (For macOS/Linux)
        

### **1.3. Install Dependencies**

Once the virtual environment is activated, install the required Python packages by running the following command:

    pip install flask flask-jwt-extended flask-limiter flask-sqlalchemy

These dependencies include:

*   `flask`: The web framework for creating the API.
    
*   `flask-jwt-extended`: To handle JWT-based authentication.
    
*   `flask-limiter`: To implement rate-limiting.
    
*   `flask-sqlalchemy`: For SQLite database integration.
    

### **1.4. Run the Flask Application**

Once everything is set up, you can run the Flask app:

    python app.py   

The Flask server will start and run locally on `http://127.0.0.1:5000/`.

**2\. Testing the API Using Postman**
-------------------------------------

### **2.1. Install Postman**

If you don't already have Postman installed, download it from [here](https://www.postman.com/downloads/) and install it on your system.

### **2.2. Test the /login Endpoint**

To test the login and retrieve the JWT token:

1.  Open **Postman**.
    
2.  Create a **new POST request**.
    
3.  Set the URL to 
    
        http://127.0.0.1:5000/login
    
4.  Under the Body tab, select raw and choose JSON from the dropdown. Then, enter the following data:
    ```
    { 
        "username": "testuser", 
        "password": "password123"
    }
    ```
    
5.  Click **Send**.
    
    *   If the credentials are correct, you'll receive a response containing the JWT token:
        ```
        { 
            "access_token": "your_generated_jwt_token"
        }
        ```
        
    *   Copy the access\_token value, as you will need it to access other endpoints.
        

### **2.3. Test the /banking\_data Endpoint**

To access protected data using the JWT token:

1.  Create a **new GET request**.
    
2.  Set the URL to 
    
        http://127.0.0.1:5000/banking_data
    
3.  Under the **Authorization** tab, select **Bearer Token** and paste the JWT token you received from the /login endpoint into the **Token** field.
    
4.  Click **Send**.
    
    *   If the token is valid, you'll receive a response based on the role of the user:
        
        *   For an Admin role, the response will look like:
            ```
            { 
                "data": "Sensitive banking data here"
            }
            ```
            
        *   For a User role, the response will look like:
            ```
            { 
                "data": "Non-sensitive banking data here"
            }
            ```
            
5. If the token is not authorized or the role doesn't match, you will receive an error:  
    ```
    {
        "msg": "You are not authorized to access this data"
    }
    ```
    

### **2.4. Test the /transaction\_history Endpoint with Rate Limiting**

To test the rate limiting feature:

1.  Create a **new GET request**.
    
2.  Set the URL to 
    
        http://127.0.0.1:5000/transaction_history
    
3.  Under the **Authorization** tab, use the same **Bearer Token** as before.
    
4.  Click **Send**.
    
    * You should receive the transaction history data:   
        ```
        { 
            "data": "User's transaction history"
        }
        ```
        
5.  To test the rate-limiting, send multiple requests (more than 5 in one minute) to this endpoint. After exceeding the limit, you will receive:
    ```
    { 
        "msg": "ratelimit exceeded"
    }
    ```

This shows that the rate-limiting is working correctly.
    

**3\. Troubleshooting**
-----------------------

Here are some common issues and how to resolve them:

### **3.1. Flask App Not Running**

If the Flask app is not running, ensure that you have activated your virtual environment and run the following command:
    
    python app.py 

Make sure no errors appear in the terminal. If you see any errors, check the traceback for details and address the issue accordingly.

### **3.2. Invalid JWT Token**

If Postman returns an error like 401 Unauthorized, the JWT token may be invalid or expired. Simply log in again by sending a POST request to /login with valid credentials to get a new token.

### **3.3. Database Issues**

If there are issues related to the database, ensure that the tables are created correctly by running the following inside your Flask app:

    with app.app_context():      
        db.create_all()

