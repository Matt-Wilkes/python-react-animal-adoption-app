import { useState, useEffect, createContext, useContext } from "react";
import { loginService, logoutService, refreshToken } from "../../services/authService"
import { jwtDecode } from "jwt-decode";


const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
  const [token, setToken] = useState();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false); 

  const isTokenExpired = (token) => {
    // if there isn't a token, return true
    if (!token) return true
    try {
    // if there is a token, decode the token
      const decoded = jwtDecode(token);
      return decoded.exp * 1000 < Date.now() - 30000;
    } catch (error) {
      return true;
    }
  }

  // initAuth will run on mount
useEffect(() => {
const initAuth = async () => {
  try {
    console.log("Initializing auth state...");
    const data = await refreshToken()
    if (data && data.token) {
      
      console.log("Retrieved token during init")
      setToken(data.token); // or should be token?
      setIsAuthenticated(true);
    }
    else {
      console.error("no token data")
      // setIsAuthenticated(false);
    }
  }
  catch (error) {
    console.error('Failed to initialize auth', error);
    setIsAuthenticated(false)
  }
  finally {
    setIsLoading(false)
    console.log('initAuth has finished')
  }
};

initAuth()

}, [])

const handleRefreshToken = async () => {

  if (refreshing) return false;

  try {
    setRefreshing(true)
    console.log('attempting to refresh token')
    const data = await refreshToken();

    if (data && data.token) {
      console.log('token refreshed successfully')
      setToken(data.token);
      return true;
    } else {
      console.log('token refresh failed - no token returned');
      setIsAuthenticated(false);
      return false
    }
  } catch (error) {
    console.error("Token refresh error:", error);
    setIsAuthenticated(false);
    return false;
  } finally {
    setRefreshing(false)
  }
};

const handleLogin = async (email, password) => {
  try {
    console.log('attempting login...')
    const data = await loginService(email, password);
    if (data && data.token) {
      console.log("Login successful")
      setToken(data.token)
      setIsAuthenticated(true);
      return true
    }
    return false
  } catch (error) {
    console.error("Login error", error);
    setIsAuthenticated(false);
    return false;
  }
}

const handleLogout = async () => {
  try {
    console.log("logging out");
    await logoutService();
    setToken(null);
    setIsAuthenticated(false);

    navigate("/login");
    return true
  } catch (error) {
    console.error("Logout error", error)
    return false;
  }
}


const authFetch = async(url, options = {}) => {
  // check if token is expired
  // if expired -> try to refresh the token
  // if the token can't be refreshed, get a new token
  if (isTokenExpired(token)) {
    console.log("Token expired, attempting refresh before fetch");
    const refreshed = handleRefreshToken();
   
  }
  // make the request using the current token
  const authOptions = {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      },
    };
  try {
    const response = await fetch(url, authOptions);

  if (response.status === 401) {
    console.log("Receved 401 from fetch, attempting token refresh");
    const refreshed = handleRefreshToken();

    if (refreshed) {
      console.log("token refreshed after 401, retrying fetch");
      authOptions.headers.Authorization = `Bearer ${data.token}`;
      return fetch(url, authOptions);
    } else {
      console.log("Token refresh failed after 401")
      throw new Error('Session expired');
    }
  }
  return response;
  } catch (error) {
    console.error("Auth fethc error:", error)
    throw error;
}
  
} 

const contextValue = {
    token,
    isAuthenticated,
    isLoading,
    login: handleLogin,
    logout: handleLogout,
    authFetch
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {!isLoading && children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export { AuthProvider, useAuth};