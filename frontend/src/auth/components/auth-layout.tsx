export const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="pt-20 bg-neutral-100 dark:bg-background min-h-screen flex flex-col w-full items-center">
      {children}
    </div>
  );
};
