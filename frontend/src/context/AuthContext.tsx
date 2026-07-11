import { createContext, useContext, useState, type ReactNode } from "react";
import API from "../services/api";

interface AuthContextType {
  email: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [email, setEmail] = useState<string | null>(
    localStorage.getItem("edurag_email")
  );
  const [error, setError] = useState<string | null>(null);

  const login = async (loginEmail: string, password: string) => {
    setError(null);
    try {
      const response = await API.post("/auth/login", { email: loginEmail, password });
      localStorage.setItem("edurag_token", response.data.token);
      localStorage.setItem("edurag_email", response.data.email);
      setEmail(response.data.email);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed. Check your email and password.");
      throw err;
    }
  };

  const signup = async (signupEmail: string, password: string) => {
    setError(null);
    try {
      const response = await API.post("/auth/signup", { email: signupEmail, password });
      localStorage.setItem("edurag_token", response.data.token);
      localStorage.setItem("edurag_email", response.data.email);
      setEmail(response.data.email);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Signup failed. That email may already be registered.");
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem("edurag_token");
    localStorage.removeItem("edurag_email");
    setEmail(null);
  };

  return (
    <AuthContext.Provider
      value={{ email, isAuthenticated: !!email, login, signup, logout, error }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}