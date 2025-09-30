import { useMutation, useQuery } from "@tanstack/react-query";
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
      toast.success("Logged in successfully!");
      sessionStorage.setItem("mp3_refresh_token", data.refresh_token);
      navigate("/");
    },
    onError: (error) => {
      sessionStorage.removeItem("refresh_token");
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

  const logout = useMutation({
    mutationFn: async () => {
      sessionStorage.removeItem("mp3_refresh_token");
      navigate("/sign-in");
      return true;
    },
    onSuccess: () => {
      toast.success("Logged out successfully!");
    },
    onError: (error) => {
      handleError(error);
    },
  });

  const session = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const refresh_token = sessionStorage.getItem("mp3_refresh_token");
      const access_token = await axios.get(`/api/auth/refresh-token`, {
        headers: { Authorization: `Bearer ${refresh_token}` },
      });

      console.log({ refresh_token, access_token });
      return true;
    },
  });

  return { signIn, signUp, logout, session };
};
