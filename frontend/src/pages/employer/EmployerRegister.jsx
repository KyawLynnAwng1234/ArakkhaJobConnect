import { useState, useEffect } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useEmployerAuth } from "../../hooks/useEmployerAuth";
import logo from "../../assets/images/logo.png";
import usePageTitle from "../../hooks/usePageTitle";

export default function EmployerRegister() {
  usePageTitle("Employer Register");
  const navigate = useNavigate();
  const { register } = useEmployerAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Errors
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [formError, setFormError] = useState("");

  const [loading, setLoading] = useState(false);

  // NEW: Email check states
  const [emailChecking, setEmailChecking] = useState(false);
  const [emailExists, setEmailExists] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  // AJAX email check (Step 1)
  useEffect(() => {
    if (!email) return;
    setEmailError(""); // clear error when typing

    const delay = setTimeout(async () => {
      setEmailChecking(true);

      try {
        const res = await fetch(
          `${API_URL}/accounts/check-email/?email=${email}`
        );
        const data = await res.json();
        setEmailExists(data.exists);
      } catch (err) {
        console.error("Email check error:", err);
      } finally {
        setEmailChecking(false);
      }
    }, 500); // debounce

    return () => clearTimeout(delay);
  }, [email]);

  // Submit Step 1 → Only continue if email is available
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    setPasswordError("");
    setEmailError("");

    if (!email.trim()) {
      setEmailError("Email is required");
      return;
    }
    if (!password.trim()) {
      setPasswordError("Password is required");
      return;
    }
    if (emailExists) {
      setEmailError("Email already exists");
      return;
    }

    setLoading(true);

    try {
      const newUser = await register(email, password);

      navigate("/employer/company/detail", {
        state: { email: newUser.email, password },
      });
    } catch (err) {
      const data = err?.response?.data;

      if (data?.code === "EMAIL_EXISTS") {
        setEmailError("Email already exists.");
        setLoading(false);
        return;
      }

      setFormError(data?.error || "Registration failed. Try again.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center font-inter">
      {/* HEADER */}
      <header className="fixed top-0 left-0 w-full z-50 bg-white shadow-md">
        <div className="container mx-auto px-4 py-1.5 flex items-center justify-between">
          <NavLink to="/" className="text-2xl font-bold custom-blue-text">
            <img src={logo} alt="JobSeeker Logo" className="h-13 object-contain" />
          </NavLink>
        </div>
      </header>

      {/* CARD */}
      <div className="bg-blue-50 rounded-2xl shadow-md w-full max-w-md p-8 text-center mt-14">
        <p className="text-gray-600 mb-2">
          Are you looking for{" "}
          <Link to="/sign-in" className="text-blue-600">
            a job?
          </Link>
        </p>

        <h2 className="text-2xl font-bold mb-6">Register as an employer</h2>

        {formError && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 border border-red-300 rounded-lg text-sm">
            {formError}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-left">
          {/* EMAIL INPUT */}
          <div>
            <label className="block text-sm font-medium mb-1">Email Address</label>
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={`w-full border rounded-lg px-3 py-2 ${
                emailError ? "border-red-500" : "border-gray-300"
              }`}
            />

            {emailChecking && (
              <p className="text-blue-500 text-sm">Checking email...</p>
            )}

            {!emailChecking && emailExists && email.length > 3 && (
              <p className="text-red-500 text-sm">❌ Email already exists</p>
            )}

            {!emailChecking && !emailExists && email.length > 3 && (
              <p className="text-green-600 text-sm">✔ Email available</p>
            )}

            {emailError && (
              <p className="text-red-500 text-sm mt-1">{emailError}</p>
            )}
          </div>

          {/* PASSWORD INPUT */}
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={`w-full border rounded-lg px-3 py-2 ${
                passwordError ? "border-red-500" : "border-gray-300"
              }`}
            />
            {passwordError && (
              <p className="text-red-500 text-sm mt-1">{passwordError}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || emailExists}
            className={`w-full text-white rounded-lg py-2 font-medium transition ${
              loading || emailExists
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Checking..." : "Register"}
          </button>
        </form>

        <p className="mt-4 text-sm text-gray-600">
          Already have your account?{" "}
          <Link to="/employer/sign-in" className="text-blue-600 hover:underline">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
