import { AuthLayout } from "@/auth/components/auth-layout";
import { SignUpForm } from "@/auth/components/sign-up-form";

const SignUp = () => {
  return (
    <AuthLayout>
      <SignUpForm />
    </AuthLayout>
  );
};

export default SignUp;
