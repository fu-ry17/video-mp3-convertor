import { AuthLayout } from "@/auth/components/auth-layout";
import { SignInForm } from "@/auth/components/sign-in-form";

export default function SignIn() {
  return (
    <AuthLayout>
      <SignInForm />
    </AuthLayout>
  );
}
