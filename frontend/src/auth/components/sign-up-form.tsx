"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Loader2 } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { registerSchema } from "../schema";
import { Link } from "react-router-dom";
import { useAuth } from "../auth-hook";

export const SignUpForm = () => {
  const { signUp } = useAuth();

  const form = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
    },
  });

  const onSubmit = (values: z.infer<typeof registerSchema>) => {
    signUp.mutate(values);
  };

  return (
    <Card className="w-full h-full md:w-[400px] border-none shadow-none">
      <CardHeader className="flex items-center justify-center text-center p-7 flex-col">
        <CardTitle className="text-2xl">Sign Up</CardTitle>
        <CardDescription>
          By signing up , you agree to our {""}
          <Link to={`/privacy`}>
            <span className="text-blue-700">Privacy Policy</span>
          </Link>{" "}
          and {""}
          <Link to={`/terms`}>
            <span className="text-blue-700"> Terms of Service</span>
          </Link>
        </CardDescription>
      </CardHeader>

      <div className="px-7">
        <Separator />
      </div>

      <CardContent className="p-7">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              name="name"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      {...field}
                      type="text"
                      placeholder="Enter name"
                      disabled={signUp.isPending}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              name="email"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      {...field}
                      type="text"
                      placeholder="Enter email address"
                      disabled={signUp.isPending}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              name="password"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <Input
                      {...field}
                      type="password"
                      placeholder="Enter password"
                      disabled={signUp.isPending}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button className="w-full" size="lg" disabled={signUp.isPending}>
              {signUp.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Sign Up
            </Button>
          </form>
        </Form>
      </CardContent>

      <div className="px-7">
        <Separator />
      </div>

      <CardContent className="p-7 flex items-center justify-center text-sm">
        <p>
          Already have an account?
          <Link to="/sign-in">
            <span className="text-blue-700">&nbsp; Sign In</span>
          </Link>
        </p>
      </CardContent>
    </Card>
  );
};
