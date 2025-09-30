import { z } from "zod";

export const loginSchema = z.object({
  email: z.email({
    message: "Please enter a valid email address.",
  }),
  password: z.string().min(6, {
    message: "Password must be at least 6 characters.",
  }),
});

export const registerSchema = z.object({
  name: z.string().min(3, "Full name is required"),
  email: z.email({ message: "Enter a valid email" }),
  password: z.string().min(8, "Minimum 8 characters"),
});

export const forgotPasswordSchema = z.object({
  email: z.email({
    message: "Please enter a valid email address.",
  }),
});

export const resetPasswordSchema = z
  .object({
    password: z.string().min(8, {
      message: "Password must be at least 8 characters.",
    }),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });
