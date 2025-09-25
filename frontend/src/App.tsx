import { Route, Routes } from "react-router-dom";
import SignIn from "./pages/sign-in";
import SignUp from "./pages/sign-up";

const App = () => {
  return (
    <div>
      <Routes>
        <Route element={<SignIn />} path="/sign-in" />
        <Route element={<SignUp />} path="/sign-up" />
      </Routes>
    </div>
  );
};

export default App;
