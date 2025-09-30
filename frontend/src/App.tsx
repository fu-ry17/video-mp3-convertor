import { Route, Routes } from "react-router-dom";
import SignIn from "./pages/sign-in";
import SignUp from "./pages/sign-up";
import { useAuth } from "./auth/auth-hook";

const App = () => {
  const { session } = useAuth();
  const { data, isLoading, error } = session;

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!data) {
    return <div>No session data available</div>;
  }

  return (
    <div className="w-full">
      <Routes>
        <Route element={<SignIn />} path="/sign-in" />
        <Route element={<SignUp />} path="/sign-up" />
      </Routes>
    </div>
  );
};

export default App;
