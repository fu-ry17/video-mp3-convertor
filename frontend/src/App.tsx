import { useEffect } from "react";
import axios from "axios";

const App = () => {
  useEffect(() => {
    console.log("App mounted");
    const testAuth = async () => {
      const res = await axios.post("/api/auth/sign-in", {
        email: "cool@gmail.com",
        password: "123456",
      });
      console.log(res.data);
    };
    testAuth();
  }, []);

  return <div>Home Page</div>;
};

export default App;
