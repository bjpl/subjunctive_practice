import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  message?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function LoadingSpinner({
  message = "Loading...",
  size = "lg",
  className
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: "h-8 w-8",
    md: "h-16 w-16",
    lg: "h-32 w-32"
  };

  return (
    <div className={cn("flex min-h-screen items-center justify-center bg-background", className)}>
      <div className="text-center">
        <div
          className={cn(
            "animate-spin rounded-full border-b-2 border-t-2 border-primary mx-auto",
            sizeClasses[size]
          )}
        />
        {message && (
          <p className="mt-4 text-lg text-muted-foreground">{message}</p>
        )}
      </div>
    </div>
  );
}
