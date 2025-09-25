import { Route, Routes } from "react-router-dom";
import SignIn from "./pages/sign-in";
import SignUp from "./pages/sign-up";

const App = () => {
  return (
    <div>
      <h1> Video MP3 Converter HomePage </h1>
      <Routes>
        <Route element={<SignIn />} path="/sign-in" />
        <Route element={<SignUp />} path="/sign-up" />
      </Routes>
    </div>
  );
};

export default App;
