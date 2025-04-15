// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export const loginService = async (email, password) => {

    const payload = {
        email: email,
        password: password,
      }
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      credentials: 'include'
    };
    
    const response = await fetch(`${BACKEND_URL}/token`, requestOptions);
    if (response.status !== 200) {
      if (response.status == 401)
          throw new Error("Username or Password is incorrect");
      else {
          throw new Error("Login failed");
      }
    }
  
    const data = await response.json();
    return data;
  };

export const refreshToken = async () => {
  console.log("Document cookies before refresh:", document.cookie);
  
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: 'include'
    }

    const response = await fetch(`${BACKEND_URL}/refresh-token`, requestOptions);
    if (response.status !== 200) {
      if (response.status == 401)
          throw new Error("Unauthorised");
      else {
          throw new Error("refresh failed");
      }
    }
  
    const data = await response.json();
    return data;
  };

