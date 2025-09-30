import { useMutation } from "@tanstack/react-query";
import type z from "zod";
import type { loginSchema, registerSchema } from "./schema";
import { handleError } from "@/lib/handle-error";
import axios from "axios";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";

export const useAuth = () => {
  const navigate = useNavigate();

  const signIn = useMutation({
    mutationFn: async (payload: z.Infer<typeof loginSchema>) => {
      const res = await axios.post(`/api/auth/sign-in`, payload);
      return res.data;
    },
    onSuccess: (data) => {
      console.log({ data });
      toast.success("Logged in successfully!");
      sessionStorage.setItem("refresh_token", data.refresh_token);
      navigate("/");
    },
    onError: (error) => {
      handleError(error);
    },
  });

  const signUp = useMutation({
    mutationFn: async (payload: z.Infer<typeof registerSchema>) => {
      const res = await axios.post(`/api/auth/sign-up`, {
        ...payload,
        username: payload.email,
      });
      return res.data;
    },
    onSuccess: () => {
      toast.success("Registration successful!");
      navigate("/sign-in");
    },
    onError: (error) => {
      handleError(error);
    },
  });

  return { signIn, signUp };
};
